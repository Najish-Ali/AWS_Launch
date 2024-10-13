from datetime import datetime

def log_deletion(bucket_name):
    with open('deletion_log.txt', 'a') as log_file:
        log_file.write(f"{datetime.now()}: Deleted bucket {bucket_name}\n")
