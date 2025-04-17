import pytest
from ..config.data_quality_config import (
    EC2_CONFIG,
    S3_CONFIG,
    RDS_CONFIG,
    LAMBDA_CONFIG,
    IAM_CONFIG,
    SERVICE_CONFIGS
)

def test_ec2_config():
    """
    Test EC2 data quality configuration.
    """
    # Check required columns
    assert "instance_id" in EC2_CONFIG["required_columns"]
    assert "instance_type" in EC2_CONFIG["required_columns"]
    assert "state" in EC2_CONFIG["required_columns"]
    assert "launch_time" in EC2_CONFIG["required_columns"]
    
    # Check expected types
    assert EC2_CONFIG["expected_types"]["instance_id"] == "string"
    assert EC2_CONFIG["expected_types"]["launch_time"] == "timestamp"
    assert EC2_CONFIG["expected_types"]["security_groups"] == "array"
    
    # Check null check columns
    assert "instance_id" in EC2_CONFIG["null_check_columns"]
    assert "instance_type" in EC2_CONFIG["null_check_columns"]
    assert "state" in EC2_CONFIG["null_check_columns"]
    
    # Check key columns
    assert EC2_CONFIG["key_columns"] == ["instance_id"]
    
    # Check column ranges
    assert "launch_time" in EC2_CONFIG["column_ranges"]
    assert len(EC2_CONFIG["column_ranges"]["launch_time"]) == 2

def test_s3_config():
    """
    Test S3 data quality configuration.
    """
    # Check required columns
    assert "bucket_name" in S3_CONFIG["required_columns"]
    assert "creation_date" in S3_CONFIG["required_columns"]
    assert "region" in S3_CONFIG["required_columns"]
    
    # Check expected types
    assert S3_CONFIG["expected_types"]["bucket_name"] == "string"
    assert S3_CONFIG["expected_types"]["creation_date"] == "timestamp"
    assert S3_CONFIG["expected_types"]["tags"] == "array"
    
    # Check null check columns
    assert "bucket_name" in S3_CONFIG["null_check_columns"]
    assert "creation_date" in S3_CONFIG["null_check_columns"]
    assert "region" in S3_CONFIG["null_check_columns"]
    
    # Check key columns
    assert S3_CONFIG["key_columns"] == ["bucket_name"]
    
    # Check column ranges
    assert "creation_date" in S3_CONFIG["column_ranges"]
    assert len(S3_CONFIG["column_ranges"]["creation_date"]) == 2

def test_rds_config():
    """
    Test RDS data quality configuration.
    """
    # Check required columns
    assert "db_instance_identifier" in RDS_CONFIG["required_columns"]
    assert "engine" in RDS_CONFIG["required_columns"]
    assert "engine_version" in RDS_CONFIG["required_columns"]
    assert "instance_class" in RDS_CONFIG["required_columns"]
    
    # Check expected types
    assert RDS_CONFIG["expected_types"]["db_instance_identifier"] == "string"
    assert RDS_CONFIG["expected_types"]["allocated_storage"] == "integer"
    assert RDS_CONFIG["expected_types"]["security_groups"] == "array"
    
    # Check null check columns
    assert "db_instance_identifier" in RDS_CONFIG["null_check_columns"]
    assert "engine" in RDS_CONFIG["null_check_columns"]
    assert "engine_version" in RDS_CONFIG["null_check_columns"]
    
    # Check key columns
    assert RDS_CONFIG["key_columns"] == ["db_instance_identifier"]
    
    # Check column ranges
    assert "allocated_storage" in RDS_CONFIG["column_ranges"]
    assert "backup_retention_period" in RDS_CONFIG["column_ranges"]
    assert "port" in RDS_CONFIG["column_ranges"]

def test_lambda_config():
    """
    Test Lambda data quality configuration.
    """
    # Check required columns
    assert "function_name" in LAMBDA_CONFIG["required_columns"]
    assert "runtime" in LAMBDA_CONFIG["required_columns"]
    assert "handler" in LAMBDA_CONFIG["required_columns"]
    assert "memory_size" in LAMBDA_CONFIG["required_columns"]
    
    # Check expected types
    assert LAMBDA_CONFIG["expected_types"]["function_name"] == "string"
    assert LAMBDA_CONFIG["expected_types"]["memory_size"] == "integer"
    assert LAMBDA_CONFIG["expected_types"]["tags"] == "array"
    
    # Check null check columns
    assert "function_name" in LAMBDA_CONFIG["null_check_columns"]
    assert "runtime" in LAMBDA_CONFIG["null_check_columns"]
    assert "handler" in LAMBDA_CONFIG["null_check_columns"]
    
    # Check key columns
    assert LAMBDA_CONFIG["key_columns"] == ["function_name"]
    
    # Check column ranges
    assert "memory_size" in LAMBDA_CONFIG["column_ranges"]
    assert "timeout" in LAMBDA_CONFIG["column_ranges"]
    assert "code_size" in LAMBDA_CONFIG["column_ranges"]

def test_iam_config():
    """
    Test IAM data quality configuration.
    """
    # Check required columns
    assert "role_name" in IAM_CONFIG["required_columns"]
    assert "role_id" in IAM_CONFIG["required_columns"]
    assert "arn" in IAM_CONFIG["required_columns"]
    assert "create_date" in IAM_CONFIG["required_columns"]
    
    # Check expected types
    assert IAM_CONFIG["expected_types"]["role_name"] == "string"
    assert IAM_CONFIG["expected_types"]["create_date"] == "timestamp"
    assert IAM_CONFIG["expected_types"]["tags"] == "array"
    
    # Check null check columns
    assert "role_name" in IAM_CONFIG["null_check_columns"]
    assert "role_id" in IAM_CONFIG["null_check_columns"]
    assert "arn" in IAM_CONFIG["null_check_columns"]
    
    # Check key columns
    assert IAM_CONFIG["key_columns"] == ["role_name"]
    
    # Check column ranges
    assert "max_session_duration" in IAM_CONFIG["column_ranges"]
    assert "create_date" in IAM_CONFIG["column_ranges"]

def test_service_configs():
    """
    Test service configurations mapping.
    """
    # Check all services are present
    assert "ec2" in SERVICE_CONFIGS
    assert "s3" in SERVICE_CONFIGS
    assert "rds" in SERVICE_CONFIGS
    assert "lambda" in SERVICE_CONFIGS
    assert "iam" in SERVICE_CONFIGS
    
    # Check configurations match
    assert SERVICE_CONFIGS["ec2"] == EC2_CONFIG
    assert SERVICE_CONFIGS["s3"] == S3_CONFIG
    assert SERVICE_CONFIGS["rds"] == RDS_CONFIG
    assert SERVICE_CONFIGS["lambda"] == LAMBDA_CONFIG
    assert SERVICE_CONFIGS["iam"] == IAM_CONFIG 