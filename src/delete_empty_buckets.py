import boto3
from aws_credentials import load_aws_credentials
def delete_empty_buckets(empty_buckets):
    aws_access_key_id, aws_secret_access_key, aws_region = load_aws_credentials()
    s3_client = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region
    )
    for bucket in empty_buckets:
        s3_client.delete_bucket(Bucket=bucket)
        print(f"Deleted bucket: {bucket}")
