import boto3
import logging
import os
from botocore.exceptions import NoCredentialsError, ClientError

# Initialize logging
logging.basicConfig(
    filename='log_history.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def initialize_s3_client():
    """Initialize and return the S3 client"""
    try:
        s3 = boto3.client('s3')
        logging.info("S3 client initialized successfully.")
        return s3
    except NoCredentialsError:
        logging.error("AWS credentials not found.")
        raise
    except Exception as e:
        logging.error(f"Error initializing S3 client: {e}")
        raise

def list_s3_buckets(s3):
    """List all S3 buckets and return the list"""
    try:
        response = s3.list_buckets()
        buckets = [bucket['Name'] for bucket in response['Buckets']]
        logging.info(f"Retrieved bucket list: {buckets}")
        return buckets
    except ClientError as e:
        logging.error(f"Error retrieving S3 buckets: {e}")
        raise

def scan_bucket_objects(s3, bucket_name):
    """Scan and log all objects in a specific S3 bucket"""
    try:
        logging.info(f"Scanning bucket: {bucket_name}")
        objects = s3.list_objects_v2(Bucket=bucket_name)

        if 'Contents' in objects:
            for obj in objects['Contents']:
                logging.info(f"Object found in {bucket_name}: {obj['Key']} (Last Modified: {obj['LastModified']})")
        else:
            logging.info(f"No objects found in {bucket_name}.")
    except ClientError as e:
        logging.error(f"Error scanning bucket {bucket_name}: {e}")
        raise

def log_to_cloudwatch(log_group_name, log_stream_name, message):
    """Log a custom message to AWS CloudWatch Logs"""
    client = boto3.client('logs')
    try:
        # Create log group if it doesn't exist
        client.create_log_group(logGroupName=log_group_name)
    except client.exceptions.ResourceAlreadyExistsException:
        pass  # Log group already exists, no need to create it

    # Create log stream if it doesn't exist
    try:
        client.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)
    except client.exceptions.ResourceAlreadyExistsException:
        pass  # Log stream already exists, no need to create it

    # Get the next sequence token if the log stream already has logs
    try:
        response = client.describe_log_streams(
            logGroupName=log_group_name,
            logStreamNamePrefix=log_stream_name
        )
        sequence_token = response['logStreams'][0].get('uploadSequenceToken', None)
    except Exception as e:
        logging.error(f"Error fetching sequence token: {e}")
        raise

    # Put log events
    try:
        log_event = {
            'logGroupName': log_group_name,
            'logStreamName': log_stream_name,
            'logEvents': [
                {
                    'timestamp': int(round(time.time() * 1000)),
                    'message': message
                }
            ]
        }

        if sequence_token:
            log_event['sequenceToken'] = sequence_token

        client.put_log_events(**log_event)
        logging.info(f"Logged to CloudWatch: {message}")
    except ClientError as e:
        logging.error(f"Error logging to CloudWatch: {e}")
        raise

def main():
    """Main function to orchestrate the S3 scanning and logging"""
    s3 = initialize_s3_client()

    # List all S3 buckets
    buckets = list_s3_buckets(s3)

    # Scan each bucket and log its contents
    for bucket in buckets:
        scan_bucket_objects(s3, bucket)

    # Example of logging a custom message to CloudWatch
    log_group_name = "cronda-logs"
    log_stream_name = "s3-scan-results"
    log_message = "S3 scan completed successfully"
    log_to_cloudwatch(log_group_name, log_stream_name, log_message)

if __name__ == "__main__":
    main()
