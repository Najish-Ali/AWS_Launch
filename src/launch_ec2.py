import boto3
import os

def launch_ec2_instances(region, num_instances, ami_id, instance_type, key_name, security_group_ids):
    ec2 = boto3.client('ec2', region_name=region)
    response = ec2.run_instances(
        ImageId=ami_id,
        MinCount=num_instances,
        MaxCount=num_instances,
        InstanceType=instance_type,
        KeyName=key_name,
        SecurityGroupIds=security_group_ids
    )
    instance_ids = [instance['InstanceId'] for instance in response['Instances']]
    for idx, instance_id in enumerate(instance_ids, start=1):
        print(f"  Instance {idx}: {instance_id}")

if __name__ == "__main__":
    region = os.getenv('AWS_REGION', 'us-west-2')
    num_instances = int(os.getenv('NUM_INSTANCES', 1))
    ami_id = os.getenv('AMI_ID', '')
    instance_type = os.getenv('INSTANCE_TYPE', 't2.micro')
    key_name = os.getenv('KEY_NAME', 'my-key-pair')
    security_group_ids = os.getenv('SECURITY_GROUP_IDS', 'sg-12345678').split(',')

    if not ami_id:
        print("AMI ID must be provided!")
        exit(1)

    launch_ec2_instances(region, num_instances, ami_id, instance_type, key_name, security_group_ids)
