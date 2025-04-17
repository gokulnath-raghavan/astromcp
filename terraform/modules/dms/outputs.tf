output "replication_instance_arn" {
  description = "ARN of the DMS replication instance"
  value       = aws_dms_replication_instance.main.replication_instance_arn
}

output "replication_instance_id" {
  description = "ID of the DMS replication instance"
  value       = aws_dms_replication_instance.main.replication_instance_id
}

output "source_endpoint_arn" {
  description = "ARN of the source endpoint"
  value       = aws_dms_endpoint.source.endpoint_arn
}

output "target_endpoint_arn" {
  description = "ARN of the target endpoint"
  value       = aws_dms_endpoint.target.endpoint_arn
}

output "replication_task_arns" {
  description = "Map of replication task names to their ARNs"
  value = {
    for name, task in aws_dms_replication_task.main : name => task.replication_task_arn
  }
}

output "security_group_id" {
  description = "ID of the DMS security group"
  value       = aws_security_group.dms.id
}

output "kms_key_arn" {
  description = "ARN of the KMS key used for DMS encryption"
  value       = aws_kms_key.dms.arn
}

output "kms_key_alias" {
  description = "Alias of the KMS key used for DMS encryption"
  value       = aws_kms_alias.dms.name
} 