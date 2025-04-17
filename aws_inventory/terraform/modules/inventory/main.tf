resource "aws_s3_bucket" "inventory" {
  bucket = "${var.project_name}-inventory-${var.environment}"
  acl    = "private"

  versioning {
    enabled = true
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  tags = {
    Name        = "${var.project_name}-inventory-${var.environment}"
    Environment = var.environment
    Project     = var.project_name
  }
}

resource "aws_glue_catalog_database" "inventory" {
  name = "${var.project_name}_inventory_${var.environment}"
}

resource "aws_iam_role" "glue" {
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

resource "aws_iam_role_policy" "glue" {
  name = "${var.project_name}-glue-policy-${var.environment}"
  role = aws_iam_role.glue.id

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
          aws_s3_bucket.inventory.arn,
          "${aws_s3_bucket.inventory.arn}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "glue:*",
          "cloudwatch:PutMetricData"
        ]
        Resource = "*"
      }
    ]
  })
}

resource "aws_glue_job" "inventory" {
  name         = "${var.project_name}-inventory-collector-${var.environment}"
  role_arn     = aws_iam_role.glue.arn
  glue_version = "3.0"

  command {
    script_location = "s3://${aws_s3_bucket.inventory.bucket}/glue_job.zip"
    python_version  = "3.9"
  }

  default_arguments = {
    "--job-language"                   = "python"
    "--extra-py-files"                 = "s3://${aws_s3_bucket.inventory.bucket}/glue_job.zip"
    "--enable-metrics"                 = ""
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-spark-ui"                = "true"
    "--spark-event-logs-path"          = "s3://${aws_s3_bucket.inventory.bucket}/spark-logs/"
  }

  max_retries     = 0
  timeout         = var.glue_job_timeout
  max_capacity    = 0.0625
  number_of_workers = var.glue_job_workers
  worker_type     = var.glue_job_worker_type
}

resource "aws_glue_trigger" "inventory" {
  name          = "${var.project_name}-inventory-trigger-${var.environment}"
  type          = "SCHEDULED"
  schedule      = var.inventory_schedule
  start_on_creation = true

  actions {
    job_name = aws_glue_job.inventory.name
  }
}

resource "aws_glue_crawler" "inventory" {
  name          = "${var.project_name}-inventory-crawler-${var.environment}"
  role          = aws_iam_role.glue.arn
  database_name = aws_glue_catalog_database.inventory.name
  schedule      = var.inventory_schedule

  s3_target {
    path = "s3://${aws_s3_bucket.inventory.bucket}/inventory/"
  }
} 