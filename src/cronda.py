from aws_credentials import load_aws_credentials
from list_buckets import list_s3_buckets
from delete_empty_buckets import delete_empty_buckets
from log_history import log_data, log_deletion

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
    empty_buckets = [bucket for bucket in buckets if check_if_empty(s3, bucket)]

    # Log the deletion
    for bucket in empty_buckets:
        log_deletion(bucket)

    # Delete empty buckets
    delete_empty_buckets(empty_buckets)

if __name__ == "__main__":
    main()
