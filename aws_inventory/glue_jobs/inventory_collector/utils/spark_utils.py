from pyspark.sql import SparkSession
from pyspark.conf import SparkConf
from typing import Dict, Any, List, Optional, Union
from pyspark.sql.functions import col, lit, current_timestamp, date_format
from pyspark.sql.types import StructType, StructField, StringType, TimestampType

def create_spark_session(app_name: str = "AWSInventoryCollector") -> SparkSession:
    """
    Create and configure a Spark session for Glue jobs.
    
    Args:
        app_name: Name of the Spark application
    
    Returns:
        Configured SparkSession
    """
    conf = SparkConf()
    
    # Set Spark configurations
    conf.set("spark.sql.sources.partitionOverwriteMode", "dynamic")
    conf.set("spark.sql.parquet.compression.codec", "snappy")
    conf.set("spark.sql.parquet.writeLegacyFormat", "true")
    conf.set("spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version", "2")
    
    # Create Spark session
    spark = SparkSession.builder \
        .appName(app_name) \
        .config(conf=conf) \
        .enableHiveSupport() \
        .getOrCreate()
    
    return spark

def optimize_spark_config(spark: SparkSession, config: Dict[str, Any]):
    """
    Optimize Spark configuration based on job requirements.
    
    Args:
        spark: SparkSession instance
        config: Dictionary of configuration parameters
    """
    # Set memory configurations
    spark.conf.set("spark.executor.memory", config.get("executor_memory", "4g"))
    spark.conf.set("spark.driver.memory", config.get("driver_memory", "4g"))
    
    # Set parallelism configurations
    spark.conf.set("spark.default.parallelism", config.get("parallelism", "200"))
    spark.conf.set("spark.sql.shuffle.partitions", config.get("shuffle_partitions", "200"))
    
    # Set dynamic allocation
    spark.conf.set("spark.dynamicAllocation.enabled", "true")
    spark.conf.set("spark.dynamicAllocation.minExecutors", config.get("min_executors", "1"))
    spark.conf.set("spark.dynamicAllocation.maxExecutors", config.get("max_executors", "10"))
    
    # Set other optimizations
    spark.conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer")
    spark.conf.set("spark.sql.adaptive.enabled", "true")
    spark.conf.set("spark.sql.adaptive.coalescePartitions.enabled", "true")

class SparkJobManager:
    """Utility class for managing Spark operations in AWS Glue jobs"""
    
    def __init__(
        self,
        spark: SparkSession,
        logger,
        s3_bucket: str,
        glue_database: str
    ):
        """Initialize the Spark job manager
        
        Args:
            spark: SparkSession instance
            logger: Logger instance
            s3_bucket: S3 bucket name
            glue_database: Glue database name
        """
        self.spark = spark
        self.logger = logger
        self.s3_bucket = s3_bucket
        self.glue_database = glue_database
        
    def read_json_from_s3(
        self,
        path: str,
        schema: Optional[StructType] = None
    ) -> DataFrame:
        """Read JSON data from S3
        
        Args:
            path: S3 path to JSON files
            schema: Optional schema for the data
            
        Returns:
            DataFrame: Spark DataFrame containing the data
        """
        try:
            self.logger.info(f"Reading JSON data from s3://{self.s3_bucket}/{path}")
            df = self.spark.read.json(
                f"s3://{self.s3_bucket}/{path}",
                schema=schema
            )
            return df
        except Exception as e:
            self.logger.error(f"Failed to read JSON data: {e}")
            raise
            
    def write_to_s3(
        self,
        df: DataFrame,
        path: str,
        format: str = "parquet",
        partition_by: Optional[List[str]] = None,
        mode: str = "overwrite"
    ) -> None:
        """Write DataFrame to S3
        
        Args:
            df: DataFrame to write
            path: S3 path to write to
            format: Output format (default: parquet)
            partition_by: List of columns to partition by
            mode: Write mode (default: overwrite)
        """
        try:
            self.logger.info(f"Writing data to s3://{self.s3_bucket}/{path}")
            writer = df.write.format(format).mode(mode)
            if partition_by:
                writer = writer.partitionBy(*partition_by)
            writer.save(f"s3://{self.s3_bucket}/{path}")
        except Exception as e:
            self.logger.error(f"Failed to write data to S3: {e}")
            raise
            
    def create_glue_table(
        self,
        df: DataFrame,
        table_name: str,
        path: str,
        partition_by: Optional[List[str]] = None
    ) -> None:
        """Create or update Glue table
        
        Args:
            df: DataFrame containing the data
            table_name: Name of the Glue table
            path: S3 path where the data is stored
            partition_by: List of columns to partition by
        """
        try:
            self.logger.info(f"Creating/updating Glue table: {table_name}")
            self.spark.sql(f"CREATE DATABASE IF NOT EXISTS {self.glue_database}")
            
            # Create temporary view
            df.createOrReplaceTempView("temp_table")
            
            # Build partition clause
            partition_clause = ""
            if partition_by:
                partition_clause = f"PARTITIONED BY ({', '.join(partition_by)})"
                
            # Create table
            self.spark.sql(f"""
                CREATE TABLE IF NOT EXISTS {self.glue_database}.{table_name}
                USING parquet
                {partition_clause}
                LOCATION 's3://{self.s3_bucket}/{path}'
                AS SELECT * FROM temp_table
            """)
        except Exception as e:
            self.logger.error(f"Failed to create/update Glue table: {e}")
            raise
            
    def add_metadata_columns(
        self,
        df: DataFrame,
        job_name: str,
        region: str
    ) -> DataFrame:
        """Add metadata columns to DataFrame
        
        Args:
            df: Input DataFrame
            job_name: Name of the Glue job
            region: AWS region
            
        Returns:
            DataFrame: DataFrame with metadata columns
        """
        try:
            self.logger.info("Adding metadata columns")
            return df.withColumn("job_name", lit(job_name)) \
                    .withColumn("region", lit(region)) \
                    .withColumn("processing_time", current_timestamp()) \
                    .withColumn("processing_date", date_format(current_timestamp(), "yyyy-MM-dd"))
        except Exception as e:
            self.logger.error(f"Failed to add metadata columns: {e}")
            raise
            
    def optimize_spark_config(self, config: Dict[str, str]) -> None:
        """Optimize Spark configuration
        
        Args:
            config: Dictionary of Spark configuration settings
        """
        try:
            self.logger.info("Optimizing Spark configuration")
            for key, value in config.items():
                self.spark.conf.set(key, value)
        except Exception as e:
            self.logger.error(f"Failed to optimize Spark configuration: {e}")
            raise
            
    def cache_dataframe(self, df: DataFrame, name: str) -> None:
        """Cache DataFrame and log memory usage
        
        Args:
            df: DataFrame to cache
            name: Name of the DataFrame for logging
        """
        try:
            self.logger.info(f"Caching DataFrame: {name}")
            df.cache()
            df.count()  # Force caching
            self.logger.info(f"DataFrame {name} cached successfully")
        except Exception as e:
            self.logger.error(f"Failed to cache DataFrame: {e}")
            raise
            
    def uncache_dataframe(self, df: DataFrame, name: str) -> None:
        """Uncache DataFrame
        
        Args:
            df: DataFrame to uncache
            name: Name of the DataFrame for logging
        """
        try:
            self.logger.info(f"Uncaching DataFrame: {name}")
            df.unpersist()
            self.logger.info(f"DataFrame {name} uncached successfully")
        except Exception as e:
            self.logger.error(f"Failed to uncache DataFrame: {e}")
            raise
            
    def validate_schema(
        self,
        df: DataFrame,
        required_columns: List[str],
        schema: Optional[StructType] = None
    ) -> bool:
        """Validate DataFrame schema
        
        Args:
            df: DataFrame to validate
            required_columns: List of required column names
            schema: Optional expected schema
            
        Returns:
            bool: True if schema is valid, False otherwise
        """
        try:
            self.logger.info("Validating DataFrame schema")
            
            # Check required columns
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                self.logger.error(f"Missing required columns: {missing_columns}")
                return False
                
            # Check schema if provided
            if schema:
                df_schema = df.schema
                for field in schema:
                    if field.name not in df_schema.names:
                        self.logger.error(f"Missing schema field: {field.name}")
                        return False
                    if df_schema[field.name].dataType != field.dataType:
                        self.logger.error(
                            f"Type mismatch for field {field.name}: "
                            f"expected {field.dataType}, got {df_schema[field.name].dataType}"
                        )
                        return False
                        
            return True
        except Exception as e:
            self.logger.error(f"Failed to validate schema: {e}")
            return False
            
    def log_dataframe_stats(self, df: DataFrame, name: str) -> None:
        """Log DataFrame statistics
        
        Args:
            df: DataFrame to analyze
            name: Name of the DataFrame for logging
        """
        try:
            self.logger.info(f"Logging statistics for DataFrame: {name}")
            
            # Basic statistics
            count = df.count()
            self.logger.log_metric(f"{name}_row_count", count)
            
            # Column statistics
            for column in df.columns:
                null_count = df.filter(col(column).isNull()).count()
                self.logger.log_metric(
                    f"{name}_{column}_null_count",
                    null_count
                )
                if null_count > 0:
                    self.logger.warning(
                        f"Column {column} has {null_count} null values "
                        f"({(null_count/count)*100:.2f}%)"
                    )
                    
            # Schema information
            self.logger.info(f"Schema for {name}:")
            for field in df.schema:
                self.logger.info(
                    f"  {field.name}: {field.dataType}"
                )
        except Exception as e:
            self.logger.error(f"Failed to log DataFrame statistics: {e}")
            raise 