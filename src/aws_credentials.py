import os

def load_aws_credentials():
    """Load AWS credentials from environment variables."""
    aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
    aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
    aws_region = os.getenv('AWS_DEFAULT_REGION')

    if not aws_access_key_id or not aws_secret_access_key or not aws_region:
        raise RuntimeError("AWS credentials not set in environment variables")

    return aws_access_key_id, aws_secret_access_key, aws_region
