# __generated__ by Terraform
# Please review these resources and move them into your main configuration files.

# __generated__ by Terraform
resource "aws_glue_job" "glue-intermediate-dw" {
  connections = ["USP-EDW-GLUE-REDSHIFT-DW-TEST", "USP-EDW-GLUE-REDSHIFT-STG-TEST", "USP-EDW-GLUE-REDSHIFT-STG-DEV"]
  default_arguments = {
    "--TempDir"                   = "s3://aws-glue-assets-574445142477-us-east-1/temporary/"
    "--additional-python-modules" = "redshift-connector"
    "--conf"                      = "spark.sql.parquet.int96RebaseModeInWrite=LEGACY"
    "--config_names"              = "s3://edw-usp-raw-dev/parameter/intermediate-dw/EBS/gl_je_f/USP-EDW-GLUE-GL_JE_F-INC-LOAD-INTERMEDIATE-DW-CONFIG.json"
    "--enable-auto-scaling"       = "true"
    "--enable-glue-datacatalog"   = "true"
    "--enable-job-insights"       = "true"
    "--enable-metrics"            = "true"
    "--env"                       = "env"
    "--extra-py-files"            = "s3://edw-usp-raw-dev/scripts/usp-edw-glue-framework.zip"
    "--job-bookmark-option"       = "job-bookmark-disable"
    "--job-language"              = "python"
    "--master_path"               = "s3://edw-usp-raw-dev/parameter/master/USP-EDW-GLUE-EBS-MASTER-PARAMETER.json"
    "--spark-event-logs-path"     = "s3://aws-glue-assets-574445142477-us-east-1/sparkHistoryLogs/"
  }
  description               = "usp-edw-glue-intermediate-dw job for loading data from Redshift intermediate table to final Redshift dw - dimension & fact tables"
  execution_class           = "STANDARD"
  glue_version              = jsonencode(4)
  job_run_queuing_enabled   = false
  maintenance_window        = null
  max_capacity              = 10
  max_retries               = 0
  name                      = "usp-edw-glue-intermediate-dw"
  non_overridable_arguments = {}
  number_of_workers         = 5
  role_arn                  = "arn:aws:iam::574445142477:role/edw-glue-service-role-dev"
  security_configuration    = null
  tags                      = {}
  tags_all                  = {}
  timeout                   = 2880
  worker_type               = "G.2X"
  command {
    name            = "glueetl"
    python_version  = jsonencode(3)
    runtime         = null
    script_location = "s3://aws-glue-assets-574445142477-us-east-1/scripts/usp-edw-glue-intermediate-dw.py"
  }
  execution_property {
    max_concurrent_runs = 20
  }
}

# __generated__ by Terraform
resource "aws_glue_job" "glue-source-dw" {
  connections = ["USP-EDW-GLUE-ORACLE-EBS-DEV", "USP-EDW-GLUE-ORACLE-EDW-DEV"]
  default_arguments = {
    "--TempDir"                   = "s3://aws-glue-assets-574445142477-us-east-1/temporary/"
    "--additional-python-modules" = "redshift-connector"
    "--conf"                      = "spark.sql.parquet.int96RebaseModeInWrite=LEGACY"
    "--config_names"              = "s3://edw-usp-raw-dev/parameter/source-dw/BIP/USP-EDW-GLUE-GL_JE_SOURCES-FULL-LOAD-SOURCE2DW-CONFIG.json"
    "--enable-auto-scaling"       = "true"
    "--enable-glue-datacatalog"   = "true"
    "--enable-job-insights"       = "true"
    "--enable-metrics"            = "true"
    "--env"                       = "env"
    "--extra-py-files"            = "s3://edw-usp-raw-dev/scripts/usp-edw-glue-framework.zip"
    "--job-bookmark-option"       = "job-bookmark-disable"
    "--job-language"              = "python"
    "--master_path"               = "s3://edw-usp-raw-dev/parameter/master/USP-EDW-GLUE-EBS-MASTER-PARAMETER.json"
    "--spark-event-logs-path"     = "s3://aws-glue-assets-574445142477-us-east-1/sparkHistoryLogs/"
  }
  description               = "usp-edw-glue-source-raw for reading incremental data from source and write to s3 raw"
  execution_class           = "STANDARD"
  glue_version              = jsonencode(4)
  job_run_queuing_enabled   = false
  maintenance_window        = null
  max_capacity              = 10
  max_retries               = 0
  name                      = "usp-edw-glue-source-dw"
  non_overridable_arguments = {}
  number_of_workers         = 5
  role_arn                  = "arn:aws:iam::574445142477:role/edw-glue-service-role-dev"
  security_configuration    = null
  tags                      = {}
  tags_all                  = {}
  timeout                   = 2880
  worker_type               = "G.2X"
  command {
    name            = "glueetl"
    python_version  = jsonencode(3)
    runtime         = null
    script_location = "s3://aws-glue-assets-574445142477-us-east-1/scripts/usp-edw-glue-source-dw.py"
  }
  execution_property {
    max_concurrent_runs = 20
  }
}

# __generated__ by Terraform
resource "aws_glue_job" "glue-normalized-stg" {
  connections = ["USP-EDW-GLUE-ORACLE-EBS-TEST", "USP-EDW-GLUE-ORACLE-EDW-TEST", "USP-EDW-GLUE-REDSHIFT-DW-TEST", "USP-EDW-GLUE-REDSHIFT-STG-DEV", "USP-EDW-GLUE-REDSHIFT-USERLOGIN-DEV"]
  default_arguments = {
    "--TempDir"                   = "s3://aws-glue-assets-574445142477-us-east-1/temporary/"
    "--additional-python-modules" = "redshift-connector"
    "--conf"                      = "spark.sql.parquet.int96RebaseModeInWrite=LEGACY"
    "--config_names"              = "s3://edw-usp-raw-dev/parameter/source-dw/test stg and dim bulk/USP-EDW-GLUE-PA-TEST-INC-LOAD-NORMALIZED-STAGE-CONFIG.json"
    "--enable-auto-scaling"       = "true"
    "--enable-glue-datacatalog"   = "true"
    "--enable-job-insights"       = "true"
    "--enable-metrics"            = "true"
    "--env"                       = "env"
    "--extra-py-files"            = "s3://edw-usp-raw-dev/scripts/usp-edw-glue-framework.zip"
    "--job-bookmark-option"       = "job-bookmark-disable"
    "--job-language"              = "python"
    "--master_path"               = "s3://edw-usp-raw-dev/parameter/master/USP-EDW-GLUE-EBS-MASTER-PARAMETER.json"
    "--spark-event-logs-path"     = "s3://aws-glue-assets-574445142477-us-east-1/sparkHistoryLogs/"
  }
  description               = "usp-edw-glue-normalized-stg job for loading incremental data from s3 normalizer layer to Redshift Stage tables"
  execution_class           = "STANDARD"
  glue_version              = jsonencode(4)
  job_run_queuing_enabled   = false
  maintenance_window        = null
  max_capacity              = 10
  max_retries               = 0
  name                      = "usp-edw-glue-normalized-stg"
  non_overridable_arguments = {}
  number_of_workers         = 5
  role_arn                  = "arn:aws:iam::574445142477:role/edw-glue-service-role-dev"
  security_configuration    = null
  tags                      = {}
  tags_all                  = {}
  timeout                   = 2880
  worker_type               = "G.2X"
  command {
    name            = "glueetl"
    python_version  = jsonencode(3)
    runtime         = null
    script_location = "s3://aws-glue-assets-574445142477-us-east-1/scripts/usp-edw-glue-normalized-stg.py"
  }
  execution_property {
    max_concurrent_runs = 20
  }
}

# __generated__ by Terraform
resource "aws_glue_job" "glue-stg-intermediate" {
  connections = ["USP-EDW-GLUE-REDSHIFT-STG-TEST"]
  default_arguments = {
    "--TempDir"                   = "s3://aws-glue-assets-574445142477-us-east-1/temporary/"
    "--additional-python-modules" = "redshift-connector"
    "--conf"                      = "spark.sql.parquet.int96RebaseModeInWrite=LEGACY"
    "--config_names"              = "s3://edw-usp-raw-dev/parameter/stage-intermediate/EBS/abc_class_d/USP-EDW-GLUE-ABC_CLASS-D99-INC-LOAD-STG-INTERMEDIATE-CONFIG.json"
    "--enable-auto-scaling"       = "true"
    "--enable-glue-datacatalog"   = "true"
    "--enable-job-insights"       = "true"
    "--enable-metrics"            = "true"
    "--env"                       = "env"
    "--extra-py-files"            = "s3://edw-usp-raw-dev/scripts/usp-edw-glue-framework.zip"
    "--job-bookmark-option"       = "job-bookmark-disable"
    "--job-language"              = "python"
    "--master_path"               = "s3://edw-usp-raw-dev/parameter/master/USP-EDW-GLUE-EBS-MASTER-PARAMETER.json"
    "--spark-event-logs-path"     = "s3://aws-glue-assets-574445142477-us-east-1/sparkHistoryLogs/"
  }
  description               = "usp-edw-glue-stg-intermediate job for loading incremental data from Redshift stage table to Redshift Intermediate tables"
  execution_class           = "STANDARD"
  glue_version              = jsonencode(4)
  job_run_queuing_enabled   = false
  maintenance_window        = null
  max_capacity              = 10
  max_retries               = 0
  name                      = "usp-edw-glue-stg-intermediate"
  non_overridable_arguments = {}
  number_of_workers         = 5
  role_arn                  = "arn:aws:iam::574445142477:role/edw-glue-service-role-dev"
  security_configuration    = null
  tags                      = {}
  tags_all                  = {}
  timeout                   = 2880
  worker_type               = "G.2X"
  command {
    name            = "glueetl"
    python_version  = jsonencode(3)
    runtime         = null
    script_location = "s3://aws-glue-assets-574445142477-us-east-1/scripts/usp-edw-glue-stg-intermediate.py"
  }
  execution_property {
    max_concurrent_runs = 20
  }
}

# __generated__ by Terraform
resource "aws_glue_job" "glue-source-raw" {
  connections = ["USP-EDW-GLUE-ORACLE-EBS-DEV"]
  default_arguments = {
    "--TempDir"                   = "s3://aws-glue-assets-574445142477-us-east-1/temporary/"
    "--additional-python-modules" = "redshift-connector"
    "--conf"                      = "spark.sql.parquet.int96RebaseModeInWrite=LEGACY"
    "--config_names"              = "s3://edw-usp-raw-dev/parameter/source-dw/test stg and dim bulk/USP-EDW-GLUE-PA-TEST-INC-LOAD-SOURCE-RAW-CONFIG.json"
    "--enable-auto-scaling"       = "true"
    "--enable-glue-datacatalog"   = "true"
    "--enable-job-insights"       = "true"
    "--enable-metrics"            = "true"
    "--env"                       = "env"
    "--extra-py-files"            = "s3://edw-usp-raw-dev/scripts/usp-edw-glue-framework.zip"
    "--job-bookmark-option"       = "job-bookmark-disable"
    "--job-language"              = "python"
    "--master_path"               = "s3://edw-usp-raw-dev/parameter/master/USP-EDW-GLUE-EBS-MASTER-PARAMETER.json"
    "--spark-event-logs-path"     = "s3://aws-glue-assets-574445142477-us-east-1/sparkHistoryLogs/"
  }
  description               = "usp-edw-glue-source-raw for reading incremental data from source and write to s3 raw"
  execution_class           = "STANDARD"
  glue_version              = jsonencode(4)
  job_run_queuing_enabled   = false
  maintenance_window        = null
  max_capacity              = 10
  max_retries               = 0
  name                      = "usp-edw-glue-source-raw"
  non_overridable_arguments = {}
  number_of_workers         = 5
  role_arn                  = "arn:aws:iam::574445142477:role/edw-glue-service-role-dev"
  security_configuration    = null
  tags                      = {}
  tags_all                  = {}
  timeout                   = 2880
  worker_type               = "G.2X"
  command {
    name            = "glueetl"
    python_version  = jsonencode(3)
    runtime         = null
    script_location = "s3://aws-glue-assets-574445142477-us-east-1/scripts/usp-edw-glue-source-raw.py"
  }
  execution_property {
    max_concurrent_runs = 20
  }
}

# __generated__ by Terraform
resource "aws_glue_job" "glue-source-stage-cronjob" {
  connections = ["USP-EDW-GLUE-ORACLE-EBS-DEV"]
  default_arguments = {
    "--TempDir"                          = "s3://aws-glue-assets-574445142477-us-east-1/temporary/"
    "--additional-python-modules"        = "redshift-connector"
    "--conf"                             = "spark.sql.parquet.int96RebaseModeInWrite=LEGACY"
    "--config_names"                     = "s3://edw-usp-raw-dev/parameter/source-raw/EBS/XLA/USP-EDW-GLUE-XLA-CRON_JOB-INC-LOAD-SOURCE-RAW-CONFIG.json"
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-glue-datacatalog"          = "true"
    "--enable-job-insights"              = "true"
    "--enable-metrics"                   = "true"
    "--enable-spark-ui"                  = "true"
    "--env"                              = "env"
    "--extra-py-files"                   = "s3://edw-usp-raw-dev/scripts/usp-edw-glue-framework.zip"
    "--job-bookmark-option"              = "job-bookmark-disable"
    "--job-language"                     = "python"
    "--master_path"                      = "s3://edw-usp-raw-dev/parameter/master/USP-EDW-GLUE-EBS-MASTER-PARAMETER.json"
    "--spark-event-logs-path"            = "s3://aws-glue-assets-574445142477-us-east-1/sparkHistoryLogs/"
  }
  description               = null
  execution_class           = "STANDARD"
  glue_version              = jsonencode(5)
  job_run_queuing_enabled   = false
  maintenance_window        = null
  max_capacity              = 5
  max_retries               = 0
  name                      = "usp-edw-glue-source-stage-cronjob"
  non_overridable_arguments = {}
  number_of_workers         = 5
  role_arn                  = "arn:aws:iam::574445142477:role/edw-glue-service-role-dev"
  security_configuration    = null
  tags                      = {}
  tags_all                  = {}
  timeout                   = 480
  worker_type               = "G.1X"
  command {
    name            = "glueetl"
    python_version  = jsonencode(3)
    runtime         = null
    script_location = "s3://aws-glue-assets-574445142477-us-east-1/scripts/usp-edw-glue-source-stage-cronjob.py"
  }
  execution_property {
    max_concurrent_runs = 1
  }
}

# __generated__ by Terraform
resource "aws_glue_job" "glue-raw-normalized" {
  connections = ["USP-EDW-GLUE-REDSHIFT-DW-TEST", "USP-EDW-GLUE-REDSHIFT-STG-DEV", "USP-EDW-GLUE-REDSHIFT-STG-TEST"]
  default_arguments = {
    "--TempDir"                   = "s3://aws-glue-assets-574445142477-us-east-1/temporary/"
    "--additional-python-modules" = "redshift-connector"
    "--conf"                      = "spark.sql.parquet.int96RebaseModeInWrite=LEGACY"
    "--config_names"              = "s3://edw-usp-raw-dev/parameter/source-dw/test stg and dim bulk/USP-EDW-GLUE-PA-TEST-INC-LOAD-RAW-NORMALIZED-CONFIG.json"
    "--enable-auto-scaling"       = "true"
    "--enable-glue-datacatalog"   = "true"
    "--enable-job-insights"       = "true"
    "--enable-metrics"            = "true"
    "--env"                       = "env"
    "--extra-py-files"            = "s3://edw-usp-raw-dev/scripts/usp-edw-glue-framework.zip"
    "--job-bookmark-option"       = "job-bookmark-disable"
    "--job-language"              = "python"
    "--master_path"               = "s3://edw-usp-raw-dev/parameter/master/USP-EDW-GLUE-EBS-MASTER-PARAMETER.json"
    "--spark-event-logs-path"     = "s3://aws-glue-assets-574445142477-us-east-1/sparkHistoryLogs/"
  }
  description               = "usp-edw-glue-raw-normalized job for loading incremental data from s3 raw to s3 normalized"
  execution_class           = "STANDARD"
  glue_version              = jsonencode(4)
  job_run_queuing_enabled   = false
  maintenance_window        = null
  max_capacity              = 10
  max_retries               = 0
  name                      = "usp-edw-glue-raw-normalized"
  non_overridable_arguments = {}
  number_of_workers         = 5
  role_arn                  = "arn:aws:iam::574445142477:role/edw-glue-service-role-dev"
  security_configuration    = null
  tags                      = {}
  tags_all                  = {}
  timeout                   = 2880
  worker_type               = "G.2X"
  command {
    name            = "glueetl"
    python_version  = jsonencode(3)
    runtime         = null
    script_location = "s3://aws-glue-assets-574445142477-us-east-1/scripts/usp-edw-glue-raw-normalized.py"
  }
  execution_property {
    max_concurrent_runs = 20
  }
}

# __generated__ by Terraform
resource "aws_glue_job" "glue-stored-procedure-trigger" {
  connections = ["USP-EDW-GLUE-REDSHIFT-DW-DEV", "USP-EDW-GLUE-REDSHIFT-STG-DEV", "USP-EDW-GLUE-REDSHIFT-USERLOGIN-DEV"]
  default_arguments = {
    "--TempDir"                          = "s3://aws-glue-assets-574445142477-us-east-1/temporary/"
    "--additional-python-modules"        = "redshift-connector"
    "--conf"                             = "spark.sql.parquet.int96RebaseModeInWrite=LEGACY"
    "--config_names"                     = "s3://edw-usp-raw-dev/parameter/store_procedure/USP_USER_LOGIN/USP-EDW-GLUE-PRC_VALIDATE_LOGININFO-CONFIG.json"
    "--enable-continuous-cloudwatch-log" = "true"
    "--enable-glue-datacatalog"          = "true"
    "--enable-job-insights"              = "true"
    "--enable-metrics"                   = "true"
    "--enable-observability-metrics"     = "true"
    "--enable-spark-ui"                  = "true"
    "--env"                              = "env"
    "--extra-py-files"                   = "s3://edw-usp-raw-dev/scripts/usp-edw-glue-framework.zip"
    "--job-bookmark-option"              = "job-bookmark-disable"
    "--job-language"                     = "python"
    "--master_path"                      = "s3://edw-usp-raw-dev/parameter/master/USP-EDW-GLUE-EBS-MASTER-PARAMETER.json"
    "--spark-event-logs-path"            = "s3://aws-glue-assets-574445142477-us-east-1/sparkHistoryLogs/"
  }
  description               = null
  execution_class           = "STANDARD"
  glue_version              = jsonencode(5)
  job_run_queuing_enabled   = false
  maintenance_window        = null
  max_capacity              = 2
  max_retries               = 0
  name                      = "usp-edw-glue-stored-procedure-trigger"
  non_overridable_arguments = {}
  number_of_workers         = 2
  role_arn                  = "arn:aws:iam::574445142477:role/edw-glue-service-role-dev"
  security_configuration    = null
  tags                      = {}
  tags_all                  = {}
  timeout                   = 480
  worker_type               = "G.1X"
  command {
    name            = "glueetl"
    python_version  = jsonencode(3)
    runtime         = null
    script_location = "s3://aws-glue-assets-574445142477-us-east-1/scripts/usp-edw-glue-stored-procedure-trigger.py"
  }
  execution_property {
    max_concurrent_runs = 5
  }
}

# __generated__ by Terraform
resource "aws_glue_job" "glue-pkg_variable_initialization" {
  connections = ["USP-EDW-GLUE-ORACLE-EBS-DEV", "USP-EDW-GLUE-REDSHIFT-DW-DEV"]
  default_arguments = {
    "--TempDir"                   = "s3://aws-glue-assets-574445142477-us-east-1/temporary/"
    "--additional-python-modules" = "redshift-connector"
    "--conf"                      = "spark.sql.parquet.int96RebaseModeInWrite=LEGACY"
    "--config_names"              = "s3://edw-usp-raw-dev/parameter/Global_Variables/USP-EDW-GLUE-PKG-VARIABLE-INITIALIZATION.yaml"
    "--enable-auto-scaling"       = "true"
    "--enable-glue-datacatalog"   = "true"
    "--enable-job-insights"       = "true"
    "--enable-metrics"            = "true"
    "--enable-spark-ui"           = "true"
    "--env"                       = "env"
    "--extra-py-files"            = "s3://edw-usp-raw-dev/scripts/usp-edw-glue-framework.zip"
    "--job-bookmark-option"       = "job-bookmark-disable"
    "--job-language"              = "python"
    "--master_path"               = "s3://edw-usp-raw-dev/parameter/master/USP-EDW-GLUE-EBS-MASTER-PARAMETER.json"
    "--spark-event-logs-path"     = "s3://aws-glue-assets-574445142477-us-east-1/sparkHistoryLogs/"
  }
  description               = "usp-edw-glue-pkg_variable_initialization job for generating global variables json file"
  execution_class           = "STANDARD"
  glue_version              = jsonencode(4)
  job_run_queuing_enabled   = false
  maintenance_window        = null
  max_capacity              = 4
  max_retries               = 0
  name                      = "usp-edw-glue-pkg_variable_initialization"
  non_overridable_arguments = {}
  number_of_workers         = 4
  role_arn                  = "arn:aws:iam::574445142477:role/edw-glue-service-role-dev"
  security_configuration    = null
  tags                      = {}
  tags_all                  = {}
  timeout                   = 2880
  worker_type               = "G.1X"
  command {
    name            = "glueetl"
    python_version  = jsonencode(3)
    runtime         = null
    script_location = "s3://aws-glue-assets-574445142477-us-east-1/scripts/usp-edw-glue-pkg_variable_initialization.py"
  }
  execution_property {
    max_concurrent_runs = 4
  }
}
