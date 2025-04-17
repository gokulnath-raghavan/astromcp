import {
  to = aws_lambda_function.user_login_file_validation
  id = "arn:aws:lambda:us-east-1:574445142477:function:usp-edw-dev-user_login_file_validation"
}


import {
  to = aws_lambda_function.user_login_business_logic
  id = "usp-edw-dev-user_login_business_logic"
}

import {
  to = aws_lambda_function.user_login_success_failure_lambda
  id = "usp-edw-dev-user_login_success_failure_lambda"
}
