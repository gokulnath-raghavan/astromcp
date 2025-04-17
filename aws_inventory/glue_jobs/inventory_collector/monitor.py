import boto3
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class GlueJobMonitor:
    """
    Monitor AWS Glue jobs and collect metrics.
    """
    
    def __init__(self, job_name: str, region: str = "us-east-1"):
        """
        Initialize the monitor.
        
        Args:
            job_name: Name of the Glue job
            region: AWS region
        """
        self.job_name = job_name
        self.region = region
        self.glue = boto3.client("glue", region_name=region)
        self.cloudwatch = boto3.client("cloudwatch", region_name=region)
        self.logs = boto3.client("logs", region_name=region)
    
    def get_job_runs(self, hours: int = 24) -> List[Dict]:
        """
        Get recent job runs.
        
        Args:
            hours: Number of hours to look back
            
        Returns:
            List of job runs
        """
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=hours)
        
        response = self.glue.get_job_runs(
            JobName=self.job_name,
            StartedAfter=start_time.isoformat(),
            MaxResults=100
        )
        
        return response.get("JobRuns", [])
    
    def get_job_metrics(self, job_run_id: str) -> Dict:
        """
        Get metrics for a specific job run.
        
        Args:
            job_run_id: ID of the job run
            
        Returns:
            Dictionary of metrics
        """
        response = self.glue.get_job_run(
            JobName=self.job_name,
            RunId=job_run_id
        )
        
        job_run = response["JobRun"]
        return {
            "JobRunId": job_run["Id"],
            "StartedOn": job_run["StartedOn"],
            "CompletedOn": job_run.get("CompletedOn"),
            "ExecutionTime": job_run.get("ExecutionTime", 0),
            "DPUSeconds": job_run.get("DPUSeconds", 0),
            "Status": job_run["JobRunState"],
            "ErrorMessage": job_run.get("ErrorMessage"),
            "LogGroupName": f"/aws-glue/jobs/{self.job_name}",
            "LogStreamName": job_run_id
        }
    
    def get_cloudwatch_metrics(self, job_run_id: str) -> Dict:
        """
        Get CloudWatch metrics for a job run.
        
        Args:
            job_run_id: ID of the job run
            
        Returns:
            Dictionary of CloudWatch metrics
        """
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=1)
        
        metrics = {}
        for metric_name in ["glue.driver.aggregate.bytesRead", "glue.driver.aggregate.bytesWritten"]:
            response = self.cloudwatch.get_metric_statistics(
                Namespace="AWS/Glue",
                MetricName=metric_name,
                Dimensions=[
                    {"Name": "JobName", "Value": self.job_name},
                    {"Name": "JobRunId", "Value": job_run_id}
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=300,
                Statistics=["Sum"]
            )
            
            if response["Datapoints"]:
                metrics[metric_name] = response["Datapoints"][-1]["Sum"]
        
        return metrics
    
    def get_log_events(self, job_run_id: str, limit: int = 100) -> List[Dict]:
        """
        Get log events for a job run.
        
        Args:
            job_run_id: ID of the job run
            limit: Maximum number of events to return
            
        Returns:
            List of log events
        """
        try:
            response = self.logs.get_log_events(
                logGroupName=f"/aws-glue/jobs/{self.job_name}",
                logStreamName=job_run_id,
                limit=limit
            )
            return response.get("events", [])
        except Exception as e:
            print(f"Error getting log events: {e}")
            return []
    
    def generate_report(self, hours: int = 24) -> Dict:
        """
        Generate a monitoring report.
        
        Args:
            hours: Number of hours to include in the report
            
        Returns:
            Dictionary containing the report
        """
        job_runs = self.get_job_runs(hours)
        report = {
            "job_name": self.job_name,
            "time_period": f"Last {hours} hours",
            "total_runs": len(job_runs),
            "successful_runs": len([r for r in job_runs if r["JobRunState"] == "SUCCEEDED"]),
            "failed_runs": len([r for r in job_runs if r["JobRunState"] == "FAILED"]),
            "runs": []
        }
        
        for job_run in job_runs:
            run_id = job_run["Id"]
            metrics = self.get_job_metrics(run_id)
            cloudwatch_metrics = self.get_cloudwatch_metrics(run_id)
            log_events = self.get_log_events(run_id)
            
            report["runs"].append({
                "job_run_id": run_id,
                "start_time": job_run["StartedOn"].isoformat(),
                "end_time": job_run.get("CompletedOn", "").isoformat() if job_run.get("CompletedOn") else "",
                "status": job_run["JobRunState"],
                "execution_time": job_run.get("ExecutionTime", 0),
                "dpu_seconds": job_run.get("DPUSeconds", 0),
                "error_message": job_run.get("ErrorMessage"),
                "cloudwatch_metrics": cloudwatch_metrics,
                "recent_logs": [{"timestamp": e["timestamp"], "message": e["message"]} for e in log_events]
            })
        
        return report

def main():
    """
    Main function to run the monitor.
    """
    import argparse
    
    parser = argparse.ArgumentParser(description="Monitor AWS Glue jobs")
    parser.add_argument("--job-name", required=True, help="Name of the Glue job")
    parser.add_argument("--region", default="us-east-1", help="AWS region")
    parser.add_argument("--hours", type=int, default=24, help="Number of hours to look back")
    parser.add_argument("--output", choices=["json", "text"], default="text", help="Output format")
    
    args = parser.parse_args()
    
    monitor = GlueJobMonitor(args.job_name, args.region)
    report = monitor.generate_report(args.hours)
    
    if args.output == "json":
        print(json.dumps(report, indent=2))
    else:
        print(f"\nMonitoring Report for {args.job_name}")
        print(f"Time Period: Last {args.hours} hours")
        print(f"Total Runs: {report['total_runs']}")
        print(f"Successful Runs: {report['successful_runs']}")
        print(f"Failed Runs: {report['failed_runs']}")
        
        for run in report["runs"]:
            print(f"\nRun ID: {run['job_run_id']}")
            print(f"Status: {run['status']}")
            print(f"Start Time: {run['start_time']}")
            print(f"End Time: {run['end_time']}")
            print(f"Execution Time: {run['execution_time']} seconds")
            print(f"DPU Seconds: {run['dpu_seconds']}")
            
            if run["error_message"]:
                print(f"Error: {run['error_message']}")
            
            if run["cloudwatch_metrics"]:
                print("\nCloudWatch Metrics:")
                for metric, value in run["cloudwatch_metrics"].items():
                    print(f"  {metric}: {value}")

if __name__ == "__main__":
    main() 