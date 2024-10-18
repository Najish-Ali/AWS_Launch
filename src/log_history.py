import boto3
import logging
from watchtower import CloudWatchLogHandler
from datetime import datetime

# Set up logging configuration
logger = logging.getLogger("LogHistoryLogger")
logger.setLevel(logging.INFO)  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

# Configure CloudWatch logging
log_group_name = "CrondaLogs"  # Name of your CloudWatch log group
log_stream_name = "LogHistoryStream"  # Name of your log stream

# Create a CloudWatch log handler


# Function to log historical data
def log_data(data):
    logger.info(f"Logging data: {data}")
    # Here you would include the logic to log your historical data
    # For example, appending data to a file or processing it

if __name__ == "__main__":
    # Example usage
    sample_data = {"key": "value"}  # Replace this with your actual data
    log_data(sample_data)

def log_deletion(bucket_name):
    with open('deletion_log.txt', 'a') as log_file:
        log_file.write(f"{datetime.now()}: Deleted bucket {bucket_name}\n")
