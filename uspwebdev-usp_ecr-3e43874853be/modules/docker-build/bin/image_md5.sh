#!/bin/bash

# Fail fast
set -e

# List of arguments
dockerfile_path=$1

# Linux has command md5sum and OSX has command md5
if command -v md5sum >/dev/null 2>&1; then
  md5_cmd=md5sum
elif command -v md5 >/dev/null 2>&1; then
  md5_cmd=md5
else
  echo "ERROR: md5sum is not installed"
  exit 255
fi

# Take md5 from each file inside the dockerfile_path and take a md5 of these files to output
md5_result=$(eval $md5_cmd $dockerfile_path/** | $md5_cmd )

# Output result as JSON back to terraform
echo "{ \"md5\": \"$md5_result\" }"
