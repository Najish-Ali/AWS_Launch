import boto3
import time
import os
import requests

# Get current instance ID to avoid self-termination
try:
    CURRENT_INSTANCE_ID = requests.get('http://169.254.169.254/latest/meta-data/instance-id', timeout=2).text
except requests.RequestException:
    CURRENT_INSTANCE_ID = None

def get_instances_by_ami(ec2, ami_id):
    """Filter running instances by AMI ID"""
    instances = []
    response = ec2.describe_instances(
        Filters=[{
            'Name': 'image-id',
            'Values': [ami_id]
        },
        {
            'Name': 'instance-state-name',
            'Values': ['running']
        }]
    )
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances.append(instance['InstanceId'])
    return instances

def get_instance_launch_time(ec2, instance_id):
    """Get the launch time of an instance"""
    response = ec2.describe_instances(InstanceIds=[instance_id])
    return response['Reservations'][0]['Instances'][0]['LaunchTime']

def get_avg_cpu(cloudwatch, instance_id, region):
    """Get average CPU utilization over the past 30 minutes"""
    end_time = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    start_time = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(time.time() - 1800))
    metric = cloudwatch.get_metric_statistics(
        Namespace='AWS/EC2',
        MetricName='CPUUtilization',
        Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
        StartTime=start_time,
        EndTime=end_time,
        Period=300,
        Statistics=['Average'],
        Unit='Percent'
    )
    datapoints = metric['Datapoints']
    return sum(dp['Average'] for dp in datapoints) / len(datapoints) if datapoints else 0

def get_network_traffic(cloudwatch, instance_id):
    """Get total network traffic (in bytes) in the last 30 minutes"""
    end_time = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    start_time = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(time.time() - 1800))

    def get_sum(metric_name):
        res = cloudwatch.get_metric_statistics(
            Namespace='AWS/EC2',
            MetricName=metric_name,
            Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}],
            StartTime=start_time,
            EndTime=end_time,
            Period=300,
            Statistics=['Sum'],
            Unit='Bytes'
        )
        return sum(dp['Sum'] for dp in res.get('Datapoints', []))

    return get_sum('NetworkIn') + get_sum('NetworkOut')

def main():
    # Fetch environment variables
    region = os.getenv('AWS_REGION')
    ami_id = os.getenv('AMI_ID')
    cpu_threshold = float(os.getenv('CPU_THRESHOLD'))
    traffic_threshold = float(os.getenv('TRAFFIC_THRESHOLD'))

    ec2 = boto3.client('ec2', region_name=region)
    cloudwatch = boto3.client('cloudwatch', region_name=region)

    # Step 1: Find running instances created from this custom AMI
    instance_ids = get_instances_by_ami(ec2, ami_id)
    print(f"Found {len(instance_ids)} instance(s) using this AMI.")

    for instance_id in instance_ids:
        if instance_id == CURRENT_INSTANCE_ID:
            print(f"Skipping self-instance {instance_id}")
            continue

        # Step 2: Monitor CPU utilization and network traffic
        avg_cpu = get_avg_cpu(cloudwatch, instance_id, region)
        print(f"Instance {instance_id} - Avg CPU: {avg_cpu:.2f}%")

        total_traffic = get_network_traffic(cloudwatch, instance_id)
        print(f"Instance {instance_id} - Network Traffic (30 min): {total_traffic:.2f} bytes")

        # Step 3: Terminate instances based on low traffic
        if total_traffic < traffic_threshold:
            print(f"Terminating {instance_id} (Low Network Traffic)...")
            ec2.terminate_instances(InstanceIds=[instance_id])
        else:
            print(f"{instance_id} has sufficient traffic.")

if __name__ == "__main__":
    main()
