"""Health check service module."""
import os
import boto3
from botocore.exceptions import ClientError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def map_health_status(state, status_code):
    """Map EC2 instance state and status checks to human-readable health status.
    
    User Story 2 implementation: Map raw AWS state and status codes to
    a simple, human-readable health status.
    
    Args:
        state (str): EC2 instance state (running, stopped, terminated, stopping, pending, etc.)
        status_code (str): Instance status checks (ok, initializing, insufficient-data, failed, unknown)
    
    Returns:
        str: Human-readable health status:
            - "healthy": Instance is running with all status checks passing
            - "initializing": Instance is running but still initializing
            - "unhealthy": Instance is running but status checks failed
            - "stopped": Instance is stopped
            - "terminated": Instance is terminated
            - "unknown": Unknown or transitional state
    """
    # Handle stopped and terminated states
    if state == 'stopped':
        return 'stopped'
    elif state == 'terminated':
        return 'terminated'
    
    # Handle running state with status checks
    elif state == 'running':
        if status_code == 'ok':
            return 'healthy'
        elif status_code == 'initializing':
            return 'initializing'
        elif status_code == 'insufficient-data':
            return 'initializing'
        elif status_code == 'failed':
            return 'unhealthy'
        else:  # unknown, or other values
            return 'initializing'
    
    # Handle transitional states
    elif state in ['stopping', 'pending']:
        return 'initializing'
    
    # Default for unknown states
    else:
        return 'unknown'


def get_instance_health(instance_id):
    """Get health status of an EC2 instance.
    
    Queries AWS EC2 API to get instance state and status checks.
    Maps them to human-readable health status (healthy, initializing, unhealthy, stopped, terminated).
    
    User Story 2 implementation: Uses boto3 to query real AWS EC2 instance data
    and derives health status from state + status checks.
    
    Args:
        instance_id (str): AWS EC2 instance ID (e.g., i-0123456789abcdef0)
    
    Returns:
        dict: Health status with 'state', 'status_code', and 'health' keys,
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
        
        # Map to human-readable health status (User Story 2)
        health_status = map_health_status(instance_state, status_code)
        
        return {
            'state': instance_state,
            'status_code': status_code,
            'health': health_status
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
