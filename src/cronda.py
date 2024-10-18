import sys
import os
import boto3
from datetime import datetime

# Ensure src path is included for module imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from list_buckets import list_s3_buckets
from delete_empty_buckets import delete_empty_buckets
from log_history import log_data, log_deletion

def load_credentials():
    try:
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        aws_region = os.getenv('AWS_DEFAULT_REGION')

        if not aws_access_key_id or not aws_secret_access_key or not aws_region:
            raise RuntimeError("AWS credentials not set in environment variables")

        return aws_access_key_id, aws_secret_access_key, aws_region
    except Exception as e:
        raise RuntimeError(f"Failed to load credentials: {e}")

def main():
    try:
        aws_access_key_id, aws_secret_access_key, aws_region = load_credentials()

        # Initialize S3 client with credentials
        s3_client = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region
        )

        # Step 1: List all S3 buckets
        buckets = list_s3_buckets(s3_client)
        print(f"Buckets found: {buckets}")

        # Step 2: Identify and delete empty buckets
        empty_buckets = [bucket for bucket in buckets if s3_client.list_objects_v2(Bucket=bucket).get('Contents') is None]
        if empty_buckets:
            delete_empty_buckets(empty_buckets)
            print(f"Deleted empty buckets: {empty_buckets}")

            # Log the bucket deletion to a file
            for bucket in empty_buckets:
                log_deletion(bucket)
        else:
            print("No empty buckets to delete.")

        # Step 3: Log the operation in CloudWatch
        log_data({
            "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "deleted_buckets": empty_buckets
        })

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

