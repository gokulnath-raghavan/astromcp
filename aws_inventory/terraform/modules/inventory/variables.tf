variable "project_name" {
  description = "Name of the project"
  type        = string
}

variable "environment" {
  description = "Environment (dev, staging, prod)"
  type        = string
}

variable "aws_region" {
  description = "AWS region"
  type        = string
}

variable "inventory_schedule" {
  description = "Schedule for inventory collection (cron expression)"
  type        = string
}

variable "glue_job_timeout" {
  description = "Timeout for Glue job in minutes"
  type        = number
}

variable "glue_job_workers" {
  description = "Number of workers for Glue job"
  type        = number
}

variable "glue_job_worker_type" {
  description = "Worker type for Glue job"
  type        = string
} 