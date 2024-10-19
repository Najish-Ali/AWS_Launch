import boto3
from aws_credentials import load_aws_credentials
from list_buckets import list_s3_buckets
from delete_empty_buckets import delete_empty_buckets
from log_history import log_data, log_deletion

# Function to check if an S3 bucket is empty
def check_if_empty(s3_client, bucket_name):
    """Check if the specified S3 bucket is empty."""
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name)
        # If 'Contents' key exists in response, bucket is not empty
        if 'Contents' in response:
            return False  # Bucket is not empty
        return True  # Bucket is empty
    except Exception as e:
        print(f"Error checking if bucket {bucket_name} is empty: {e}")
        return False

def main():
    aws_access_key_id, aws_secret_access_key, aws_region = load_aws_credentials()
    
    # Initialize S3 client
    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region
    )

    # List buckets
    buckets = list_s3_buckets(s3)
    
    # Filter empty buckets
    empty_buckets = [bucket for bucket in buckets if check_if_empty(s3, bucket)]

    # Log the deletion
    for bucket in empty_buckets:
        log_deletion(bucket)

    # Delete empty buckets
    delete_empty_buckets(empty_buckets)

if __name__ == "__main__":
    main()
