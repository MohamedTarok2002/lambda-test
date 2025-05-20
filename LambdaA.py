import boto3
import os
import zipfile
import json

lambda_client = boto3.client('lambda')

def lambda_handler(event, context):
    s3 = boto3.client('s3')

    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    download_path = '/tmp/temp.zip'
    extract_path = '/tmp/extracted/'

    # Download the zip file from S3
    s3.download_file(bucket, key, download_path)

    # Ensure extraction directory exists
    os.makedirs(extract_path, exist_ok=True)

    # Extract the zip file
    with zipfile.ZipFile(download_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

    # List extracted files for debugging
    extracted_files = os.listdir(extract_path)
    print("Extracted files:", extracted_files)

    # Construct path to your Python file (adjust filename if necessary)
    code_file = os.path.join(extract_path, 'lambda.py')  # Update if you fix the filename to 'lambda.py'

    # Check if file exists before opening
    if not os.path.isfile(code_file):
        raise FileNotFoundError(f"{code_file} not found in extracted contents")

    # Open and read the code file
    with open(code_file, 'r') as f:
        code = f.read()

    print("Code content loaded successfully")

    # Invoke Lambda B asynchronously, passing the code as payload
    response = lambda_client.invoke(
        FunctionName='lambdarun',  # Replace with your Lambda B function name
        InvocationType='Event',  # Async invocation
        Payload=json.dumps({'code': code})
    )

    print(f"Invoked Lambda B with status code: {response['StatusCode']}")

    return {
        'statusCode': 200,
        'body': 'File processed and Lambda B invoked successfully'
    }
