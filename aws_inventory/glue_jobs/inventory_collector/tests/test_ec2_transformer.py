import pytest
from pyspark.sql import SparkSession
from datetime import datetime
from ..transforms.ec2_transformer import transform_ec2_data

@pytest.fixture(scope="session")
def spark():
    """
    Create a SparkSession for testing.
    """
    spark = SparkSession.builder \
        .appName("test_ec2_transformer") \
        .master("local[2]") \
        .getOrCreate()
    yield spark
    spark.stop()

@pytest.fixture
def sample_ec2_data(spark):
    """
    Create sample EC2 data for testing.
    """
    data = [
        {
            "InstanceId": "i-1234567890abcdef0",
            "InstanceType": "t2.micro",
            "State": {"Name": "running"},
            "Tags": [{"Key": "Name", "Value": "test-instance"}],
            "LaunchTime": "2023-01-01T00:00:00Z",
            "VpcId": "vpc-12345678",
            "SubnetId": "subnet-12345678",
            "Platform": "linux",
            "Architecture": "x86_64",
            "RootDeviceType": "ebs",
            "RootDeviceName": "/dev/xvda",
            "PublicIpAddress": "1.2.3.4",
            "PrivateIpAddress": "10.0.0.1",
            "SecurityGroups": [
                {"GroupId": "sg-12345678", "GroupName": "test-sg"}
            ],
            "IamInstanceProfile": {"Arn": "arn:aws:iam::123456789012:instance-profile/test-profile"},
            "MetadataOptions": {"HttpTokens": "optional", "HttpEndpoint": "enabled"}
        }
    ]
    return spark.createDataFrame(data)

def test_transform_ec2_data(spark, sample_ec2_data):
    """
    Test the EC2 data transformation.
    """
    # Transform the data
    transformed_df = transform_ec2_data(sample_ec2_data)
    
    # Check schema
    expected_columns = [
        "instance_id", "instance_type", "state", "tags",
        "launch_time", "vpc_id", "subnet_id", "platform",
        "architecture", "root_device_type", "root_device_name",
        "public_ip", "private_ip", "security_groups",
        "iam_profile", "metadata_options", "collection_date",
        "collection_timestamp"
    ]
    assert all(col in transformed_df.columns for col in expected_columns)
    
    # Check data types
    assert transformed_df.schema["instance_id"].dataType.typeName() == "string"
    assert transformed_df.schema["launch_time"].dataType.typeName() == "timestamp"
    assert transformed_df.schema["tags"].dataType.typeName() == "array"
    assert transformed_df.schema["security_groups"].dataType.typeName() == "array"
    
    # Check values
    row = transformed_df.first()
    assert row.instance_id == "i-1234567890abcdef0"
    assert row.instance_type == "t2.micro"
    assert row.state == "running"
    assert row.tags[0]["Key"] == "Name"
    assert row.tags[0]["Value"] == "test-instance"
    assert row.security_groups[0]["GroupId"] == "sg-12345678"
    assert row.security_groups[0]["GroupName"] == "test-sg"
    assert row.iam_profile == "arn:aws:iam::123456789012:instance-profile/test-profile"
    assert row.metadata_options["HttpTokens"] == "optional"
    assert row.metadata_options["HttpEndpoint"] == "enabled"
    
    # Check metadata columns
    assert isinstance(row.collection_date, datetime)
    assert isinstance(row.collection_timestamp, datetime) 