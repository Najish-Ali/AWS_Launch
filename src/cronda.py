import json
import boto3
from botocore.exceptions import NoCredentialsError

def load_credentials():
    try:
        with open('secrets.json', 'r') as f:
            secrets = json.load(f)
            aws_access_key_id = secrets['AWS_ACCESS_KEY_ID']
            aws_secret_access_key = secrets['AWS_SECRET_ACCESS_KEY']
            aws_region = secrets.get('AWS_DEFAULT_REGION', 'us-east-1')  # Default to 'us-east-1' if not in secrets
            return aws_access_key_id, aws_secret_access_key, aws_region
    except FileNotFoundError:
        print("The secrets.json file was not found.")
        raise
    except KeyError as e:
        print(f"Missing key in secrets.json: {e}")
        raise

def list_s3_buckets(s3):
    try:
        response = s3.list_buckets()
        print("Buckets found:")
        for bucket in response['Buckets']:
            print(bucket['Name'])
    except NoCredentialsError:
        print("No valid credentials found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    aws_access_key_id, aws_secret_access_key, aws_region = load_credentials()
    
    # Create a session using the loaded credentials
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region
    )
    
    # Initialize S3 client
    s3 = session.client('s3')
    
    # List buckets
    list_s3_buckets(s3)

if __name__ == "__main__":
    main()

