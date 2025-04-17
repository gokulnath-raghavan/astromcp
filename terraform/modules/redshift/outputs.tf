output "cluster_endpoint" {
  description = "Redshift cluster endpoint"
  value       = aws_redshift_cluster.main.endpoint
}

output "cluster_id" {
  description = "Redshift cluster ID"
  value       = aws_redshift_cluster.main.id
}

output "cluster_arn" {
  description = "Redshift cluster ARN"
  value       = aws_redshift_cluster.main.arn
}

output "security_group_id" {
  description = "Redshift security group ID"
  value       = aws_security_group.redshift.id
}

output "subnet_group_name" {
  description = "Redshift subnet group name"
  value       = aws_redshift_subnet_group.main.name
}

output "logs_bucket_name" {
  description = "S3 bucket name for Redshift logs"
  value       = aws_s3_bucket.logs.bucket
} 