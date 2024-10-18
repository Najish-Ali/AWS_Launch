import boto3
from list_buckets import list_s3_buckets
from delete_empty_buckets import delete_empty_buckets
from log_history import log_deletion, log_data
def filter_empty_buckets(s3_client, buckets):
    """Filter out empty buckets."""
    empty_buckets = []
    for bucket in buckets:
        objects = s3_client.list_objects_v2(Bucket=bucket)
        if 'Contents' not in objects:
            empty_buckets.append(bucket)
    return empty_buckets
def main():
    # List S3 buckets
    s3_client = boto3.client('s3')
    buckets = list_s3_buckets(s3_client)
    if buckets:
        # Filter for empty buckets
        empty_buckets = filter_empty_buckets(s3_client, buckets)
        # If there are empty buckets, delete them
        if empty_buckets:
            delete_empty_buckets(empty_buckets)
            for bucket in empty_buckets:
                log_deletion(bucket)
        else:
            print("No empty buckets found.")
    else:
        print("No buckets available.")
if __name__ == "__main__":
    main()
