#!/bin/bash
# At least first 3 parameters are required

usage() {
   echo
   echo "Usage:"
   echo " automation/deploy.sh -access-key <AWS Access Key> -secret-key <AWS Secret Access Key> -environment <Env name> [--destroy]"
   echo
   echo " environment values: dev/test/prod"
   echo
}

export AWS_ACCESS_KEY_ID=
export AWS_SECRET_ACCESS_KEY=
export AWS_DEFAULT_REGION="us-east-1"
ENV_NAME=
DESTROY_FLAG=N

while test "$1" != ""
do
   case $1 in
      -access-key)
         AWS_ACCESS_KEY_ID="$2"
         shift
         ;;
      -secret-key)
         AWS_SECRET_ACCESS_KEY="$2"
         shift
         ;;
      -environment)
         ENV_NAME="${2,,}"
         shift
         ;;
      -region)
         AWS_DEFAULT_REGION="${2,,}"
         shift
         ;;
      --destroy)
        DESTROY_FLAG=Y
        ;;
      -*)
        echo "Unrecognised parameter"
        usage
        exit 101
        ;;
   esac
   shift
done

if [ -z "${AWS_ACCESS_KEY_ID}" ]; then
   echo "Required -access-key parameter is not passed"
   usage
   exit 1;
fi

if [ -z "${AWS_SECRET_ACCESS_KEY}" ]; then
   echo "Required -secret-key parameter is not passed"
   usage
   exit 1;
fi

if [ -z "${ENV_NAME}" ]; then
   echo "Required -environment parameter is not passed"
   usage
   exit 1;
fi

echo "###############################################"
echo "Setting AWS Access Keys"
#echo "###############################################"
aws configure set aws_access_key_id ${AWS_ACCESS_KEY_ID}
aws configure set aws_secret_access_key ${AWS_SECRET_ACCESS_KEY}
aws configure set default.region ${AWS_DEFAULT_REGION}
aws configure set preview.cloudsearch true

CURRENT_TIME_SECONDS=`date '+%s'`
ACCOUNT_ID=$(aws sts get-caller-identity | jq '.Account' | sed 's/\"//g')

###MAKE SURE BUCKETS MATCH#######
#Create S3 Bucket named usp-iac-tf-state-bucket TODO - Bucket ID must be unique - to match TF
#state_bucket="usp-terraform-state-${CURRENT_TIME_SECONDS}"
state_bucket="usp-terraform-state-${AWS_DEFAULT_REGION}-${ACCOUNT_ID}"
aws s3api head-bucket --bucket "${state_bucket}" 2>&1
if [ "$?" -ne 0 ]; then
   echo "###############################################"
   echo "Creating S3 Bucket for terraform state: ${state_bucket}"
   aws s3api --no-verify-ssl create-bucket --bucket "${state_bucket}" --region "${AWS_DEFAULT_REGION}"
fi

echo "###############################################"
echo "Updating the config tf file"
FILE=./config.tf
if [ -f "$FILE" ]; then
    echo "$FILE file exists."
    echo "skipping the creation of config.tf"
else
    #sed  "s/@@TIMESECONDS@@/${CURRENT_TIME_SECONDS}/g" automation/config.tf.templ > ./config.tf
    sed -e "s/@@REGION@@/${AWS_DEFAULT_REGION}/g" -e "s/@@ACCOUNTID@@/${ACCOUNT_ID}/g" automation/config.tf.templ > ./config.tf
fi

echo "###############################################"
echo "Current Working Dir -- "`pwd`
sleep 5

echo "###############################################"
echo "Running terraform init"

rm -rf .terraform*
sleep 3
# initialize modules, plugins, providers, and backend
terraform init

echo "###############################################"
echo "Running terraform workspace selection/creation"
#echo "###############################################"

# workspace selection or creation if not exist
terraform workspace select ${ENV_NAME} || terraform workspace new ${ENV_NAME}
sleep 3
terraform workspace list
retval=0
if [[ "${DESTROY_FLAG}" == "Y" ]]; then
   terraform destroy -auto-approve -var-file=env/tf-resources.tfvars -var-file=env/${ENV_NAME}.tfvars -var "usp_aws_access_key=${AWS_ACCESS_KEY_ID}" -var "usp_aws_secret_key=${AWS_SECRET_ACCESS_KEY}" 
   retval=$?
else
   terraform apply -auto-approve -var-file=env/tf-resources.tfvars -var-file=env/${ENV_NAME}.tfvars -var "usp_aws_access_key=${AWS_ACCESS_KEY_ID}" -var "usp_aws_secret_key=${AWS_SECRET_ACCESS_KEY}" 
   retval=$?
fi
sleep 6
echo "##################################################################################################################################"
echo "Step completed"
echo "##################################################################################################################################"
echo "Exit code: $retval"
exit $retval