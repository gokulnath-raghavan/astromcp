from typing import Dict, List, Tuple

# EC2 data quality configuration
EC2_CONFIG = {
    "required_columns": [
        "instance_id",
        "instance_type",
        "state",
        "launch_time",
        "vpc_id",
        "subnet_id",
        "platform",
        "architecture",
        "root_device_type",
        "root_device_name",
        "public_ip",
        "private_ip",
        "security_groups",
        "iam_profile",
        "metadata_options",
        "collection_date",
        "collection_timestamp"
    ],
    "expected_types": {
        "instance_id": "string",
        "instance_type": "string",
        "state": "string",
        "launch_time": "timestamp",
        "vpc_id": "string",
        "subnet_id": "string",
        "platform": "string",
        "architecture": "string",
        "root_device_type": "string",
        "root_device_name": "string",
        "public_ip": "string",
        "private_ip": "string",
        "security_groups": "array",
        "iam_profile": "string",
        "metadata_options": "struct",
        "collection_date": "date",
        "collection_timestamp": "timestamp"
    },
    "null_check_columns": [
        "instance_id",
        "instance_type",
        "state",
        "launch_time",
        "vpc_id",
        "subnet_id",
        "architecture"
    ],
    "key_columns": ["instance_id"],
    "column_ranges": {
        "launch_time": ("2020-01-01", "2025-12-31")  # Valid date range
    }
}

# S3 data quality configuration
S3_CONFIG = {
    "required_columns": [
        "bucket_name",
        "creation_date",
        "region",
        "versioning_status",
        "encryption_status",
        "public_access_block",
        "tags",
        "collection_date",
        "collection_timestamp"
    ],
    "expected_types": {
        "bucket_name": "string",
        "creation_date": "timestamp",
        "region": "string",
        "versioning_status": "string",
        "encryption_status": "string",
        "public_access_block": "struct",
        "tags": "array",
        "collection_date": "date",
        "collection_timestamp": "timestamp"
    },
    "null_check_columns": [
        "bucket_name",
        "creation_date",
        "region"
    ],
    "key_columns": ["bucket_name"],
    "column_ranges": {
        "creation_date": ("2006-03-14", "2025-12-31")  # S3 launch date to future
    }
}

# RDS data quality configuration
RDS_CONFIG = {
    "required_columns": [
        "db_instance_identifier",
        "engine",
        "engine_version",
        "instance_class",
        "allocated_storage",
        "storage_type",
        "master_username",
        "endpoint",
        "port",
        "vpc_id",
        "subnet_group",
        "security_groups",
        "parameter_groups",
        "option_groups",
        "backup_retention_period",
        "multi_az",
        "publicly_accessible",
        "storage_encrypted",
        "collection_date",
        "collection_timestamp"
    ],
    "expected_types": {
        "db_instance_identifier": "string",
        "engine": "string",
        "engine_version": "string",
        "instance_class": "string",
        "allocated_storage": "integer",
        "storage_type": "string",
        "master_username": "string",
        "endpoint": "string",
        "port": "integer",
        "vpc_id": "string",
        "subnet_group": "string",
        "security_groups": "array",
        "parameter_groups": "array",
        "option_groups": "array",
        "backup_retention_period": "integer",
        "multi_az": "boolean",
        "publicly_accessible": "boolean",
        "storage_encrypted": "boolean",
        "collection_date": "date",
        "collection_timestamp": "timestamp"
    },
    "null_check_columns": [
        "db_instance_identifier",
        "engine",
        "engine_version",
        "instance_class",
        "allocated_storage",
        "storage_type"
    ],
    "key_columns": ["db_instance_identifier"],
    "column_ranges": {
        "allocated_storage": (5, 65536),  # Min 5GB, Max 64TB
        "backup_retention_period": (0, 35),  # 0-35 days
        "port": (1150, 65535)  # Valid port range
    }
}

# Lambda data quality configuration
LAMBDA_CONFIG = {
    "required_columns": [
        "function_name",
        "runtime",
        "handler",
        "code_size",
        "memory_size",
        "timeout",
        "last_modified",
        "vpc_config",
        "environment",
        "tags",
        "collection_date",
        "collection_timestamp"
    ],
    "expected_types": {
        "function_name": "string",
        "runtime": "string",
        "handler": "string",
        "code_size": "long",
        "memory_size": "integer",
        "timeout": "integer",
        "last_modified": "timestamp",
        "vpc_config": "struct",
        "environment": "struct",
        "tags": "array",
        "collection_date": "date",
        "collection_timestamp": "timestamp"
    },
    "null_check_columns": [
        "function_name",
        "runtime",
        "handler",
        "code_size",
        "memory_size",
        "timeout"
    ],
    "key_columns": ["function_name"],
    "column_ranges": {
        "memory_size": (128, 10240),  # 128MB to 10GB
        "timeout": (1, 900),  # 1 to 900 seconds
        "code_size": (0, 524288000)  # 0 to 500MB
    }
}

# IAM data quality configuration
IAM_CONFIG = {
    "required_columns": [
        "role_name",
        "role_id",
        "arn",
        "create_date",
        "path",
        "max_session_duration",
        "assume_role_policy_document",
        "description",
        "tags",
        "collection_date",
        "collection_timestamp"
    ],
    "expected_types": {
        "role_name": "string",
        "role_id": "string",
        "arn": "string",
        "create_date": "timestamp",
        "path": "string",
        "max_session_duration": "integer",
        "assume_role_policy_document": "string",
        "description": "string",
        "tags": "array",
        "collection_date": "date",
        "collection_timestamp": "timestamp"
    },
    "null_check_columns": [
        "role_name",
        "role_id",
        "arn",
        "create_date"
    ],
    "key_columns": ["role_name"],
    "column_ranges": {
        "max_session_duration": (3600, 43200),  # 1 to 12 hours
        "create_date": ("2006-03-14", "2025-12-31")  # IAM launch date to future
    }
}

# Service to configuration mapping
SERVICE_CONFIGS = {
    "ec2": EC2_CONFIG,
    "s3": S3_CONFIG,
    "rds": RDS_CONFIG,
    "lambda": LAMBDA_CONFIG,
    "iam": IAM_CONFIG
} 