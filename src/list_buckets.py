import boto3
from aws_credentials import load_aws_credentials

def list_buckets():
    aws_access_key_id, aws_secret_access_key, aws_region = load_aws_credentials()
    s3_client = boto3.client(
        's3',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region
    )
    response = s3_client.list_buckets()
    return [bucket['Name'] for bucket in response['Buckets']]
