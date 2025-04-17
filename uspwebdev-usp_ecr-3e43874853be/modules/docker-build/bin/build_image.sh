#!/bin/bash

# Fail fast
set -e

dockerfile_path=$1
ecr_repository_url_with_tag=$2
aws_region=$3

# overriding the aws region from system
if [ "$aws_region" != "" ]; then
  aws_extra_flags="--region ${aws_region}"
else
  aws_extra_flags=""
fi

# Check that aws is installed
which aws > /dev/null || { echo 'ERROR: aws-cli is not installed' ; exit 1; }

# Check that docker is installed and running
which docker > /dev/null && docker ps > /dev/null || { echo 'ERROR: docker is not running' ; exit 1; }

# Connect into aws
aws ecr get-login-password ${aws_extra_flags} | docker login --username AWS --password-stdin ${ecr_repository_url_with_tag}

# Some Useful Debug
echo "Building ${ecr_repository_url_with_tag} from ${dockerfile_path}/Dockerfile"

# Build image
docker build -t ${ecr_repository_url_with_tag} ${dockerfile_path}

# Push image
docker push ${ecr_repository_url_with_tag}
