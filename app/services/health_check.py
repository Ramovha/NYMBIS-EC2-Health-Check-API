"""Health check service module."""
import os
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def get_instance_health(instance_id):
    """Get health status of an EC2 instance.
    
    Queries AWS EC2 API to get instance state and status checks.
    
    Args:
        instance_id (str): AWS EC2 instance ID (e.g., i-0123456789abcdef0)
    
    Returns:
        dict: Health status with 'state' and 'status_code' keys,
              or None if instance not found
              
    Raises:
        ClientError: If AWS API call fails (invalid credentials, no permissions, etc.)
    """
    try:
        # Get region from environment
        region = os.getenv('AWS_REGION', 'us-east-1')
        
        # Initialize EC2 client with correct region
        ec2_client = boto3.client('ec2', region_name=region)
        
        # Get instance state
        instances_response = ec2_client.describe_instances(
            InstanceIds=[instance_id]
        )
        
        # Check if instance exists
        if not instances_response['Reservations']:
            return None
        
        instance = instances_response['Reservations'][0]['Instances'][0]
        instance_state = instance['State']['Name']
        
        # Get instance status checks
        status_response = ec2_client.describe_instance_status(
            InstanceIds=[instance_id],
            IncludeAllInstances=True
        )
        
        # Extract status checks (if instance has status info)
        status_code = 'unknown'
        if status_response['InstanceStatuses']:
            status = status_response['InstanceStatuses'][0]
            instance_status = status.get('InstanceStatus', {})
            status_code = instance_status.get('Status', 'unknown')
        
        return {
            'state': instance_state,
            'status_code': status_code
        }
        
    except ClientError as e:
        error_code = e.response['Error']['Code']
        
        # Instance doesn't exist
        if error_code == 'InvalidInstanceID.NotFound':
            return None
        
        # Other AWS API errors (permissions, throttling, etc.)
        raise e
    except Exception as e:
        # Unexpected errors
        raise e
