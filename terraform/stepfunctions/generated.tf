# __generated__ by Terraform
# Please review these resources and move them into your main configuration files.

# __generated__ by Terraform
resource "aws_sfn_state_machine" "sf-ar_bal-f" {
  definition = jsonencode({
    Comment       = "Orchestration for AR_BAL Fact"
    QueryLanguage = "JSONPath"
    StartAt       = "AR_BAL-INTERMEDIATE-DW-F0"
    States = {
      AR_BAL-INTERMEDIATE-DW-F0 = {
        Next = "AR_BAL-INTERMEDIATE-DW-F0_1"
        Parameters = {
          Arguments = {
            "--additional-python-modules" = "redshift-connector"
            "--conf"                      = "spark.sql.parquet.int96RebaseModeInWrite=LEGACY"
            "--config_names"              = "s3://edw-usp-raw-dev/parameter/intermediate-dw/EBS/account_receivables_balance_f/USP-EDW-GLUE-AR_BAL_F0-INC-LOAD-INTERMEDIATE-DW-CONFIG.json"
            "--envs"                      = "env"
            "--master_path"               = "s3://edw-usp-raw-dev/parameter/master/USP-EDW-GLUE-EBS-MASTER-PARAMETER.json"
          }
          JobName = "usp-edw-glue-intermediate-dw"
        }
        Resource = "arn:aws:states:::glue:startJobRun.sync"
        Type     = "Task"
      }
      AR_BAL-INTERMEDIATE-DW-F0_1 = {
        Next = "Success"
        Parameters = {
          Arguments = {
            "--additional-python-modules" = "redshift-connector"
            "--conf"                      = "spark.sql.parquet.int96RebaseModeInWrite=LEGACY"
            "--config_names"              = "s3://edw-usp-raw-dev/parameter/intermediate-dw/EBS/account_receivables_balance_f/USP-EDW-GLUE-AR_BAL_F0_1-INC-LOAD-INTERMEDIATE-DW-CONFIG.json"
            "--envs"                      = "env"
            "--master_path"               = "s3://edw-usp-raw-dev/parameter/master/USP-EDW-GLUE-EBS-MASTER-PARAMETER.json"
          }
          JobName = "usp-edw-glue-intermediate-dw"
        }
        Resource = "arn:aws:states:::glue:startJobRun.sync"
        Type     = "Task"
      }
      Success = {
        Type = "Succeed"
      }
    }
  })
  name        = "usp-edw-sf-ar_bal-f"
  name_prefix = null
  publish     = false
  role_arn    = "arn:aws:iam::574445142477:role/usp-edw-stepfunction-service-role-dev"
  tags        = {}
  tags_all    = {}
  type        = "STANDARD"
  encryption_configuration {
    kms_data_key_reuse_period_seconds = 0
    kms_key_id                        = null
    type                              = "AWS_OWNED_KEY"
  }
  logging_configuration {
    include_execution_data = false
    level                  = "OFF"
    log_destination        = null
  }
  tracing_configuration {
    enabled = false
  }
}

# __generated__ by Terraform
resource "aws_sfn_state_machine" "sf-acct_pay_holds-d" {
  definition = jsonencode({
    Comment       = "Orchestration for ACCT_PAY_HOLDS Dimension"
    QueryLanguage = "JSONPath"
    StartAt       = "ACCT_PAY_HOLDS-STG-INTERMEDIATE"
    States = {
      ACCT_PAY_HOLDS-INTERMEDIATE-DW = {
        Next = "Success"
        Parameters = {
          Arguments = {
            "--additional-python-modules" = "redshift-connector"
            "--conf"                      = "spark.sql.parquet.int96RebaseModeInWrite=LEGACY"
            "--config_names"              = "s3://edw-usp-raw-dev/parameter/stage-intermediate/EBS/acct_pay_holds_d/USP-EDW-GLUE-ACCT_PAY_HOLDS_D0-INC-LOAD-STG-INTERMEDIATE-CONFIG.json"
            "--envs"                      = "env"
            "--master_path"               = "s3://edw-usp-raw-dev/parameter/master/USP-EDW-GLUE-EBS-MASTER-PARAMETER.json"
          }
          JobName = "usp-edw-glue-stg-intermediate"
        }
        Resource = "arn:aws:states:::glue:startJobRun.sync"
        Type     = "Task"
      }
      ACCT_PAY_HOLDS-STG-INTERMEDIATE = {
        Next = "ACCT_PAY_HOLDS-INTERMEDIATE-DW"
        Parameters = {
          Arguments = {
            "--additional-python-modules" = "redshift-connector"
            "--conf"                      = "spark.sql.parquet.int96RebaseModeInWrite=LEGACY"
            "--config_names"              = "s3://edw-usp-raw-dev/parameter/stage-intermediate/EBS/acct_pay_holds_d/USP-EDW-GLUE-ACCT_PAY_HOLDS_D99-INC-LOAD-STG-INTERMEDIATE-CONFIG.json"
            "--envs"                      = "env"
            "--master_path"               = "s3://edw-usp-raw-dev/parameter/master/USP-EDW-GLUE-EBS-MASTER-PARAMETER.json"
          }
          JobName = "usp-edw-glue-stg-intermediate"
        }
        Resource = "arn:aws:states:::glue:startJobRun.sync"
        Type     = "Task"
      }
      Success = {
        Type = "Succeed"
      }
    }
  })
  name        = "usp-edw-sf-acct_pay_holds-d"
  name_prefix = null
  publish     = false
  role_arn    = "arn:aws:iam::574445142477:role/usp-edw-stepfunction-service-role-dev"
  tags        = {}
  tags_all    = {}
  type        = "STANDARD"
  encryption_configuration {
    kms_data_key_reuse_period_seconds = 0
    kms_key_id                        = null
    type                              = "AWS_OWNED_KEY"
  }
  logging_configuration {
    include_execution_data = false
    level                  = "OFF"
    log_destination        = null
  }
  tracing_configuration {
    enabled = false
  }
}

# __generated__ by Terraform
resource "aws_sfn_state_machine" "sf-ap_payment_term-d" {
  definition = jsonencode({
    Comment       = "Orchestration for EBS AP Module"
    QueryLanguage = "JSONPath"
    StartAt       = "EBS_AP_PAYMENT_TERM_D-SOURCE-RAW"
    States = {
      EBS_AP_PAYMENT_TERM_D-INT-DW = {
        Next = "Success"
        Parameters = {
          Arguments = {
            "--additional-python-modules" = "redshift-connector"
            "--conf"                      = "spark.sql.parquet.int96RebaseModeInWrite=LEGACY"
            "--config_names"              = "s3://edw-usp-raw-dev/parameter/intermediate-dw/EBS/ap_payment_term_d/USP-EDW-GLUE-AP_PAYMENT_TERM_D-INC-LOAD-INTERMEDIATE-DW-CONFIG.json"
            "--envs"                      = "env"
            "--master_path"               = "s3://edw-usp-raw-dev/parameter/master/USP-EDW-GLUE-EBS-MASTER-PARAMETER.json"
          }
          JobName = "usp-edw-glue-intermediate-dw"
        }
        Resource = "arn:aws:states:::glue:startJobRun.sync"
        Type     = "Task"
      }
      EBS_AP_PAYMENT_TERM_D-NORMALIZED-STG = {
        Next = "EBS_AP_PAYMENT_TERM_D-STG-INT"
        Parameters = {
          Arguments = {
            "--additional-python-modules" = "redshift-connector"
            "--conf"                      = "spark.sql.parquet.int96RebaseModeInWrite=LEGACY"
            "--config_names"              = "s3://edw-usp-raw-dev/parameter/normalized-stage/EBS/AP/USP-EDW-GLUE-AP-TERMS_TL-INC-LOAD-NORMALIZED-STAGE-CONFIG.json"
            "--envs"                      = "env"
            "--master_path"               = "s3://edw-usp-raw-dev/parameter/master/USP-EDW-GLUE-EBS-MASTER-PARAMETER.json"
          }
          JobName = "usp-edw-glue-normalized-stg"
        }
        Resource = "arn:aws:states:::glue:startJobRun.sync"
        Type     = "Task"
      }
      EBS_AP_PAYMENT_TERM_D-RAW-NORMALIZED = {
        Next = "EBS_AP_PAYMENT_TERM_D-NORMALIZED-STG"
        Parameters = {
          Arguments = {
            "--additional-python-modules" = "redshift-connector"
            "--conf"                      = "spark.sql.parquet.int96RebaseModeInWrite=LEGACY"
            "--config_names"              = "s3://edw-usp-raw-dev/parameter/raw-normalized/EBS/AP/USP-EDW-GLUE-AP-TERMS_TL-INC-LOAD-RAW-NORMALIZED-CONFIG.json"
            "--envs"                      = "env"
            "--master_path"               = "s3://edw-usp-raw-dev/parameter/master/USP-EDW-GLUE-EBS-MASTER-PARAMETER.json"
          }
          JobName = "usp-edw-glue-raw-normalized"
        }
        Resource = "arn:aws:states:::glue:startJobRun.sync"
        Type     = "Task"
      }
      EBS_AP_PAYMENT_TERM_D-SOURCE-RAW = {
        Next = "EBS_AP_PAYMENT_TERM_D-RAW-NORMALIZED"
        Parameters = {
          Arguments = {
            "--additional-python-modules" = "redshift-connector"
            "--conf"                      = "spark.sql.parquet.int96RebaseModeInWrite=LEGACY"
            "--config_names"              = "s3://edw-usp-raw-dev/parameter/source-raw/EBS/AP/USP-EDW-GLUE-AP-TERMS_TL-INC-LOAD-SOURCE-RAW-CONFIG.json"
            "--envs"                      = "env"
            "--master_path"               = "s3://edw-usp-raw-dev/parameter/master/USP-EDW-GLUE-EBS-MASTER-PARAMETER.json"
          }
          JobName = "usp-edw-glue-source-raw"
        }
        Resource = "arn:aws:states:::glue:startJobRun.sync"
        Type     = "Task"
      }
      EBS_AP_PAYMENT_TERM_D-STG-INT = {
        Next = "EBS_AP_PAYMENT_TERM_D-INT-DW"
        Parameters = {
          Arguments = {
            "--additional-python-modules" = "redshift-connector"
            "--conf"                      = "spark.sql.parquet.int96RebaseModeInWrite=LEGACY"
            "--config_names"              = "s3://edw-usp-raw-dev/parameter/stage-intermediate/EBS/ap_payment_term_d/USP-EDW-GLUE-AP_PAYMENT_TERM_D99-INC-LOAD-STG-INTERMEDIATE-CONFIG.json"
            "--envs"                      = "env"
            "--master_path"               = "s3://edw-usp-raw-dev/parameter/master/USP-EDW-GLUE-EBS-MASTER-PARAMETER.json"
          }
          JobName = "usp-edw-glue-stg-intermediate"
        }
        Resource = "arn:aws:states:::glue:startJobRun.sync"
        Type     = "Task"
      }
      Success = {
        Type = "Succeed"
      }
    }
  })
  name        = "usp-edw-sf-ap_payment_term-d"
  name_prefix = null
  publish     = false
  role_arn    = "arn:aws:iam::574445142477:role/usp-edw-stepfunction-service-role-dev"
  tags        = {}
  tags_all    = {}
  type        = "STANDARD"
  encryption_configuration {
    kms_data_key_reuse_period_seconds = 0
    kms_key_id                        = null
    type                              = "AWS_OWNED_KEY"
  }
  logging_configuration {
    include_execution_data = false
    level                  = "OFF"
    log_destination        = null
  }
  tracing_configuration {
    enabled = false
  }
}

# __generated__ by Terraform
resource "aws_sfn_state_machine" "sf-user-d" {
  definition = jsonencode({
    Comment       = "Orchestration for User Dimension"
    QueryLanguage = "JSONPath"
    StartAt       = "USER-STG-INTERMEDIATE"
    States = {
      Success = {
        Type = "Succeed"
      }
      USER-INTERMEDIATE-DW = {
        Next = "Success"
        Parameters = {
          Arguments = {
            "--additional-python-modules" = "redshift-connector"
            "--conf"                      = "spark.sql.parquet.int96RebaseModeInWrite=LEGACY"
            "--config_names"              = "s3://edw-usp-raw-dev/parameter/intermediate-dw/EBS/user_d/USP-EDW-GLUE-USER_D-INC-LOAD-INTERMEDIATE-DW-CONFIG.json"
            "--envs"                      = "env"
            "--master_path"               = "s3://edw-usp-raw-dev/parameter/master/USP-EDW-GLUE-EBS-MASTER-PARAMETER.json"
          }
          JobName = "usp-edw-glue-intermediate-dw"
        }
        Resource = "arn:aws:states:::glue:startJobRun.sync"
        Type     = "Task"
      }
      USER-STG-INTERMEDIATE = {
        Next = "USER-INTERMEDIATE-DW"
        Parameters = {
          Arguments = {
            "--additional-python-modules" = "redshift-connector"
            "--conf"                      = "spark.sql.parquet.int96RebaseModeInWrite=LEGACY"
            "--config_names"              = "s3://edw-usp-raw-dev/parameter/stage-intermediate/EBS/user_d/USP-EDW-GLUE-USER-D99-INC-LOAD-STG-INTERMEDIATE-CONFIG.json"
            "--envs"                      = "env"
            "--master_path"               = "s3://edw-usp-raw-dev/parameter/master/USP-EDW-GLUE-EBS-MASTER-PARAMETER.json"
          }
          JobName = "usp-edw-glue-stg-intermediate"
        }
        Resource = "arn:aws:states:::glue:startJobRun.sync"
        Type     = "Task"
      }
    }
  })
  name        = "usp-edw-sf-user-d"
  name_prefix = null
  publish     = false
  role_arn    = "arn:aws:iam::574445142477:role/usp-edw-stepfunction-service-role-dev"
  tags        = {}
  tags_all    = {}
  type        = "STANDARD"
  encryption_configuration {
    kms_data_key_reuse_period_seconds = 0
    kms_key_id                        = null
    type                              = "AWS_OWNED_KEY"
  }
  logging_configuration {
    include_execution_data = false
    level                  = "OFF"
    log_destination        = null
  }
  tracing_configuration {
    enabled = false
  }
}

# __generated__ by Terraform
resource "aws_sfn_state_machine" "sf-payment_term-d" {
  definition = jsonencode({
    Comment       = "Orchestration for PAYMENT_TERM Dimension"
    QueryLanguage = "JSONPath"
    StartAt       = "PAYMENT_TERM-STG-INTERMEDIATE"
    States = {
      PAYMENT_TERM-INTERMEDIATE-DW = {
        Next = "Success"
        Parameters = {
          Arguments = {
            "--additional-python-modules" = "redshift-connector"
            "--conf"                      = "spark.sql.parquet.int96RebaseModeInWrite=LEGACY"
            "--config_names"              = "s3://edw-usp-raw-dev/parameter/intermediate-dw/EBS/payment_term_d/USP-EDW-GLUE-PAYMENT_TERM_D-INC-LOAD-INTERMEDIATE-DW-CONFIG.json"
            "--envs"                      = "env"
            "--master_path"               = "s3://edw-usp-raw-dev/parameter/master/USP-EDW-GLUE-EBS-MASTER-PARAMETER.json"
          }
          JobName = "usp-edw-glue-intermediate-dw"
        }
        Resource = "arn:aws:states:::glue:startJobRun.sync"
        Type     = "Task"
      }
      PAYMENT_TERM-STG-INTERMEDIATE = {
        Next = "PAYMENT_TERM-INTERMEDIATE-DW"
        Parameters = {
          Arguments = {
            "--additional-python-modules" = "redshift-connector"
            "--conf"                      = "spark.sql.parquet.int96RebaseModeInWrite=LEGACY"
            "--config_names"              = "s3://edw-usp-raw-dev/parameter/stage-intermediate/EBS/payment_term_d/USP-EDW-GLUE-PAYMENT_TERM_D99-INC-LOAD-STG-INTERMEDIATE-CONFIG.json"
            "--envs"                      = "env"
            "--master_path"               = "s3://edw-usp-raw-dev/parameter/master/USP-EDW-GLUE-EBS-MASTER-PARAMETER.json"
          }
          JobName = "usp-edw-glue-stg-intermediate"
        }
        Resource = "arn:aws:states:::glue:startJobRun.sync"
        Type     = "Task"
      }
      Success = {
        Type = "Succeed"
      }
    }
  })
  name        = "usp-edw-sf-payment_term-d"
  name_prefix = null
  publish     = false
  role_arn    = "arn:aws:iam::574445142477:role/usp-edw-stepfunction-service-role-dev"
  tags        = {}
  tags_all    = {}
  type        = "STANDARD"
  encryption_configuration {
    kms_data_key_reuse_period_seconds = 0
    kms_key_id                        = null
    type                              = "AWS_OWNED_KEY"
  }
  logging_configuration {
    include_execution_data = false
    level                  = "OFF"
    log_destination        = null
  }
  tracing_configuration {
    enabled = false
  }
}

# __generated__ by Terraform
resource "aws_sfn_state_machine" "sf-sales_order_hold-d" {
  definition = jsonencode({
    Comment       = "Orchestration for SALES_ORDER_HOLD Dimension"
    QueryLanguage = "JSONPath"
    StartAt       = "SALES_ORDER_HOLD-STG-INTERMEDIATE"
    States = {
      SALES_ORDER_HOLD-INTERMEDIATE-DW = {
        Next = "Success"
        Parameters = {
          Arguments = {
            "--additional-python-modules" = "redshift-connector"
            "--conf"                      = "spark.sql.parquet.int96RebaseModeInWrite=LEGACY"
            "--config_names"              = "s3://edw-usp-raw-dev/parameter/intermediate-dw/EBS/sales_order_holds_d/USP-EDW-GLUE-SALES_ORDER_HOLD-INC-LOAD-INTERMEDIATE-DW-CONFIG.json"
            "--envs"                      = "env"
            "--master_path"               = "s3://edw-usp-raw-dev/parameter/master/USP-EDW-GLUE-EBS-MASTER-PARAMETER.json"
          }
          JobName = "usp-edw-glue-intermediate-dw"
        }
        Resource = "arn:aws:states:::glue:startJobRun.sync"
        Type     = "Task"
      }
      SALES_ORDER_HOLD-STG-INTERMEDIATE = {
        Next = "SALES_ORDER_HOLD-INTERMEDIATE-DW"
        Parameters = {
          Arguments = {
            "--additional-python-modules" = "redshift-connector"
            "--conf"                      = "spark.sql.parquet.int96RebaseModeInWrite=LEGACY"
            "--config_names"              = "s3://edw-usp-raw-dev/parameter/stage-intermediate/EBS/sales_order_holds_d/USP-EDW-GLUE-SALES_ORDER_HOLD_D99-INC-LOAD-STG-INTERMEDIATE-CONFIG.json"
            "--envs"                      = "env"
            "--master_path"               = "s3://edw-usp-raw-dev/parameter/master/USP-EDW-GLUE-EBS-MASTER-PARAMETER.json"
          }
          JobName = "usp-edw-glue-stg-intermediate"
        }
        Resource = "arn:aws:states:::glue:startJobRun.sync"
        Type     = "Task"
      }
      Success = {
        Type = "Succeed"
      }
    }
  })
  name        = "usp-edw-sf-sales_order_hold-d"
  name_prefix = null
  publish     = false
  role_arn    = "arn:aws:iam::574445142477:role/usp-edw-stepfunction-service-role-dev"
  tags        = {}
  tags_all    = {}
  type        = "STANDARD"
  encryption_configuration {
    kms_data_key_reuse_period_seconds = 0
    kms_key_id                        = null
    type                              = "AWS_OWNED_KEY"
  }
  logging_configuration {
    include_execution_data = false
    level                  = "OFF"
    log_destination        = null
  }
  tracing_configuration {
    enabled = false
  }
}

# __generated__ by Terraform
resource "aws_sfn_state_machine" "sf-item_dl-d" {
  definition = jsonencode({
    Comment       = "Orchestration for ITEMS_DL Dimension"
    QueryLanguage = "JSONPath"
    StartAt       = "ITEMS_DL-STG-INTERMEDIATE"
    States = {
      ITEMS_DL-INTERMEDIATE-DW = {
        Next = "Success"
        Parameters = {
          Arguments = {
            "--additional-python-modules" = "redshift-connector"
            "--conf"                      = "spark.sql.parquet.int96RebaseModeInWrite=LEGACY"
            "--config_names"              = "s3://edw-usp-raw-dev/parameter/intermediate-dw/EBS/item_dl/USP-EDW-GLUE-ITEM_DL-INC-LOAD-INTERMEDIATE-DW-CONFIG.json"
            "--envs"                      = "env"
            "--master_path"               = "s3://edw-usp-raw-dev/parameter/master/USP-EDW-GLUE-EBS-MASTER-PARAMETER.json"
          }
          JobName = "usp-edw-glue-intermediate-dw"
        }
        Resource = "arn:aws:states:::glue:startJobRun.sync"
        Type     = "Task"
      }
      ITEMS_DL-STG-INTERMEDIATE = {
        Next = "ITEMS_DL-INTERMEDIATE-DW"
        Parameters = {
          Arguments = {
            "--additional-python-modules" = "redshift-connector"
            "--conf"                      = "spark.sql.parquet.int96RebaseModeInWrite=LEGACY"
            "--config_names"              = "s3://edw-usp-raw-dev/parameter/stage-intermediate/EBS/item_dl/USP-EDW-GLUE-ITEM_DL_D1-99-INC-LOAD-STG-INTERMEDIATE-CONFIG.json"
            "--envs"                      = "env"
            "--master_path"               = "s3://edw-usp-raw-dev/parameter/master/USP-EDW-GLUE-EBS-MASTER-PARAMETER.json"
          }
          JobName = "usp-edw-glue-stg-intermediate"
        }
        Resource = "arn:aws:states:::glue:startJobRun.sync"
        Type     = "Task"
      }
      Success = {
        Type = "Succeed"
      }
    }
  })
  name        = "usp-edw-sf-item_dl-d"
  name_prefix = null
  publish     = false
  role_arn    = "arn:aws:iam::574445142477:role/usp-edw-stepfunction-service-role-dev"
  tags        = {}
  tags_all    = {}
  type        = "STANDARD"
  encryption_configuration {
    kms_data_key_reuse_period_seconds = 0
    kms_key_id                        = null
    type                              = "AWS_OWNED_KEY"
  }
  logging_configuration {
    include_execution_data = false
    level                  = "OFF"
    log_destination        = null
  }
  tracing_configuration {
    enabled = false
  }
}
