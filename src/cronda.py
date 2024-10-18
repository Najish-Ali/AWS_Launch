import boto3
import json
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from src.list_buckets import list_s3_buckets  # Import the function

def load_credentials():
    try:
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        aws_region = os.getenv('AWS_DEFAULT_REGION')

        if not aws_access_key_id or not aws_secret_access_key or not aws_region:
            raise NoCredentialsError("AWS credentials not set in environment variables")

        return aws_access_key_id, aws_secret_access_key, aws_region
    except Exception as e:
        raise RuntimeError(f"Failed to load credentials: {e}")

def main():
    try:
        aws_access_key_id, aws_secret_access_key, aws_region = load_credentials()

        # Initialize S3 client with credentials
        s3 = boto3.client(
            's3',
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region
        )

        # List buckets
        buckets = list_s3_buckets(s3)  # Call the imported function
        print(f"Buckets found: {buckets}")

    except NoCredentialsError as e:
        print(f"Error: {str(e)}")
    except PartialCredentialsError as e:
        print(f"Incomplete credentials: {str(e)}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
