import boto3
import logging
from typing import Dict, List, Optional
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

class GlueJobManager:
    """Utility class for managing AWS Glue jobs"""
    
    def __init__(self, region: str = "us-east-1"):
        """Initialize the Glue job manager
        
        Args:
            region: AWS region name
        """
        self.glue_client = boto3.client("glue", region_name=region)
        self.s3_client = boto3.client("s3", region_name=region)
        self.cloudwatch_client = boto3.client("cloudwatch", region_name=region)
        
    def create_job(self, job_config: Dict) -> str:
        """Create a new Glue job
        
        Args:
            job_config: Glue job configuration dictionary
            
        Returns:
            str: The name of the created job
        """
        try:
            response = self.glue_client.create_job(
                Name=job_config["name"],
                Description=job_config["description"],
                Role=job_config["role"],
                GlueVersion=job_config["glue_version"],
                WorkerType=job_config["worker_type"],
                NumberOfWorkers=job_config["number_of_workers"],
                Timeout=job_config["timeout"],
                MaxRetries=job_config["max_retries"],
                MaxConcurrentRuns=job_config["max_concurrent_runs"],
                Command={
                    "Name": "glueetl",
                    "ScriptLocation": f"s3://{job_config['s3_bucket']}/glue_jobs/{job_config['name']}/main.py",
                    "PythonVersion": "3"
                },
                DefaultArguments=job_config["job_args"],
                Tags=job_config["tags"],
                Connections=job_config["connections"],
                MaxCapacity=job_config.get("max_capacity"),
                SecurityConfiguration=job_config.get("security_configuration"),
                NotificationProperty=job_config.get("notification_property"),
                ExecutionProperty=job_config.get("execution_property")
            )
            logger.info(f"Created Glue job: {job_config['name']}")
            return response["Name"]
        except ClientError as e:
            logger.error(f"Failed to create Glue job: {e}")
            raise
            
    def create_trigger(self, trigger_config: Dict) -> str:
        """Create a new Glue trigger
        
        Args:
            trigger_config: Glue trigger configuration dictionary
            
        Returns:
            str: The name of the created trigger
        """
        try:
            response = self.glue_client.create_trigger(
                Name=trigger_config["name"],
                Type=trigger_config["type"],
                Schedule=trigger_config.get("schedule"),
                Description=trigger_config.get("description"),
                Actions=[{
                    "JobName": trigger_config["job_name"]
                }],
                StartOnCreation=trigger_config.get("start_on_creation", True)
            )
            logger.info(f"Created Glue trigger: {trigger_config['name']}")
            return response["Name"]
        except ClientError as e:
            logger.error(f"Failed to create Glue trigger: {e}")
            raise
            
    def start_job_run(self, job_name: str, arguments: Optional[Dict] = None) -> str:
        """Start a Glue job run
        
        Args:
            job_name: Name of the Glue job
            arguments: Optional job arguments
            
        Returns:
            str: The ID of the job run
        """
        try:
            response = self.glue_client.start_job_run(
                JobName=job_name,
                Arguments=arguments or {}
            )
            logger.info(f"Started Glue job run: {response['JobRunId']}")
            return response["JobRunId"]
        except ClientError as e:
            logger.error(f"Failed to start Glue job run: {e}")
            raise
            
    def get_job_run_status(self, job_name: str, run_id: str) -> str:
        """Get the status of a Glue job run
        
        Args:
            job_name: Name of the Glue job
            run_id: ID of the job run
            
        Returns:
            str: The status of the job run
        """
        try:
            response = self.glue_client.get_job_run(
                JobName=job_name,
                RunId=run_id
            )
            return response["JobRun"]["JobRunState"]
        except ClientError as e:
            logger.error(f"Failed to get Glue job run status: {e}")
            raise
            
    def get_job_run_metrics(self, job_name: str, run_id: str) -> Dict:
        """Get metrics for a Glue job run
        
        Args:
            job_name: Name of the Glue job
            run_id: ID of the job run
            
        Returns:
            Dict: Job run metrics
        """
        try:
            response = self.glue_client.get_job_run(
                JobName=job_name,
                RunId=run_id
            )
            return {
                "ExecutionTime": response["JobRun"]["ExecutionTime"],
                "MaxCapacity": response["JobRun"]["MaxCapacity"],
                "NumberOfWorkers": response["JobRun"]["NumberOfWorkers"],
                "WorkerType": response["JobRun"]["WorkerType"],
                "CompletedOn": response["JobRun"].get("CompletedOn"),
                "StartedOn": response["JobRun"].get("StartedOn"),
                "ErrorMessage": response["JobRun"].get("ErrorMessage")
            }
        except ClientError as e:
            logger.error(f"Failed to get Glue job run metrics: {e}")
            raise
            
    def stop_job_run(self, job_name: str, run_id: str) -> None:
        """Stop a Glue job run
        
        Args:
            job_name: Name of the Glue job
            run_id: ID of the job run
        """
        try:
            self.glue_client.batch_stop_job_run(
                JobName=job_name,
                JobRunIds=[run_id]
            )
            logger.info(f"Stopped Glue job run: {run_id}")
        except ClientError as e:
            logger.error(f"Failed to stop Glue job run: {e}")
            raise
            
    def delete_job(self, job_name: str) -> None:
        """Delete a Glue job
        
        Args:
            job_name: Name of the Glue job
        """
        try:
            self.glue_client.delete_job(JobName=job_name)
            logger.info(f"Deleted Glue job: {job_name}")
        except ClientError as e:
            logger.error(f"Failed to delete Glue job: {e}")
            raise
            
    def list_jobs(self, tags: Optional[Dict] = None) -> List[str]:
        """List Glue jobs
        
        Args:
            tags: Optional tags to filter jobs
            
        Returns:
            List[str]: List of job names
        """
        try:
            response = self.glue_client.list_jobs(
                Tags=tags or {}
            )
            return response["JobNames"]
        except ClientError as e:
            logger.error(f"Failed to list Glue jobs: {e}")
            raise
            
    def update_job(self, job_name: str, job_config: Dict) -> None:
        """Update a Glue job
        
        Args:
            job_name: Name of the Glue job
            job_config: Updated job configuration
        """
        try:
            self.glue_client.update_job(
                JobName=job_name,
                JobUpdate={
                    "Description": job_config.get("description"),
                    "Role": job_config.get("role"),
                    "ExecutionProperty": job_config.get("execution_property"),
                    "Command": {
                        "Name": "glueetl",
                        "ScriptLocation": f"s3://{job_config['s3_bucket']}/glue_jobs/{job_name}/main.py",
                        "PythonVersion": "3"
                    },
                    "DefaultArguments": job_config.get("job_args"),
                    "Connections": job_config.get("connections"),
                    "MaxRetries": job_config.get("max_retries"),
                    "Timeout": job_config.get("timeout"),
                    "MaxCapacity": job_config.get("max_capacity"),
                    "WorkerType": job_config.get("worker_type"),
                    "NumberOfWorkers": job_config.get("number_of_workers"),
                    "SecurityConfiguration": job_config.get("security_configuration"),
                    "NotificationProperty": job_config.get("notification_property"),
                    "GlueVersion": job_config.get("glue_version")
                }
            )
            logger.info(f"Updated Glue job: {job_name}")
        except ClientError as e:
            logger.error(f"Failed to update Glue job: {e}")
            raise 