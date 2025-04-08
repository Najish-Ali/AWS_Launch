# launch_ec2_instances.py
import boto3

# Take user inputs
region = input("Enter the AWS region (e.g., ap-south-1): ")
num_instances = int(input("Enter the number of instances to launch: "))
ami_id = input("Enter the custom AMI ID: ")
#instance_type = input("Enter the instance type (e.g., t2.micro): ")
#key_name = input("Enter the key pair name (for SSH access): ")

# Initialize EC2 client
ec2 = boto3.client('ec2', region_name=region)

# Launch instances using a custom AMI
response = ec2.run_instances(
    ImageId=ami_id,  # Specify the AMI ID here
    MinCount=num_instances,
    MaxCount=num_instances,
    InstanceType="t2.micro",  # Instance type
    KeyName="test",  # SSH key pair for access
    SecurityGroupIds=["sg-0cd5a1a0c2a934f7d"]
)

# Store and print launched instance IDs
instance_ids = [instance['InstanceId'] for instance in response['Instances']]
for idx, instance_id in enumerate(instance_ids, start=1):
    print(f"Launched EC2 instance {idx}: {instance_id}")
