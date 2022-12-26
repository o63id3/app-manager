import boto3
from aws_keys import access_key_id, secret_access_key

# client = boto3.client('autoscaling', aws_access_key_id=access_key_id, aws_secret_access_key=secret_access_key, region_name='us-east-1')

# response = client.describe_auto_scaling_groups(
#     AutoScalingGroupNames=[
#         'imagey_autoscaling_group',
#     ]
# )
# number_of_instances = response["AutoScalingGroups"][0]['DesiredCapacity']


asg_client = boto3.client('autoscaling',aws_access_key_id=access_key_id,aws_secret_access_key=secret_access_key,region_name='us-east-1')
ec2_client = boto3.client('ec2',aws_access_key_id=access_key_id,aws_secret_access_key=secret_access_key,region_name='us-east-1')

asg = "imagey_autoscaling_group"
print(asg)
asg_response = asg_client.describe_auto_scaling_groups(AutoScalingGroupNames=[asg])

instance_ids = [] # List to hold the instance-ids

for i in asg_response['AutoScalingGroups']:
    for k in i['Instances']:
        instance_ids.append(k['InstanceId'])

ec2_response = ec2_client.describe_instances(
        InstanceIds = instance_ids
        )   
print(instance_ids) #This line will print the instance_ids

private_ip = [] # List to hold the Private IP Address

for instances in ec2_response['Reservations']:
    for ip in instances['Instances']:
        private_ip.append(ip['PublicIpAddress'])


print("\n".join(private_ip))