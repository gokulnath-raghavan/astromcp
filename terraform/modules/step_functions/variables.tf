variable "environment" {
  description = "Environment name (dev, test, prod)"
  type        = string
}

variable "step_function_definition" {
  description = "Step Function state machine definition"
  type        = string
}

variable "log_retention_days" {
  description = "Number of days to retain CloudWatch logs"
  type        = number
  default     = 30
} 