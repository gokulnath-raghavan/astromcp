from typing import Dict, Any
from datetime import datetime

# AWS Regions to collect inventory from
REGIONS = [
    "us-east-1",
    "us-west-2",
    "eu-west-1",
    "ap-southeast-1"
]

# S3 paths
S3_BUCKET = "aws-inventory-data"
S3_RAW_PATH = "raw"
S3_PROCESSED_PATH = "processed"
S3_TEMP_PATH = "temp"

# Glue database and table names
GLUE_DATABASE = "aws_inventory"
GLUE_TABLES = {
    "ec2": "ec2_instances",
    "s3": "s3_buckets",
    "rds": "rds_instances",
    "lambda": "lambda_functions",
    "iam": "iam_roles"
}

# Spark configurations
SPARK_CONFIG = {
    "executor_memory": "4g",
    "driver_memory": "4g",
    "parallelism": "200",
    "shuffle_partitions": "200",
    "min_executors": "1",
    "max_executors": "10"
}

# Job metadata
JOB_METADATA = {
    "job_name": "aws_inventory_collector",
    "job_version": "1.0.0",
    "job_owner": "Data Engineering Team",
    "job_schedule": "daily",
    "job_timeout": 3600  # 1 hour in seconds
}

def get_current_timestamp() -> str:
    """
    Get current timestamp in ISO format.
    
    Returns:
        Current timestamp as string
    """
    return datetime.utcnow().isoformat()

def get_s3_paths(region: str, service: str) -> Dict[str, str]:
    """
    Get S3 paths for a specific region and service.
    
    Args:
        region: AWS region
        service: AWS service name
    
    Returns:
        Dictionary of S3 paths
    """
    timestamp = get_current_timestamp()
    return {
        "raw": f"s3://{S3_BUCKET}/{S3_RAW_PATH}/{region}/{service}/{timestamp}/",
        "processed": f"s3://{S3_BUCKET}/{S3_PROCESSED_PATH}/{region}/{service}/{timestamp}/",
        "temp": f"s3://{S3_BUCKET}/{S3_TEMP_PATH}/{region}/{service}/{timestamp}/"
    } 