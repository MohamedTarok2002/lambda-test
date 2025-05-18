#!/bin/bash
set -e  # Exit on any error

echo "Lambda files got changed. Going to update lambda function code"

# Fetch parameters from SSM Parameter Store and save as .env file
aws ssm get-parameters-by-path --path /Test-LAMBDA --region us-west-2 | \
  jq -r '.Parameters | map(.Name+"="+.Value) | join("\n") | sub("/Test-LAMBDA/"; ""; "g")' > .env

# Prepare temporary folder for packaging
mkdir -p /tmp/lamda/Test

echo "Copying files from project to temp folder"
rsync -a Test/ /tmp/lamda/Test/

# Rename your main Lambda file to the expected handler name
mv /tmp/lamda/Test/Test.py /tmp/lamda/Test/lambda_function.py

# Copy environment variables file into temp folder
cp .env /tmp/lamda/Test/.env

# Zip the contents of the temp folder
cd /tmp/lamda/Test/ && zip -rq ../Test.zip .

# Upload zip to S3 bucket (replace 'your-bucket' with your bucket name)
aws s3 cp /tmp/lamda/Test.zip s3://your-bucket/lambda_functions/Test-Lambda/Test.zip

# Update Lambda function code from the S3 bucket (replace 'TestLambda' with your function name)
aws lambda update-function-code --function-name TestLambda --s3-bucket your-bucket --s3-key lambda_functions/Test-Lambda/Test.zip

echo "Lambda function code updated successfully."
