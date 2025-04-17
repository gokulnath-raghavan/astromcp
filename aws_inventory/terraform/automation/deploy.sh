#!/bin/bash

# Set environment variables
PROJECT_NAME="aws-inventory"
ENVIRONMENT=${1:-"dev"}
AWS_REGION=${2:-"us-east-1"}

# Create Python package
echo "Creating Python package..."
cd ../src
zip -r ../glue_job.zip .
cd ..

# Upload to S3
echo "Uploading package to S3..."
aws s3 cp glue_job.zip s3://${PROJECT_NAME}-inventory-${ENVIRONMENT}/glue_job.zip

# Create/Update Glue Job
echo "Creating/Updating Glue Job..."
aws glue create-job \
    --name "${PROJECT_NAME}-inventory-collector-${ENVIRONMENT}" \
    --role "arn:aws:iam::$(aws sts get-caller-identity --query Account --output text):role/${PROJECT_NAME}-glue-role-${ENVIRONMENT}" \
    --command "{
        \"Name\": \"pythonshell\",
        \"ScriptLocation\": \"s3://${PROJECT_NAME}-inventory-${ENVIRONMENT}/glue_job.zip\",
        \"PythonVersion\": \"3.9\"
    }" \
    --default-arguments "{
        \"--job-language\": \"python\",
        \"--extra-py-files\": \"s3://${PROJECT_NAME}-inventory-${ENVIRONMENT}/glue_job.zip\",
        \"--enable-metrics\": \"\",
        \"--enable-continuous-cloudwatch-log\": \"true\",
        \"--enable-spark-ui\": \"true\",
        \"--spark-event-logs-path\": \"s3://${PROJECT_NAME}-inventory-${ENVIRONMENT}/spark-logs/\"
    }" \
    --max-retries 0 \
    --timeout 2880 \
    --max-capacity 0.0625 \
    --glue-version "3.0" \
    --number-of-workers 2 \
    --worker-type "G.1X"

# Create/Update Glue Trigger
echo "Creating/Updating Glue Trigger..."
aws glue create-trigger \
    --name "${PROJECT_NAME}-inventory-trigger-${ENVIRONMENT}" \
    --type "SCHEDULED" \
    --schedule "cron(0 12 * * ? *)" \
    --actions "JobName=${PROJECT_NAME}-inventory-collector-${ENVIRONMENT}" \
    --start-on-creation

echo "Deployment completed successfully!" 