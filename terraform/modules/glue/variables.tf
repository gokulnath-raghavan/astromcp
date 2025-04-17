variable "environment" {
  description = "Environment name (dev, test, prod)"
  type        = string
}

variable "glue_job_scripts" {
  description = "Map of Glue job names to their script locations"
  type = map(object({
    script_path = string
    role_arn    = string
    timeout     = number
  }))
}

variable "glue_version" {
  description = "Glue version"
  type        = string
  default     = "3.0"
}

variable "worker_type" {
  description = "Glue worker type"
  type        = string
  default     = "G.1X"
}

variable "number_of_workers" {
  description = "Number of workers for Glue jobs"
  type        = number
  default     = 2
} 