# AWS Inventory Collector Glue Job

This Glue job collects and processes inventory data from various AWS services, including EC2, S3, RDS, Lambda, and IAM. The job is designed to run daily and store the collected data in S3 and Glue tables for analysis.

## Features

- Collects inventory data from multiple AWS services
- Processes and transforms raw data into structured format
- Validates data quality and integrity
- Stores processed data in S3 and Glue tables
- Provides detailed logging and monitoring
- Supports multiple AWS regions
- Automated deployment and configuration

## Prerequisites

- AWS CLI configured with appropriate credentials
- Python 3.8 or later
- Required Python packages (see requirements.txt)
- AWS Glue service role with necessary permissions
- S3 bucket for storing job artifacts and data

## Directory Structure

```
inventory_collector/
├── config/
│   ├── glue_config.py
│   └── data_quality_config.py
├── transforms/
│   ├── ec2_transformer.py
│   ├── s3_transformer.py
│   ├── rds_transformer.py
│   ├── lambda_transformer.py
│   └── iam_transformer.py
├── utils/
│   ├── glue_utils.py
│   ├── spark_utils.py
│   └── logging_utils.py
├── tests/
│   ├── test_glue_config.py
│   ├── test_glue_utils.py
│   ├── test_main.py
│   └── test_data_quality_config.py
├── main.py
├── deploy.sh
├── requirements.txt
└── README.md
```

## Configuration

The job configuration is defined in `config/glue_config.py` and includes:

- Glue job settings (name, description, role, version, etc.)
- Job arguments and parameters
- Schedule configuration
- Security settings
- Monitoring configuration
- Tags and connections

## Deployment

To deploy the Glue job:

1. Make sure you have AWS CLI configured with appropriate credentials
2. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Make the deployment script executable:
   ```bash
   chmod +x deploy.sh
   ```
4. Run the deployment script:
   ```bash
   ./deploy.sh
   ```

The script will:
- Create an S3 bucket if it doesn't exist
- Package the Glue job code and dependencies
- Upload the package to S3
- Create or update the Glue job and trigger

## Testing

To run the tests:

```bash
pytest tests/
```

The tests cover:
- Glue job configuration
- Utility functions
- Data quality checks
- Main job functionality

## Monitoring

The job provides monitoring through:
- CloudWatch logs
- Glue job metrics
- Data quality checks
- Error handling and reporting

## Data Quality

Data quality checks are performed on:
- Required fields
- Data types
- Value ranges
- Null values
- Key columns

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 