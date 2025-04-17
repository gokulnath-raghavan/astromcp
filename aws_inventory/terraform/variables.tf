variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "aws-inventory"
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "inventory_schedule" {
  description = "Schedule for inventory collection (cron expression)"
  type        = string
  default     = "cron(0 12 * * ? *)"
}

variable "glue_job_timeout" {
  description = "Timeout for Glue job in minutes"
  type        = number
  default     = 2880
}

variable "glue_job_workers" {
  description = "Number of workers for Glue job"
  type        = number
  default     = 2
}

variable "glue_job_worker_type" {
  description = "Worker type for Glue job"
  type        = string
  default     = "G.1X"
}

variable "tags" {
  description = "Tags to apply to all resources"
  type        = map(string)
  default = {
    Project     = "aws-inventory"
    Environment = "dev"
    ManagedBy   = "terraform"
  }
} 