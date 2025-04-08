# EC2 Instance Launcher

This project automates the launching of EC2 instances on AWS using a Python script and GitHub Actions. The script is designed to be run as part of a GitHub Actions workflow, which allows you to configure and launch EC2 instances in a fully automated way.

## Prerequisites

Before using this project, ensure the following:

1. **AWS Account**: You need an AWS account with the necessary IAM permissions to launch EC2 instances.
2. **GitHub Repository**: A GitHub repository where you can store your Python script and GitHub Actions workflow.
3. **AWS Secrets**: The AWS credentials (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`) must be stored as GitHub Secrets in your repository.

## Setup Instructions

### 1. Create AWS Secrets in GitHub

Go to the **Settings** of your GitHub repository, then navigate to **Secrets** and add the following secrets:

- `AWS_ACCESS_KEY_ID`: Your AWS access key ID.
- `AWS_SECRET_ACCESS_KEY`: Your AWS secret access key.
- `AWS_REGION`: The AWS region where the EC2 instances should be launched.
- `AMI_ID`: The ID of the custom AMI you wish to use for the EC2 instances.
- `NUM_INSTANCES`: The number of EC2 instances to launch (e.g., 1).
- `KEY_NAME`: The name of the SSH key pair to associate with the EC2 instances.
- `SECURITY_GROUP`: The security group ID(s) to associate with the EC2 instances.

### 2. Python Script Setup

The Python script to launch EC2 instances is located in the `src` folder.

Make sure the script `launch_ec2_instances.py` exists inside the `src` folder. Here’s a brief description of the Python script:

- The script uses the `boto3` library to interact with the AWS EC2 service.
- The script will launch EC2 instances based on the environment variables set in the GitHub Actions pipeline.
  
### 3. GitHub Actions Workflow

The workflow configuration file is located in the `.github/workflows` directory.

Here's how the pipeline works:
- **Trigger**: The workflow can be triggered manually using the GitHub Actions **workflow_dispatch** event.
- **Steps**:
  - **Checkout Repository**: The repository is checked out so the workflow can access the code.
  - **Set Up Python**: The workflow sets up Python 3.8.
  - **Configure AWS**: The AWS CLI is configured with the credentials stored in GitHub Secrets.
  - **Install Dependencies**: The `boto3` library is installed for interacting with AWS services.
  - **Run the Launch EC2 Instances Script**: The script located in the `src` folder is run to launch EC2 instances.

### 4. Run the Workflow

To trigger the workflow and launch EC2 instances:
1. Go to the **Actions** tab in your GitHub repository.
2. Select the **Launch EC2 Instances** workflow.
3. Click the **Run workflow** button.
4. This will manually trigger the workflow, and EC2 instances will be launched based on the configuration set in your GitHub Secrets.
