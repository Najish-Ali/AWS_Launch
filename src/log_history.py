import logging
from datetime import datetime
# Set up logging configuration
logger = logging.getLogger("LogHistoryLogger")
logger.setLevel(logging.INFO)
def log_deletion(bucket_name=None):
    with open('deletion_log.txt', 'a') as log_file:
        if bucket_name:
            log_file.write(f"{datetime.now()}: Deleted bucket {bucket_name}\n")
        else:
            log_file.write(f"{datetime.now()}: No buckets were deleted.\n")
def log_data(data):
    logger.info(f"Logging data: {data}")
