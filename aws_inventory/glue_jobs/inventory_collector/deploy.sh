#!/bin/bash

# Exit on error
set -e

# Configuration
REGION="us-east-1"
S3_BUCKET="aws-inventory-data"
GLUE_JOB_NAME="aws-inventory-collector"
GLUE_JOB_DIR="glue_jobs/inventory_collector"
GLUE_JOB_ZIP="glue_job.zip"

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check for required commands
for cmd in aws zip python3; do
    if ! command_exists "$cmd"; then
        echo "Error: $cmd is required but not installed."
        exit 1
    fi
done

# Check AWS credentials
if ! aws sts get-caller-identity >/dev/null 2>&1; then
    echo "Error: AWS credentials not configured."
    exit 1
fi

# Create S3 bucket if it doesn't exist
if ! aws s3 ls "s3://$S3_BUCKET" >/dev/null 2>&1; then
    echo "Creating S3 bucket: $S3_BUCKET"
    aws s3 mb "s3://$S3_BUCKET" --region "$REGION"
fi

# Create directory structure in S3
echo "Creating directory structure in S3..."
aws s3api put-object --bucket "$S3_BUCKET" --key "$GLUE_JOB_DIR/" >/dev/null 2>&1 || true

# Package the Glue job
echo "Packaging Glue job..."
cd "$(dirname "$0")"
zip -r "$GLUE_JOB_ZIP" . -x "*.pyc" "*.pyo" "*.pyd" "*.zip" "*.sh" "*.md" "*.git*" "*.DS_Store" "tests/*" "venv/*" "__pycache__/*"

# Upload the package to S3
echo "Uploading Glue job package to S3..."
aws s3 cp "$GLUE_JOB_ZIP" "s3://$S3_BUCKET/$GLUE_JOB_DIR/$GLUE_JOB_ZIP"

# Clean up local zip file
rm -f "$GLUE_JOB_ZIP"

# Create or update Glue job
echo "Creating/updating Glue job..."
python3 -c "
import boto3
from utils.glue_utils import GlueJobManager
from config.glue_config import (
    GLUE_JOB_CONFIG,
    GLUE_JOB_ARGS,
    GLUE_JOB_SCHEDULE,
    GLUE_SECURITY_CONFIG,
    GLUE_MONITORING_CONFIG,
    GLUE_JOB_TAGS,
    GLUE_JOB_CONNECTIONS,
    GLUE_JOB_CLASSIFIERS,
    GLUE_JOB_PARAMETERS
)

# Update job configuration with S3 bucket
job_config = GLUE_JOB_CONFIG.copy()
job_config['s3_bucket'] = '$S3_BUCKET'
job_config['job_args'] = GLUE_JOB_ARGS
job_config['tags'] = GLUE_JOB_TAGS
job_config['connections'] = GLUE_JOB_CONNECTIONS

# Initialize Glue job manager
glue_manager = GlueJobManager(region='$REGION')

# Create or update job
try:
    glue_manager.create_job(job_config)
    print('Created new Glue job')
except Exception as e:
    if 'already exists' in str(e):
        glue_manager.update_job('$GLUE_JOB_NAME', job_config)
        print('Updated existing Glue job')
    else:
        raise

# Create or update trigger
try:
    glue_manager.create_trigger(GLUE_JOB_SCHEDULE)
    print('Created/updated Glue trigger')
except Exception as e:
    if 'already exists' in str(e):
        print('Trigger already exists')
    else:
        raise
"

echo "Deployment completed successfully!" 