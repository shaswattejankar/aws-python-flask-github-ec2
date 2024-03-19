import boto3

def ec2_server_installation():
    # Specify the variables
    instance_name = INSTANCE_NAME
    instance_region = INSTANCE_REGION
    user_data_script_path = './user_data.sh'
    security_group_id = SECURITY_GROUP_ID
    key_name = KEY_PAIR_NAME

    # Read the user data script
    with open(user_data_script_path, 'r') as user_data_file:
        user_data_script = user_data_file.read()

    # Create EC2 client
    ec2 = boto3.client('ec2', region_name=instance_region)

    # Describe images to get the correct image-id
    response = ec2.describe_images(
        Filters=[
            {
                'Name': 'name',
                'Values': ['ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-20240301']
            },
        ]
    )
    image_id = response['Images'][0]['ImageId']

    # Launch EC2 instance
    response = ec2.run_instances(
        ImageId=image_id,  # Specify the AMI ID for Ubuntu
        InstanceType='t2.micro',  # Specify the instance type
        KeyName=key_name,  # Specify the key pair name
        UserData=user_data_script,  # Specify the user data script
        SecurityGroupIds=[
            security_group_id,
        ],
        MinCount=1,
        MaxCount=1,
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {'Key': 'Name', 'Value': instance_name}
                ]
            }
        ]
    
    )

    # Extract the instance ID
    instance_id = response['Instances'][0]['InstanceId']

    # Wait for the instance to be in the 'running' state
    print('Waiting for instance to be running...')
    waiter = ec2.get_waiter('instance_running')
    waiter.wait(InstanceIds=[instance_id])

    # Describe instances to get public IP address with extracted instance id
    response = ec2.describe_instances(InstanceIds=[instance_id])
    public_ip = response['Reservations'][0]['Instances'][0]['PublicIpAddress']
    print("Public IP of the created instance:", public_ip)

if __name__ == "__main__":

    ec2_server_installation()
