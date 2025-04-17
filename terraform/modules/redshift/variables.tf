variable "environment" {
  description = "Environment name (dev, test, prod)"
  type        = string
}

variable "redshift_cluster_identifier" {
  description = "Redshift cluster identifier"
  type        = string
}

variable "redshift_database_name" {
  description = "Redshift database name"
  type        = string
}

variable "redshift_master_username" {
  description = "Redshift master username"
  type        = string
}

variable "redshift_master_password" {
  description = "Redshift master password"
  type        = string
  sensitive   = true
}

variable "redshift_node_type" {
  description = "Redshift node type"
  type        = string
  default     = "dc2.large"
}

variable "redshift_number_of_nodes" {
  description = "Number of nodes in Redshift cluster"
  type        = number
  default     = 2
}

variable "vpc_id" {
  description = "VPC ID for Redshift cluster"
  type        = string
}

variable "subnet_ids" {
  description = "List of subnet IDs for Redshift cluster"
  type        = list(string)
}

variable "allowed_cidr_blocks" {
  description = "List of CIDR blocks allowed to access Redshift"
  type        = list(string)
  default     = ["10.0.0.0/16"]
} 