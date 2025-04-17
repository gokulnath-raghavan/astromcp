output "job_arns" {
  description = "Map of Glue job names to their ARNs"
  value = {
    for name, job in aws_glue_job.main : name => job.arn
  }
}

output "glue_service_role_arn" {
  description = "ARN of the Glue service role"
  value       = aws_iam_role.glue_service.arn
}

output "logs_bucket_name" {
  description = "S3 bucket name for Glue logs"
  value       = aws_s3_bucket.glue_logs.bucket
}

output "logs_bucket_arn" {
  description = "S3 bucket ARN for Glue logs"
  value       = aws_s3_bucket.glue_logs.arn
} 