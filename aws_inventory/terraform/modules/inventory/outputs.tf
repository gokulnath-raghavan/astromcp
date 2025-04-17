output "s3_bucket_name" {
  description = "Name of the S3 bucket for inventory data"
  value       = aws_s3_bucket.inventory.bucket
}

output "glue_database_name" {
  description = "Name of the Glue database"
  value       = aws_glue_catalog_database.inventory.name
}

output "glue_job_name" {
  description = "Name of the Glue job"
  value       = aws_glue_job.inventory.name
}

output "glue_crawler_name" {
  description = "Name of the Glue crawler"
  value       = aws_glue_crawler.inventory.name
}

output "iam_role_arn" {
  description = "ARN of the IAM role for Glue job"
  value       = aws_iam_role.glue.arn
} 