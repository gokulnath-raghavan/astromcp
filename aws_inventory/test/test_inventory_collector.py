import pytest
from src.inventory_collector import AWSInventoryCollector
from unittest.mock import Mock, patch

@pytest.fixture
def mock_boto3():
    with patch('boto3.Session') as mock_session:
        yield mock_session

def test_collect_ec2_inventory(mock_boto3):
    # Setup mock EC2 client
    mock_ec2 = Mock()
    mock_ec2.describe_instances.return_value = {
        'Reservations': [
            {
                'Instances': [
                    {
                        'InstanceId': 'i-1234567890abcdef0',
                        'InstanceType': 't2.micro',
                        'State': {'Name': 'running'},
                        'Tags': [{'Key': 'Name', 'Value': 'TestInstance'}],
                        'LaunchTime': '2023-01-01T00:00:00Z',
                        'VpcId': 'vpc-12345678',
                        'SubnetId': 'subnet-12345678'
                    }
                ]
            }
        ]
    }
    
    mock_session = Mock()
    mock_session.client.return_value = mock_ec2
    mock_boto3.return_value = mock_session
    
    collector = AWSInventoryCollector()
    result = collector.collect_ec2_inventory('us-east-1')
    
    assert len(result) == 1
    assert result[0]['InstanceId'] == 'i-1234567890abcdef0'
    assert result[0]['InstanceType'] == 't2.micro'
    assert result[0]['State'] == 'running'

def test_collect_s3_inventory(mock_boto3):
    # Setup mock S3 client
    mock_s3 = Mock()
    mock_s3.list_buckets.return_value = {
        'Buckets': [
            {
                'Name': 'test-bucket',
                'CreationDate': '2023-01-01T00:00:00Z'
            }
        ]
    }
    mock_s3.get_bucket_location.return_value = {'LocationConstraint': 'us-east-1'}
    
    mock_session = Mock()
    mock_session.client.return_value = mock_s3
    mock_boto3.return_value = mock_session
    
    collector = AWSInventoryCollector()
    result = collector.collect_s3_inventory()
    
    assert len(result) == 1
    assert result[0]['Name'] == 'test-bucket'
    assert result[0]['Region'] == 'us-east-1'

def test_collect_rds_inventory(mock_boto3):
    # Setup mock RDS client
    mock_rds = Mock()
    mock_rds.describe_db_instances.return_value = {
        'DBInstances': [
            {
                'DBInstanceIdentifier': 'test-db',
                'Engine': 'mysql',
                'DBInstanceClass': 'db.t2.micro',
                'AllocatedStorage': 20,
                'Endpoint': {'Address': 'test-db.123456789012.us-east-1.rds.amazonaws.com'},
                'MultiAZ': False
            }
        ]
    }
    
    mock_session = Mock()
    mock_session.client.return_value = mock_rds
    mock_boto3.return_value = mock_session
    
    collector = AWSInventoryCollector()
    result = collector.collect_rds_inventory('us-east-1')
    
    assert len(result) == 1
    assert result[0]['DBInstanceIdentifier'] == 'test-db'
    assert result[0]['Engine'] == 'mysql'
    assert result[0]['DBInstanceClass'] == 'db.t2.micro' 