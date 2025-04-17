import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql.functions import *
from transforms.ec2_transformer import transform_ec2_data
from transforms.s3_transformer import transform_s3_data
from transforms.rds_transformer import transform_rds_data
from utils.spark_utils import create_spark_session
from utils.aws_utils import get_aws_regions

# Initialize Spark and Glue contexts
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)

# Get job parameters
args = getResolvedOptions(sys.argv, [
    'JOB_NAME',
    'INPUT_BUCKET',
    'OUTPUT_BUCKET',
    'REGIONS'
])

job.init(args['JOB_NAME'], args)

def main():
    try:
        # Get regions to process
        regions = args['REGIONS'].split(',')
        
        # Process each region
        for region in regions:
            # Read raw inventory data
            raw_data = spark.read.json(f"s3://{args['INPUT_BUCKET']}/inventory/{region}/*.json")
            
            # Transform EC2 data
            ec2_df = transform_ec2_data(raw_data)
            ec2_df.write.mode('overwrite').parquet(
                f"s3://{args['OUTPUT_BUCKET']}/processed/ec2/{region}/"
            )
            
            # Transform S3 data
            s3_df = transform_s3_data(raw_data)
            s3_df.write.mode('overwrite').parquet(
                f"s3://{args['OUTPUT_BUCKET']}/processed/s3/{region}/"
            )
            
            # Transform RDS data
            rds_df = transform_rds_data(raw_data)
            rds_df.write.mode('overwrite').parquet(
                f"s3://{args['OUTPUT_BUCKET']}/processed/rds/{region}/"
            )
            
            # Create Glue tables
            glueContext.getSink(
                path=f"s3://{args['OUTPUT_BUCKET']}/processed/ec2/{region}/",
                connection_type="s3",
                updateBehavior="UPDATE_IN_DATABASE",
                partitionKeys=["date"],
                enableUpdateCatalog=True,
                transformation_ctx="ec2_sink"
            ).writeFrame(ec2_df)
            
            glueContext.getSink(
                path=f"s3://{args['OUTPUT_BUCKET']}/processed/s3/{region}/",
                connection_type="s3",
                updateBehavior="UPDATE_IN_DATABASE",
                partitionKeys=["date"],
                enableUpdateCatalog=True,
                transformation_ctx="s3_sink"
            ).writeFrame(s3_df)
            
            glueContext.getSink(
                path=f"s3://{args['OUTPUT_BUCKET']}/processed/rds/{region}/",
                connection_type="s3",
                updateBehavior="UPDATE_IN_DATABASE",
                partitionKeys=["date"],
                enableUpdateCatalog=True,
                transformation_ctx="rds_sink"
            ).writeFrame(rds_df)
            
    except Exception as e:
        print(f"Error processing inventory: {str(e)}")
        raise e
    finally:
        job.commit()

if __name__ == "__main__":
    main() 