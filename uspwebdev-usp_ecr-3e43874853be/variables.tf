variable "workspace_name" {
  description = "Name of the Bitbucket workspace"
  type = string
}

variable "workspace_uuid" {
  description = "UUID of the Bitbucket workspace"
  type = string
}

variable "aws_region" {
  description = "AWS Region for your environment"
  type = string
  default = "us-east-1"
}

variable "additional_thumbprints" {
  description = "Additional thumbprints"
  type = list(string)
  default = []
}

variable "common_tags" {
  type        = map(string)
  description = "The common tags for any resource"
  default = {
    region     = "us-east-1"
    Owner      = "Usp"
    Managed-By = "Terraform"
  }
}
