import {
  to = aws_glue_job.glue-pkg_variable_initialization
  id = "usp-edw-glue-pkg_variable_initialization"
}

import {
  to = aws_glue_job.glue-source-dw
  id = "usp-edw-glue-source-dw"
}

import {
  to = aws_glue_job.glue-source-raw
  id = "usp-edw-glue-source-raw"
}

import {
  to = aws_glue_job.glue-raw-normalized
  id = "usp-edw-glue-raw-normalized"
}

import {
  to = aws_glue_job.glue-normalized-stg
  id = "usp-edw-glue-normalized-stg"
}

import {
  to = aws_glue_job.glue-stg-intermediate
  id = "usp-edw-glue-stg-intermediate"
}

import {
  to = aws_glue_job.glue-intermediate-dw
  id = "usp-edw-glue-intermediate-dw"
}

import {
  to = aws_glue_job.glue-stored-procedure-trigger
  id = "usp-edw-glue-stored-procedure-trigger"
}

import {
  to = aws_glue_job.glue-source-stage-cronjob
  id = "usp-edw-glue-source-stage-cronjob"
}
