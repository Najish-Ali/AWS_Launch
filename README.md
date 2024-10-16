# CRONDA

CRONDA is a project designed to monitor and manage AWS S3 buckets by logging and cleaning up empty or extra resources using AWS CloudWatch for logging and monitoring. The project is automated using GitHub Actions for CI/CD pipeline setup.

## Features
- Monitors S3 buckets for unused or extra resources.
- Logs activities using AWS CloudWatch.
-Automates the process of running scripts and cleaning up buckets.

## Prerequisites
 Ensure you have the following tools installed on your local environment:
- Python 3.12+
- AWS CLI (configured with access keys and appropriate permissions)
- Git
- An S3 bucket setup on AWS
- CloudWatch logging permissions
- IAM roles configured for S3 and CloudWatch

## Setup
### Clone the repository:
```
git clone https://github.com/your-repo/cronda.git
cd cronda
```
### Install dependencies:

   Ensure that you have Python and pip installed. Then, run the following command:
```
pip install -r requirements.txt
The requirements.txt file includes dependencies such as watchtower for logging to CloudWatch.
```
### Configure AWS CLI:

   Ensure that your AWS CLI is configured with the necessary credentials and permissions to access S3 and CloudWatch.
```
aws configure
```
### Run the main script:
   After configuring everything, you can run the main script directly to monitor S3 buckets and log actions to CloudWatch.
```
python3 src/main.py
```
This script will scan your AWS S3 buckets and perform the necessary cleanup while logging all events to CloudWatch.

### GitHub Actions Workflow
This project is integrated with GitHub Actions to automate deployment and running of the Python script.

- Workflow steps:

Set up Python: The CI/CD pipeline installs Python 3.12 and required dependencies.Run the main script: It runs the main.py script in the src directory to ensure functionality in the deployment environment.

- GitHub Actions example (main.yml):
```
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.12

      - name: Install dependencies
        run: |
          python3 -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run main script
        run: python3 src/main.py
```
## AWS IAM Policies

To ensure proper access, ensure that the IAM roles attached to your AWS user or service have the following permissions:

- S3: s3:ListBucket, s3:GetObject, s3:DeleteObject
- CloudWatch: logs:CreateLogGroup, logs:CreateLogStream, logs:PutLogEvents

## Logs and Monitoring

All actions performed by the script will be logged to AWS CloudWatch. Ensure that the necessary CloudWatch permissions are enabled.
