import pytest
from unittest.mock import MagicMock, patch
from pyspark.sql import SparkSession
from datetime import datetime
from ..main import process_service_data, main
from ..utils.logger import GlueJobLogger
from ..utils.data_quality import DataQualityChecker

@pytest.fixture(scope="session")
def spark():
    """
    Create a SparkSession for testing.
    """
    spark = SparkSession.builder \
        .appName("test_main") \
        .master("local[2]") \
        .getOrCreate()
    yield spark
    spark.stop()

@pytest.fixture
def sample_data(spark):
    """
    Create sample data for testing.
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

@pytest.fixture
def mock_logger():
    """
    Create a mock logger.
    """
    return MagicMock(spec=GlueJobLogger)

@pytest.fixture
def mock_data_quality_checker():
    """
    Create a mock data quality checker.
    """
    return MagicMock(spec=DataQualityChecker)

def test_process_service_data(spark, sample_data, mock_logger, mock_data_quality_checker):
    """
    Test processing service data.
    """
    # Mock Spark read and write operations
    with patch("pyspark.sql.SparkSession.read") as mock_read, \
         patch("pyspark.sql.DataFrame.write") as mock_write, \
         patch("awsglue.context.GlueContext.create_dynamic_frame") as mock_create_df:
        
        # Set up mocks
        mock_read.json.return_value = sample_data
        mock_write.return_value = MagicMock()
        mock_create_df.from_catalog.return_value.toDF.return_value.write.mode.return_value.saveAsTable.return_value = None
        
        # Mock transform function
        transform_func = MagicMock(return_value=sample_data)
        
        # Mock data quality checker
        with patch("utils.data_quality.DataQualityChecker") as mock_checker_class:
            mock_checker_class.return_value = mock_data_quality_checker
            mock_data_quality_checker.run_all_checks.return_value = {}
            mock_data_quality_checker.generate_report.return_value = "Test Report"
            
            # Call the function
            process_service_data("ec2", "us-east-1", transform_func)
            
            # Verify calls
            mock_read.json.assert_called_once()
            mock_write.mode.assert_called_once_with("overwrite")
            mock_data_quality_checker.run_all_checks.assert_called_once()
            mock_data_quality_checker.generate_report.assert_called_once()
            mock_logger.log_info.assert_called()

def test_main(spark, mock_logger):
    """
    Test main function.
    """
    # Mock process_service_data
    with patch("main.process_service_data") as mock_process:
        # Mock logger
        with patch("utils.logger.GlueJobLogger") as mock_logger_class:
            mock_logger_class.return_value = mock_logger
            
            # Call main function
            main()
            
            # Verify process_service_data was called for each service and region
            assert mock_process.call_count == 9  # 5 regions * 1 service + 2 global services
            
            # Verify logger methods were called
            mock_logger.start_job.assert_called_once()
            mock_logger.end_job.assert_called_once()

def test_main_error_handling(spark, mock_logger):
    """
    Test error handling in main function.
    """
    # Mock process_service_data to raise an exception
    with patch("main.process_service_data") as mock_process:
        mock_process.side_effect = Exception("Test error")
        
        # Mock logger
        with patch("utils.logger.GlueJobLogger") as mock_logger_class:
            mock_logger_class.return_value = mock_logger
            
            # Call main function and expect exception
            with pytest.raises(Exception):
                main()
            
            # Verify error was logged
            mock_logger.log_error.assert_called_once() 