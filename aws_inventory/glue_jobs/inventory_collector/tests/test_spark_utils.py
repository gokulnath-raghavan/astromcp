import pytest
from unittest.mock import Mock, patch
from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.types import StructType, StructField, StringType, IntegerType
from utils.spark_utils import SparkJobManager

@pytest.fixture
def spark():
    """Create a SparkSession for testing"""
    return SparkSession.builder \
        .appName("test") \
        .master("local[2]") \
        .getOrCreate()

@pytest.fixture
def logger():
    """Create a mock logger"""
    return Mock()

@pytest.fixture
def spark_manager(spark, logger):
    """Create a SparkJobManager instance"""
    return SparkJobManager(
        spark=spark,
        logger=logger,
        s3_bucket="test-bucket",
        glue_database="test_db"
    )

@pytest.fixture
def sample_data(spark):
    """Create a sample DataFrame"""
    data = [("1", "test1"), ("2", "test2")]
    schema = StructType([
        StructField("id", StringType(), True),
        StructField("name", StringType(), True)
    ])
    return spark.createDataFrame(data, schema)

def test_read_json_from_s3(spark_manager, spark):
    """Test reading JSON data from S3"""
    with patch.object(spark, "read") as mock_read:
        mock_read.json.return_value = Mock(spec=DataFrame)
        df = spark_manager.read_json_from_s3("test/path")
        assert isinstance(df, DataFrame)
        mock_read.json.assert_called_once()

def test_write_to_s3(spark_manager, sample_data):
    """Test writing DataFrame to S3"""
    with patch.object(sample_data, "write") as mock_write:
        mock_format = Mock()
        mock_write.format.return_value = mock_format
        mock_format.mode.return_value = mock_format
        mock_format.partitionBy.return_value = mock_format
        mock_format.save.return_value = None
        
        spark_manager.write_to_s3(
            sample_data,
            "test/path",
            partition_by=["id"]
        )
        
        mock_write.format.assert_called_once_with("parquet")
        mock_format.mode.assert_called_once_with("overwrite")
        mock_format.partitionBy.assert_called_once_with("id")
        mock_format.save.assert_called_once()

def test_create_glue_table(spark_manager, sample_data, spark):
    """Test creating Glue table"""
    with patch.object(spark, "sql") as mock_sql:
        spark_manager.create_glue_table(
            sample_data,
            "test_table",
            "test/path",
            partition_by=["id"]
        )
        
        assert mock_sql.call_count == 2
        mock_sql.assert_any_call("CREATE DATABASE IF NOT EXISTS test_db")
        assert "CREATE TABLE" in mock_sql.call_args[0][0]

def test_add_metadata_columns(spark_manager, sample_data):
    """Test adding metadata columns"""
    df = spark_manager.add_metadata_columns(
        sample_data,
        "test_job",
        "us-east-1"
    )
    
    assert "job_name" in df.columns
    assert "region" in df.columns
    assert "processing_time" in df.columns
    assert "processing_date" in df.columns

def test_optimize_spark_config(spark_manager, spark):
    """Test optimizing Spark configuration"""
    config = {
        "spark.sql.shuffle.partitions": "200",
        "spark.default.parallelism": "200"
    }
    
    spark_manager.optimize_spark_config(config)
    
    assert spark.conf.get("spark.sql.shuffle.partitions") == "200"
    assert spark.conf.get("spark.default.parallelism") == "200"

def test_cache_dataframe(spark_manager, sample_data):
    """Test caching DataFrame"""
    with patch.object(sample_data, "cache") as mock_cache:
        with patch.object(sample_data, "count") as mock_count:
            spark_manager.cache_dataframe(sample_data, "test_df")
            mock_cache.assert_called_once()
            mock_count.assert_called_once()

def test_uncache_dataframe(spark_manager, sample_data):
    """Test uncaching DataFrame"""
    with patch.object(sample_data, "unpersist") as mock_unpersist:
        spark_manager.uncache_dataframe(sample_data, "test_df")
        mock_unpersist.assert_called_once()

def test_validate_schema(spark_manager, sample_data):
    """Test validating DataFrame schema"""
    required_columns = ["id", "name"]
    schema = StructType([
        StructField("id", StringType(), True),
        StructField("name", StringType(), True)
    ])
    
    assert spark_manager.validate_schema(
        sample_data,
        required_columns,
        schema
    )

def test_validate_schema_missing_columns(spark_manager, sample_data):
    """Test validating DataFrame schema with missing columns"""
    required_columns = ["id", "name", "missing"]
    
    assert not spark_manager.validate_schema(
        sample_data,
        required_columns
    )

def test_validate_schema_type_mismatch(spark_manager, sample_data):
    """Test validating DataFrame schema with type mismatch"""
    schema = StructType([
        StructField("id", IntegerType(), True),
        StructField("name", StringType(), True)
    ])
    
    assert not spark_manager.validate_schema(
        sample_data,
        ["id", "name"],
        schema
    )

def test_log_dataframe_stats(spark_manager, sample_data):
    """Test logging DataFrame statistics"""
    with patch.object(sample_data, "count") as mock_count:
        with patch.object(sample_data, "filter") as mock_filter:
            mock_count.return_value = 2
            mock_filter.return_value.count.return_value = 0
            
            spark_manager.log_dataframe_stats(sample_data, "test_df")
            
            mock_count.assert_called_once()
            assert mock_filter.call_count == 2  # One for each column

def test_read_json_from_s3_error(spark_manager, spark):
    """Test error handling when reading JSON from S3"""
    with patch.object(spark, "read") as mock_read:
        mock_read.json.side_effect = Exception("Test error")
        with pytest.raises(Exception):
            spark_manager.read_json_from_s3("test/path")

def test_write_to_s3_error(spark_manager, sample_data):
    """Test error handling when writing to S3"""
    with patch.object(sample_data, "write") as mock_write:
        mock_write.format.side_effect = Exception("Test error")
        with pytest.raises(Exception):
            spark_manager.write_to_s3(sample_data, "test/path")

def test_create_glue_table_error(spark_manager, sample_data, spark):
    """Test error handling when creating Glue table"""
    with patch.object(spark, "sql") as mock_sql:
        mock_sql.side_effect = Exception("Test error")
        with pytest.raises(Exception):
            spark_manager.create_glue_table(
                sample_data,
                "test_table",
                "test/path"
            )

def test_add_metadata_columns_error(spark_manager, sample_data):
    """Test error handling when adding metadata columns"""
    with patch.object(sample_data, "withColumn") as mock_with_column:
        mock_with_column.side_effect = Exception("Test error")
        with pytest.raises(Exception):
            spark_manager.add_metadata_columns(
                sample_data,
                "test_job",
                "us-east-1"
            )

def test_optimize_spark_config_error(spark_manager, spark):
    """Test error handling when optimizing Spark configuration"""
    with patch.object(spark, "conf") as mock_conf:
        mock_conf.set.side_effect = Exception("Test error")
        with pytest.raises(Exception):
            spark_manager.optimize_spark_config({
                "test.key": "test.value"
            })

def test_cache_dataframe_error(spark_manager, sample_data):
    """Test error handling when caching DataFrame"""
    with patch.object(sample_data, "cache") as mock_cache:
        mock_cache.side_effect = Exception("Test error")
        with pytest.raises(Exception):
            spark_manager.cache_dataframe(sample_data, "test_df")

def test_uncache_dataframe_error(spark_manager, sample_data):
    """Test error handling when uncaching DataFrame"""
    with patch.object(sample_data, "unpersist") as mock_unpersist:
        mock_unpersist.side_effect = Exception("Test error")
        with pytest.raises(Exception):
            spark_manager.uncache_dataframe(sample_data, "test_df")

def test_log_dataframe_stats_error(spark_manager, sample_data):
    """Test error handling when logging DataFrame statistics"""
    with patch.object(sample_data, "count") as mock_count:
        mock_count.side_effect = Exception("Test error")
        with pytest.raises(Exception):
            spark_manager.log_dataframe_stats(sample_data, "test_df") 