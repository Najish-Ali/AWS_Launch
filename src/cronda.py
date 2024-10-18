import os
import boto3
from botocore.exceptions import NoCredentialsError

def load_credentials():
    # Fetch AWS credentials and region from environment variables
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    aws_region = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')  # Default to 'us-east-1' if not provided
    
    if not aws_access_key_id or not aws_secret_access_key:
        raise RuntimeError("AWS credentials not set in environment variables")

    return aws_access_key_id, aws_secret_access_key, aws_region

def list_s3_buckets(s3_client):
    try:
        response = s3_client.list_buckets()
        return [bucket['Name'] for bucket in response['Buckets']]
    except Exception as e:
        print(f"Error listing S3 buckets: {e}")
        return []

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
