# AWS Redshift Data Migration Infrastructure

This repository contains Terraform configurations for setting up AWS infrastructure for data migration to Redshift, including:

- AWS Redshift cluster
- AWS Glue jobs for data transformation
- AWS Step Functions for orchestration
- AWS DMS for one-time historical loads
- Control tables in Redshift for dependency management

## Architecture

The infrastructure is designed to support a multi-layer data pipeline:

1. **Raw Layer**: Initial data ingestion
2. **Normalize Layer**: Data standardization
3. **Stage Layer**: Data preparation
4. **Intermediate Layer**: Data transformation
5. **Dimension/Fact Layer**: Final data model

## Prerequisites

- Terraform >= 1.0.0
- AWS CLI configured with appropriate credentials
- Access to an AWS account with necessary permissions
- Git for version control

## Directory Structure

```
.
├── terraform/
│   ├── modules/
│   │   ├── redshift/      # Redshift cluster configuration
│   │   ├── glue/          # Glue jobs configuration
│   │   ├── step_functions/# Step Functions configuration
│   │   └── dms/           # DMS configuration
│   └── environments/
│       ├── dev/           # Development environment
│       ├── test/          # Testing environment
│       └── prod/          # Production environment
├── bitbucket-pipelines/   # CI/CD pipeline configurations
└── etl_project/          # ETL scripts and configurations
```

## Getting Started

1. Clone the repository:
   ```bash
   git clone https://github.com/gokulnath-raghavan/testing_terraform.git
   cd testing_terraform
   ```

2. Initialize Terraform:
   ```bash
   cd terraform/environments/dev
   terraform init
   ```

3. Review the execution plan:
   ```bash
   terraform plan
   ```

4. Apply the configuration:
   ```bash
   terraform apply
   ```

## Environment Variables

The following environment variables need to be set:

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_DEFAULT_REGION`
- `TF_STATE_BUCKET`
- `DEV_GLUE_SCRIPTS_BUCKET`
- `TEST_GLUE_SCRIPTS_BUCKET`
- `PROD_GLUE_SCRIPTS_BUCKET`

## CI/CD Pipeline

The repository includes Bitbucket pipeline configurations for:

1. Terraform infrastructure deployment
2. Glue script deployment
3. Environment-specific deployments (dev, test, prod)

## Security Considerations

- All sensitive data is stored in AWS Secrets Manager
- IAM roles follow the principle of least privilege
- All resources are tagged for cost tracking
- KMS encryption is enabled for all storage resources

## Contributing

1. Create a feature branch
2. Make your changes
3. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 