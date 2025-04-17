## About The Project

In order to use AWS ECR docker images with OpenID Connect, you will need to configure Pipelines as a Web Identity Provider, create an IAM role, and associate the IAM role with build image. <br/><br/>
This project aims to create the following components using Terraform scripts:

- Establish a Web Identity OpenID Connect (OIDC) provider to enable Bitbucket pipelines to access AWS ECR for retrieving Docker images.
- Set up an Elastic Container Registry (ECR) repository.
- Create IAM policies and roles for enabling Federated access to the Web Identity Provider and ECR access.
- Build Docker images and push them into the ECR repository.

For more info: [Use AWS ECR images in Pipelines with OpenID Connect](https://support.atlassian.com/bitbucket-cloud/docs/use-aws-ecr-images-in-pipelines-with-openid-connect/)

### Prerequisites for Automatic deployment

  1. Navigate to your repository's settings.
  2. Under the "Deployments" section, update the existing setup to include the following environments:
    - Development
    - Test
    - Production
  3. For each environment (Development, Test, Production), add the following environment variables:
    - AWS_ACCESS_KEY_ID
    - AWS_SECRET_ACCESS_KEY
    - AWS_REGION
    
  Make sure to replace these variables with the actual values required for your AWS setup. 

### Prerequisites for Manual deployment 

Before proceeding with this project, ensure that you have the following software installed on your local machine:

- [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- [Docker Desktop](https://docs.docker.com/desktop/)

Make sure to have these prerequisites installed and configured to facilitate a smooth project setup.

## Manual Deployment

To get started with this project, follow these steps:

1. Clone this repository to your local machine:
   ```sh
   git clone git@bitbucket.org:usp/usp_ecr.git
   ```
2. Navigate to the project directory:
   ```sh
   cd usp_ecr
   ```
3. Configure your AWS credentials using the AWS CLI. This is essential for Terraform to interact with your AWS account.
4. Customize Terraform scripts as needed. Update variables, resources, and configurations to match your project's requirements:
    - env/ecr.tfvars
    - env/dev.conf
    - env/test.conf
    - env/prod.conf
5. Initialize Terraform environment:
   ```sh
   terraform init -backend-config=env/dev.conf
   ```
6. Switch workspace
   ```sh
   terraform workspace select dev || terraform workspace new dev
   ```
6. Create execution plan
   ```sh
   terraform plan
   ```
7. Apply the Terraform configuration to create and manage your AWS resources:
   ```sh
   terraform apply -auto-approve -var-file=env/ecr.tfvars
   ```
## Project Structure

 The project directory is organized as follows:

- main.tf: The main Terraform script that defines AWS resources.
- config.tf: backend S3 bucket and AWS region configuration
- variables.tf: Variables used to parameterize Terraform configuration.
- outputs.tf: Outputs that provide information about the created resources.
- terraform.tfstate: The state file that tracks the current state of your infrastructure.
- README.md: This README file.
- env/ecr.tfvars: Bitbucket workspace name and workspace UUID variables for OpenID Connect
- image/Dockerfile: Docker image to use in bitbucket pipelines
- modules/docker-build: Docker build module to build and push docker image into ECR repository

## Example of Usage in Bitbucket Pipelines
```
    ...
    - step:
        name: Deploy to Development
        image:
          name: 999999999999.dkr.ecr.us-east-1.amazonaws.com/bitbucket-runner:latest
          aws:
            oidc-role: arn:aws:iam::999999999999:role/usp-ecr-access-role
        oidc: true
        deployment: Development
        trigger: manual
        script:
          ...
```

## Feedback
If you encounter issues, have questions, or want to provide feedback, please open an issue on this repository.
