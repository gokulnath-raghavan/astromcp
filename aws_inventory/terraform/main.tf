terraform {
  required_version = ">= 1.0.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
  backend "s3" {
    bucket         = "aws-inventory-terraform-state"
    key            = "terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "aws-inventory-terraform-locks"
  }
}

provider "aws" {
  region = var.aws_region
}

# S3 Bucket for storing inventory data
resource "aws_s3_bucket" "inventory_bucket" {
  bucket = "${var.project_name}-inventory-${var.environment}"
  
  tags = {
    Name        = "${var.project_name}-inventory-${var.environment}"
    Environment = var.environment
    Project     = var.project_name
  }
}

# Glue Database for inventory data
resource "aws_glue_catalog_database" "inventory_db" {
  name = "${var.project_name}_inventory_${var.environment}"
}

# Glue Crawler for inventory data
resource "aws_glue_crawler" "inventory_crawler" {
  name          = "${var.project_name}-inventory-crawler-${var.environment}"
  database_name = aws_glue_catalog_database.inventory_db.name
  role          = aws_iam_role.glue_role.arn
  schedule      = "cron(0 12 * * ? *)"  # Run daily at 12:00 UTC

  s3_target {
    path = "s3://${aws_s3_bucket.inventory_bucket.bucket}/raw/"
  }
}

# IAM Role for Glue
resource "aws_iam_role" "glue_role" {
  name = "${var.project_name}-glue-role-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "glue.amazonaws.com"
        }
      }
    ]
  })
}

# IAM Policy for Glue Role
resource "aws_iam_role_policy" "glue_policy" {
  name = "${var.project_name}-glue-policy-${var.environment}"
  role = aws_iam_role.glue_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:ListBucket"
        ]
        Resource = [
          aws_s3_bucket.inventory_bucket.arn,
          "${aws_s3_bucket.inventory_bucket.arn}/*"
        ]
      }
    ]
  })
}

module "inventory" {
  source = "./modules/inventory"

  project_name = var.project_name
  environment  = var.environment
  aws_region   = var.aws_region
} 