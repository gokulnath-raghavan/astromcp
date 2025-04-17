from pyspark.sql import DataFrame
from pyspark.sql.functions import *
from datetime import datetime

def transform_ec2_data(raw_df: DataFrame) -> DataFrame:
    """
    Transform raw EC2 inventory data into a structured format.
    
    Args:
        raw_df: Raw inventory DataFrame containing EC2 data
    
    Returns:
        Transformed DataFrame with EC2 instance details
    """
    try:
        # Extract EC2 data from raw inventory
        ec2_df = raw_df.select(
            explode("resources.ec2").alias("ec2_data")
        ).select(
            "ec2_data.InstanceId",
            "ec2_data.InstanceType",
            "ec2_data.State",
            "ec2_data.Tags",
            "ec2_data.LaunchTime",
            "ec2_data.VpcId",
            "ec2_data.SubnetId",
            "ec2_data.Platform",
            "ec2_data.Architecture",
            "ec2_data.RootDeviceType",
            "ec2_data.PublicIpAddress",
            "ec2_data.PrivateIpAddress",
            "ec2_data.SecurityGroups",
            "ec2_data.IamInstanceProfile"
        )
        
        # Add metadata columns
        ec2_df = ec2_df.withColumn(
            "date",
            lit(datetime.now().strftime("%Y-%m-%d"))
        ).withColumn(
            "timestamp",
            lit(datetime.now().isoformat())
        )
        
        # Transform tags into columns
        ec2_df = ec2_df.withColumn(
            "tags",
            transform(
                col("Tags"),
                lambda x: struct(
                    x.getItem("Key").alias("key"),
                    x.getItem("Value").alias("value")
                )
            )
        )
        
        # Transform security groups
        ec2_df = ec2_df.withColumn(
            "security_groups",
            transform(
                col("SecurityGroups"),
                lambda x: struct(
                    x.getItem("GroupId").alias("group_id"),
                    x.getItem("GroupName").alias("group_name")
                )
            )
        )
        
        return ec2_df
        
    except Exception as e:
        raise Exception(f"Error transforming EC2 data: {str(e)}") 