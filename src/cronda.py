import json
import os
import boto3
from botocore.exceptions import NoCredentialsError

def load_credentials():
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    aws_region = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')

    if aws_access_key_id and aws_secret_access_key:
        return aws_access_key_id, aws_secret_access_key, aws_region

    # If environment variables are not set, load from secrets.json
    try:
        with open('secrets.json', 'r') as f:
            credentials = json.load(f)
            aws_access_key_id = credentials.get('AWS_ACCESS_KEY_ID')
            aws_secret_access_key = credentials.get('AWS_SECRET_ACCESS_KEY')
            aws_region = credentials.get('AWS_DEFAULT_REGION', 'us-east-1')

            if not aws_access_key_id or not aws_secret_access_key:
                raise RuntimeError("AWS credentials missing in secrets.json")

            return aws_access_key_id, aws_secret_access_key, aws_region
    except FileNotFoundError:
        raise RuntimeError("The secrets.json file was not found.")
    except json.JSONDecodeError:
        raise RuntimeError("Error parsing secrets.json file.")

def main():
    # Load AWS credentials
    aws_access_key_id, aws_secret_access_key, aws_region = load_credentials()

    # Set up boto3 client using loaded credentials
    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region
    )

    # Example operation: List S3 buckets
    buckets = list_s3_buckets(s3)
    print(f"Available S3 buckets: {buckets}")

if __name__ == "__main__":
    main()
