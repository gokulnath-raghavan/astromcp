from typing import Dict, List

# Glue job configuration
GLUE_JOB_CONFIG = {
    "name": "aws-inventory-collector",
    "description": "Collects and processes inventory data from AWS services",
    "role": "AWSGlueServiceRole-InventoryCollector",
    "glue_version": "3.0",
    "worker_type": "G.1X",
    "number_of_workers": 2,
    "timeout": 3600,  # 1 hour in seconds
    "max_retries": 0,
    "max_concurrent_runs": 1
}

# Glue job arguments
GLUE_JOB_ARGS = {
    "--job-language": "python",
    "--job-bookmark-option": "job-bookmark-enable",
    "--enable-metrics": "true",
    "--enable-continuous-cloudwatch-log": "true",
    "--enable-spark-ui": "true",
    "--spark-event-logs-path": "s3://aws-inventory-data/spark-logs/",
    "--extra-py-files": "s3://aws-inventory-data/glue_jobs/inventory_collector/glue_job.zip",
    "--additional-python-modules": "boto3==1.26.137,botocore==1.29.137"
}

# Glue job schedule
GLUE_JOB_SCHEDULE = {
    "name": "aws-inventory-collector-trigger",
    "description": "Daily trigger for AWS inventory collection",
    "schedule": "cron(0 12 * * ? *)",  # Daily at 12:00 UTC
    "type": "SCHEDULED",
    "start_on_creation": True
}

# Glue job security configuration
GLUE_SECURITY_CONFIG = {
    "name": "aws-inventory-collector-security",
    "encryption_configuration": {
        "s3_encryption": {
            "s3_encryption_mode": "SSE-S3"
        },
        "cloud_watch_encryption": {
            "cloud_watch_encryption_mode": "DISABLED"
        },
        "job_bookmarks_encryption": {
            "job_bookmarks_encryption_mode": "DISABLED"
        }
    }
}

# Glue job monitoring configuration
GLUE_MONITORING_CONFIG = {
    "cloud_watch_logs": {
        "enabled": True,
        "log_group": "/aws-glue/jobs/aws-inventory-collector",
        "log_stream_prefix": "aws-inventory-collector"
    },
    "job_metrics": {
        "enabled": True,
        "cloud_watch_namespace": "AWS/Glue",
        "metrics": [
            "glue.driver.aggregate.bytesRead",
            "glue.driver.aggregate.bytesWritten",
            "glue.driver.aggregate.elapsedTime",
            "glue.driver.aggregate.numCompletedStages",
            "glue.driver.aggregate.numFailedStages",
            "glue.driver.aggregate.numCompletedTasks",
            "glue.driver.aggregate.numFailedTasks",
            "glue.driver.aggregate.numKilledTasks",
            "glue.driver.aggregate.numCompletedJobs",
            "glue.driver.aggregate.numFailedJobs"
        ]
    }
}

# Glue job tags
GLUE_JOB_TAGS = {
    "Project": "AWS Inventory Management",
    "Environment": "Production",
    "Owner": "Data Engineering Team",
    "CostCenter": "12345"
}

# Glue job connections
GLUE_JOB_CONNECTIONS = [
    "aws-inventory-vpc-connection"
]

# Glue job classifiers
GLUE_JOB_CLASSIFIERS = [
    "aws-inventory-classifier"
]

# Glue job parameters
GLUE_JOB_PARAMETERS = {
    "REGIONS": ["us-east-1", "us-west-2", "eu-west-1", "ap-southeast-1"],
    "S3_BUCKET": "aws-inventory-data",
    "GLUE_DATABASE": "aws_inventory",
    "GLUE_TABLES": {
        "ec2": "ec2_instances",
        "s3": "s3_buckets",
        "rds": "rds_instances",
        "lambda": "lambda_functions",
        "iam": "iam_roles"
    }
} 