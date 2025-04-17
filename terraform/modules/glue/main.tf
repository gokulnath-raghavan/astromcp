resource "aws_glue_job" "main" {
  for_each = var.glue_job_scripts

  name              = each.key
  role_arn          = each.value.role_arn
  glue_version      = "3.0"
  worker_type       = "G.1X"
  number_of_workers = 2
  timeout           = each.value.timeout

  command {
    script_location = each.value.script_path
    python_version  = "3"
  }

  default_arguments = {
    "--job-language"            = "python"
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-metrics"          = "true"
    "--enable-spark-ui"         = "true"
    "--spark-event-logs-path"   = "s3://${aws_s3_bucket.glue_logs.bucket}/spark-logs/"
    "--TempDir"                 = "s3://${aws_s3_bucket.glue_logs.bucket}/temp/"
  }

  tags = {
    Environment = var.environment
    Name        = each.key
  }
}

resource "aws_s3_bucket" "glue_logs" {
  bucket = "${var.environment}-glue-logs"
  
  tags = {
    Environment = var.environment
    Name        = "${var.environment}-glue-logs"
  }
}

resource "aws_s3_bucket_versioning" "glue_logs" {
  bucket = aws_s3_bucket.glue_logs.id
  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "glue_logs" {
  bucket = aws_s3_bucket.glue_logs.id
  
  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_iam_role" "glue_service" {
  name = "${var.environment}-glue-service-role"

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

resource "aws_iam_role_policy_attachment" "glue_service" {
  role       = aws_iam_role.glue_service.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSGlueServiceRole"
}

resource "aws_iam_role_policy" "glue_s3" {
  name = "${var.environment}-glue-s3-policy"
  role = aws_iam_role.glue_service.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:ListBucket"
        ]
        Resource = [
          "arn:aws:s3:::${aws_s3_bucket.glue_logs.bucket}",
          "arn:aws:s3:::${aws_s3_bucket.glue_logs.bucket}/*"
        ]
      }
    ]
  })
} 