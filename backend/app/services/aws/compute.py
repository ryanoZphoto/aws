"""
Compute Services Checker - EC2, Lambda, Lightsail, Batch, etc.
"""
from typing import Dict, Any
import boto3
from botocore.exceptions import ClientError, BotoCoreError

from app.services.aws.base import AWSServiceChecker


class ComputeChecker(AWSServiceChecker):
    """Checker for AWS Compute services"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ec2_client = self.session.client('ec2')
        self.lambda_client = self.session.client('lambda')
        self.lightsail_client = self.session.client('lightsail')
        self.batch_client = self.session.client('batch')
        self.elasticbeanstalk_client = self.session.client('elasticbeanstalk')
    
    def get_service_name(self) -> str:
        return "compute"
    
    def check_service(self, operation: str, **kwargs) -> Dict[str, Any]:
        """
        Execute compute service operations
        
        Supported operations:
        - ec2: describe_instances, describe_images, describe_snapshots, describe_volumes, etc.
        - lambda: list_functions, get_function, list_layers, etc.
        - lightsail: get_instances, get_databases, etc.
        - batch: describe_compute_environments, describe_job_queues, etc.
        - elasticbeanstalk: describe_environments, describe_applications, etc.
        """
        service = kwargs.pop('service', 'ec2')
        
        try:
            if service == 'ec2':
                return self._check_ec2(operation, **kwargs)
            elif service == 'lambda':
                return self._check_lambda(operation, **kwargs)
            elif service == 'lightsail':
                return self._check_lightsail(operation, **kwargs)
            elif service == 'batch':
                return self._check_batch(operation, **kwargs)
            elif service == 'elasticbeanstalk':
                return self._check_elasticbeanstalk(operation, **kwargs)
            else:
                raise ValueError(f"Unsupported compute service: {service}")
        except (ClientError, BotoCoreError) as e:
            return self._handle_error(e, operation)
    
    def _check_ec2(self, operation: str, **kwargs) -> Dict[str, Any]:
        """EC2 operations"""
        if not hasattr(self.ec2_client, operation):
            raise ValueError(f"Unsupported EC2 operation: {operation}")
        
        method = getattr(self.ec2_client, operation)
        response = method(**kwargs)
        
        return {
            "service": "ec2",
            "operation": operation,
            "data": response,
            "success": True,
        }
    
    def _check_lambda(self, operation: str, **kwargs) -> Dict[str, Any]:
        """Lambda operations"""
        if not hasattr(self.lambda_client, operation):
            raise ValueError(f"Unsupported Lambda operation: {operation}")
        
        method = getattr(self.lambda_client, operation)
        response = method(**kwargs)
        
        return {
            "service": "lambda",
            "operation": operation,
            "data": response,
            "success": True,
        }
    
    def _check_lightsail(self, operation: str, **kwargs) -> Dict[str, Any]:
        """Lightsail operations"""
        if not hasattr(self.lightsail_client, operation):
            raise ValueError(f"Unsupported Lightsail operation: {operation}")
        
        method = getattr(self.lightsail_client, operation)
        response = method(**kwargs)
        
        return {
            "service": "lightsail",
            "operation": operation,
            "data": response,
            "success": True,
        }
    
    def _check_batch(self, operation: str, **kwargs) -> Dict[str, Any]:
        """Batch operations"""
        if not hasattr(self.batch_client, operation):
            raise ValueError(f"Unsupported Batch operation: {operation}")
        
        method = getattr(self.batch_client, operation)
        response = method(**kwargs)
        
        return {
            "service": "batch",
            "operation": operation,
            "data": response,
            "success": True,
        }
    
    def _check_elasticbeanstalk(self, operation: str, **kwargs) -> Dict[str, Any]:
        """Elastic Beanstalk operations"""
        if not hasattr(self.elasticbeanstalk_client, operation):
            raise ValueError(f"Unsupported Elastic Beanstalk operation: {operation}")
        
        method = getattr(self.elasticbeanstalk_client, operation)
        response = method(**kwargs)
        
        return {
            "service": "elasticbeanstalk",
            "operation": operation,
            "data": response,
            "success": True,
        }
