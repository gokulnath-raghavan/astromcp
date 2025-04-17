import boto3
from typing import Any
from botocore.config import Config

def get_aws_client(service: str, region: str = None) -> Any:
    """
    Get an AWS client with proper configuration.
    
    Args:
        service: AWS service name (e.g., 'ec2', 's3')
        region: AWS region name (e.g., 'us-east-1')
    
    Returns:
        boto3 client for the specified service
    """
    config = Config(
        retries = {
            'max_attempts': 3,
            'mode': 'adaptive'
        },
        connect_timeout = 5,
        read_timeout = 10
    )
    
    return boto3.client(
        service,
        region_name=region,
        config=config
    )

def get_aws_resource(service: str, region: str = None) -> Any:
    """
    Get an AWS resource with proper configuration.
    
    Args:
        service: AWS service name (e.g., 'ec2', 's3')
        region: AWS region name (e.g., 'us-east-1')
    
    Returns:
        boto3 resource for the specified service
    """
    config = Config(
        retries = {
            'max_attempts': 3,
            'mode': 'adaptive'
        },
        connect_timeout = 5,
        read_timeout = 10
    )
    
    return boto3.resource(
        service,
        region_name=region,
        config=config
    ) 