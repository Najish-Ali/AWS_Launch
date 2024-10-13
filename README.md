# CRONDA Project

## Overview
CRONDA (Cron Job for Resource Optimization and Deletion Automation) is a Python-based automation project designed to manage AWS S3 buckets by identifying and deleting empty buckets. This project uses AWS SDK for Python (Boto3) and is scheduled to run every Friday at 9 PM via a cron job.

## Features
- Scans AWS S3 buckets to identify empty ones.
- Automatically deletes empty S3 buckets.
- Maintains a log of deleted buckets and the execution time.
- Uses a secure method to handle AWS credentials.

## Project Structure
```plaintext
cronda/
├── src/
│   ├── aws_credentials.py      # Handles loading AWS credentials from secrets file
│   ├── list_buckets.py          # Lists all S3 buckets
│   ├── delete_empty_buckets.py   # Deletes empty S3 buckets
│   ├── log_history.py            # Logs the history of deleted buckets
│   └── main.py                   # Main script to orchestrate the process
├── secrets.json                  # JSON file containing AWS credentials
├── .gitignore                    # Git ignore file
└── README.md                     # Project documentation
