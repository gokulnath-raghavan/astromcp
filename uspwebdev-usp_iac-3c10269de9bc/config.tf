terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "3.75.1"
    }

    #databricks = {
    #  source  = "databrickslabs/databricks"
    #  version = "0.5.5"
    #}

  }
}

provider "aws" {
  region = "us-east-1"
}

#Placeholder for databricks 
#provider "databricks" {
#  alias      = "mws"
#  host       = "https://accounts.cloud.databricks.com"
#  username   = var.databricks_account_username
#  password   = var.databricks_account_password
#  account_id = var.databricks_account_id
#}

terraform {
  backend "s3" {
    bucket  = "usp-terraform-state-us-east-1-574445142477"
    key     = "usp/iac/state"
    region  = "us-east-1"
    encrypt = "true"
  }
}

data "terraform_remote_state" "dev_workspace" {
  backend = "s3"
  config = {
    bucket  = "usp-terraform-state-us-east-1-574445142477"
    key    = "env://dev/usp/iac/state"
    region = "us-east-1"
  }
}

data "terraform_remote_state" "test_workspace" {
  backend = "s3"
  config = {
    bucket  = "usp-terraform-state-us-east-1-574445142477"
    key    = "env://test/usp/iac/state"
    region = "us-east-1"
  }
}

data "terraform_remote_state" "prod_workspace" {
  backend = "s3"
  config = {
    bucket  = "usp-terraform-state-us-east-1-574445142477"
    key    = "env://prod/usp/iac/state"
    region = "us-east-1"
  }
}
