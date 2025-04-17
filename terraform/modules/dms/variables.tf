variable "environment" {
  description = "Environment name (dev, test, prod)"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID for DMS replication instance"
  type        = string
}

variable "subnet_ids" {
  description = "List of subnet IDs for DMS replication instance"
  type        = list(string)
}

variable "allowed_cidr_blocks" {
  description = "List of CIDR blocks allowed to access DMS"
  type        = list(string)
  default     = ["10.0.0.0/16"]
}

variable "replication_instance_class" {
  description = "DMS replication instance class"
  type        = string
  default     = "dms.t3.medium"
}

variable "replication_instance_storage" {
  description = "Allocated storage for DMS replication instance in GB"
  type        = number
  default     = 50
}

variable "engine_version" {
  description = "DMS engine version"
  type        = string
  default     = "3.4.6"
}

variable "availability_zone" {
  description = "Availability zone for DMS replication instance"
  type        = string
}

variable "source_endpoint" {
  description = "Source endpoint configuration"
  type = object({
    engine_name   = string
    server_name   = string
    port          = number
    username      = string
    password      = string
    database_name = string
  })
}

variable "target_endpoint" {
  description = "Target endpoint configuration"
  type = object({
    engine_name   = string
    server_name   = string
    port          = number
    username      = string
    password      = string
    database_name = string
  })
}

variable "replication_tasks" {
  description = "Map of replication task configurations"
  type = map(object({
    migration_type = string
    table_mappings = string
  }))
  default = {}
} 