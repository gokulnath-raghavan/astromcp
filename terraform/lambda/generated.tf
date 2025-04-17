# __generated__ by Terraform
# Please review these resources and move them into your main configuration files.

# __generated__ by Terraform
resource "aws_lambda_function" "user_login_business_logic" {
  architectures                      = ["x86_64"]
  code_signing_config_arn            = null
  description                        = null
  filename                           = null
  function_name                      = "usp-edw-dev-user_login_business_logic"
  handler                            = "lambda_function.lambda_handler"
  image_uri                          = null
  kms_key_arn                        = null
  layers                             = []
  memory_size                        = 128
  package_type                       = "Zip"
  publish                            = null
  replace_security_groups_on_destroy = null
  replacement_security_group_ids     = null
  reserved_concurrent_executions     = -1
  role                               = "arn:aws:iam::574445142477:role/usp-edw-userlogin-developer-service-role-dev"
  runtime                            = "python3.13"
  s3_bucket                          = null
  s3_key                             = null
  s3_object_version                  = null
  skip_destroy                       = false
  source_code_hash                   = null
  tags                               = {}
  tags_all                           = {}
  timeout                            = 300
  ephemeral_storage {
    size = 512
  }
  logging_config {
    application_log_level = null
    log_format            = "Text"
    log_group             = "/aws/lambda/usp-edw-dev-user_login_business_logic"
    system_log_level      = null
  }
  tracing_config {
    mode = "PassThrough"
  }
}

# __generated__ by Terraform
resource "aws_lambda_function" "user_login_success_failure_lambda" {
  architectures                      = ["x86_64"]
  code_signing_config_arn            = null
  description                        = null
  filename                           = null
  function_name                      = "usp-edw-dev-user_login_success_failure_lambda"
  handler                            = "lambda_function.lambda_handler"
  image_uri                          = null
  kms_key_arn                        = null
  layers                             = []
  memory_size                        = 128
  package_type                       = "Zip"
  publish                            = null
  replace_security_groups_on_destroy = null
  replacement_security_group_ids     = null
  reserved_concurrent_executions     = -1
  role                               = "arn:aws:iam::574445142477:role/usp-edw-userlogin-developer-service-role-dev"
  runtime                            = "python3.13"
  s3_bucket                          = null
  s3_key                             = null
  s3_object_version                  = null
  skip_destroy                       = false
  source_code_hash                   = null
  tags                               = {}
  tags_all                           = {}
  timeout                            = 600
  ephemeral_storage {
    size = 512
  }
  logging_config {
    application_log_level = null
    log_format            = "Text"
    log_group             = "/aws/lambda/usp-edw-dev-user_login_success_failure_lambda"
    system_log_level      = null
  }
  tracing_config {
    mode = "PassThrough"
  }
}

# __generated__ by Terraform
resource "aws_lambda_function" "user_login_file_validation" {
  architectures                      = ["x86_64"]
  code_signing_config_arn            = null
  description                        = null
  filename                           = null
  function_name                      = "arn:aws:lambda:us-east-1:574445142477:function:usp-edw-dev-user_login_file_validation"
  handler                            = "lambda_function.lambda_handler"
  image_uri                          = null
  kms_key_arn                        = null
  layers                             = []
  memory_size                        = 128
  package_type                       = "Zip"
  publish                            = null
  replace_security_groups_on_destroy = null
  replacement_security_group_ids     = null
  reserved_concurrent_executions     = -1
  role                               = "arn:aws:iam::574445142477:role/usp-edw-userlogin-developer-service-role-dev"
  runtime                            = "python3.13"
  s3_bucket                          = null
  s3_key                             = null
  s3_object_version                  = null
  skip_destroy                       = false
  source_code_hash                   = null
  tags                               = {}
  tags_all                           = {}
  timeout                            = 300
  ephemeral_storage {
    size = 512
  }
  logging_config {
    application_log_level = null
    log_format            = "Text"
    log_group             = "/aws/lambda/usp-edw-dev-user_login_file_validation"
    system_log_level      = null
  }
  tracing_config {
    mode = "PassThrough"
  }
}
