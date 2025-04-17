# AWS Inventory Management System

A comprehensive system for collecting and managing inventory of AWS resources across multiple accounts and regions.

## Features

- Multi-account and multi-region support
- Automated inventory collection
- Infrastructure as Code (Terraform)
- CI/CD pipeline integration
- Comprehensive documentation
- Automated testing

## Supported AWS Services

- EC2 Instances
- S3 Buckets
- RDS Databases
- Lambda Functions
- IAM Resources
- And more...

## Getting Started

### Prerequisites

- Python 3.9+
- Terraform 1.0.0+
- AWS CLI
- Git

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd aws_inventory
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure AWS credentials:
```bash
aws configure
```

4. Deploy infrastructure:
```bash
cd terraform
terraform init
terraform plan
terraform apply
```

## Development

### Local Development

1. Create a feature branch:
```bash
git checkout -b feature/new-feature
```

2. Make changes and test:
```bash
./scripts/deploy.sh dev
```

3. Create a pull request

### Testing

Run the test suite:
```bash
pytest test/
```

## Deployment

### Development Environment

```bash
./scripts/deploy.sh dev
```

### Production Environment

```bash
./scripts/deploy.sh prod
```

## Documentation

- [Architecture](docs/architecture/)
- [Setup Guide](docs/setup/)
- [API Documentation](docs/api/)

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 