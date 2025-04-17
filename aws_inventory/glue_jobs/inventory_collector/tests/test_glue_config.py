import pytest
from config.glue_config import (
    GLUE_JOB_CONFIG,
    GLUE_JOB_ARGS,
    GLUE_JOB_SCHEDULE,
    GLUE_SECURITY_CONFIG,
    GLUE_MONITORING_CONFIG,
    GLUE_JOB_TAGS,
    GLUE_JOB_CONNECTIONS,
    GLUE_JOB_CLASSIFIERS,
    GLUE_JOB_PARAMETERS
)

def test_glue_job_config():
    """Test Glue job configuration"""
    assert GLUE_JOB_CONFIG["name"] == "aws-inventory-collector"
    assert GLUE_JOB_CONFIG["description"] == "Collects and processes inventory data from AWS services"
    assert GLUE_JOB_CONFIG["role"] == "AWSGlueServiceRole-InventoryCollector"
    assert GLUE_JOB_CONFIG["glue_version"] == "3.0"
    assert GLUE_JOB_CONFIG["worker_type"] == "G.1X"
    assert GLUE_JOB_CONFIG["number_of_workers"] == 2
    assert GLUE_JOB_CONFIG["timeout"] == 3600
    assert GLUE_JOB_CONFIG["max_retries"] == 0
    assert GLUE_JOB_CONFIG["max_concurrent_runs"] == 1

def test_glue_job_args():
    """Test Glue job arguments"""
    assert GLUE_JOB_ARGS["--job-language"] == "python"
    assert GLUE_JOB_ARGS["--job-bookmark-option"] == "job-bookmark-enable"
    assert GLUE_JOB_ARGS["--enable-metrics"] == "true"
    assert GLUE_JOB_ARGS["--enable-continuous-cloudwatch-log"] == "true"
    assert GLUE_JOB_ARGS["--enable-spark-ui"] == "true"
    assert GLUE_JOB_ARGS["--spark-event-logs-path"] == "s3://aws-inventory-data/spark-logs/"
    assert GLUE_JOB_ARGS["--extra-py-files"] == "s3://aws-inventory-data/glue_jobs/inventory_collector/glue_job.zip"
    assert GLUE_JOB_ARGS["--additional-python-modules"] == "boto3==1.26.137,botocore==1.29.137"

def test_glue_job_schedule():
    """Test Glue job schedule"""
    assert GLUE_JOB_SCHEDULE["name"] == "aws-inventory-collector-trigger"
    assert GLUE_JOB_SCHEDULE["description"] == "Daily trigger for AWS inventory collection"
    assert GLUE_JOB_SCHEDULE["schedule"] == "cron(0 12 * * ? *)"
    assert GLUE_JOB_SCHEDULE["type"] == "SCHEDULED"
    assert GLUE_JOB_SCHEDULE["start_on_creation"] is True

def test_glue_security_config():
    """Test Glue job security configuration"""
    assert GLUE_SECURITY_CONFIG["name"] == "aws-inventory-collector-security"
    assert GLUE_SECURITY_CONFIG["encryption_configuration"]["s3_encryption"]["s3_encryption_mode"] == "SSE-S3"
    assert GLUE_SECURITY_CONFIG["encryption_configuration"]["cloud_watch_encryption"]["cloud_watch_encryption_mode"] == "DISABLED"
    assert GLUE_SECURITY_CONFIG["encryption_configuration"]["job_bookmarks_encryption"]["job_bookmarks_encryption_mode"] == "DISABLED"

def test_glue_monitoring_config():
    """Test Glue job monitoring configuration"""
    assert GLUE_MONITORING_CONFIG["cloud_watch_logs"]["enabled"] is True
    assert GLUE_MONITORING_CONFIG["cloud_watch_logs"]["log_group"] == "/aws-glue/jobs/aws-inventory-collector"
    assert GLUE_MONITORING_CONFIG["cloud_watch_logs"]["log_stream_prefix"] == "aws-inventory-collector"
    assert GLUE_MONITORING_CONFIG["job_metrics"]["enabled"] is True
    assert GLUE_MONITORING_CONFIG["job_metrics"]["cloud_watch_namespace"] == "AWS/Glue"
    assert len(GLUE_MONITORING_CONFIG["job_metrics"]["metrics"]) == 10

def test_glue_job_tags():
    """Test Glue job tags"""
    assert GLUE_JOB_TAGS["Project"] == "AWS Inventory Management"
    assert GLUE_JOB_TAGS["Environment"] == "Production"
    assert GLUE_JOB_TAGS["Owner"] == "Data Engineering Team"
    assert GLUE_JOB_TAGS["CostCenter"] == "12345"

def test_glue_job_connections():
    """Test Glue job connections"""
    assert len(GLUE_JOB_CONNECTIONS) == 1
    assert GLUE_JOB_CONNECTIONS[0] == "aws-inventory-vpc-connection"

def test_glue_job_classifiers():
    """Test Glue job classifiers"""
    assert len(GLUE_JOB_CLASSIFIERS) == 1
    assert GLUE_JOB_CLASSIFIERS[0] == "aws-inventory-classifier"

def test_glue_job_parameters():
    """Test Glue job parameters"""
    assert len(GLUE_JOB_PARAMETERS["REGIONS"]) == 4
    assert GLUE_JOB_PARAMETERS["S3_BUCKET"] == "aws-inventory-data"
    assert GLUE_JOB_PARAMETERS["GLUE_DATABASE"] == "aws_inventory"
    assert len(GLUE_JOB_PARAMETERS["GLUE_TABLES"]) == 5
    assert GLUE_JOB_PARAMETERS["GLUE_TABLES"]["ec2"] == "ec2_instances"
    assert GLUE_JOB_PARAMETERS["GLUE_TABLES"]["s3"] == "s3_buckets"
    assert GLUE_JOB_PARAMETERS["GLUE_TABLES"]["rds"] == "rds_instances"
    assert GLUE_JOB_PARAMETERS["GLUE_TABLES"]["lambda"] == "lambda_functions"
    assert GLUE_JOB_PARAMETERS["GLUE_TABLES"]["iam"] == "iam_roles" 