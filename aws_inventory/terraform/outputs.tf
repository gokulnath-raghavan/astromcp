output "s3_bucket_name" {
  description = "Name of the S3 bucket for inventory data"
  value       = module.inventory.s3_bucket_name
}

output "glue_database_name" {
  description = "Name of the Glue database"
  value       = module.inventory.glue_database_name
}

output "glue_job_name" {
  description = "Name of the Glue job"
  value       = module.inventory.glue_job_name
}

output "glue_crawler_name" {
  description = "Name of the Glue crawler"
  value       = module.inventory.glue_crawler_name
}

output "iam_role_arn" {
  description = "ARN of the IAM role for Glue job"
  value       = module.inventory.iam_role_arn
} 