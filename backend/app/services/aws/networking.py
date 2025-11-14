"""
Networking Services Checker - VPC, CloudFront, API Gateway, Route 53, etc.
"""
from typing import Dict, Any
import boto3
from botocore.exceptions import ClientError, BotoCoreError

from app.services.aws.base import AWSServiceChecker


class NetworkingChecker(AWSServiceChecker):
    """Checker for AWS Networking services"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ec2_client = self.session.client('ec2')  # VPC is part of EC2
        self.cloudfront_client = self.session.client('cloudfront')
        self.apigateway_client = self.session.client('apigateway')
        self.route53_client = self.session.client('route53')
        self.directconnect_client = self.session.client('directconnect')
        self.globalaccelerator_client = self.session.client('globalaccelerator')
    
    def get_service_name(self) -> str:
        return "networking"
    
    def check_service(self, operation: str, **kwargs) -> Dict[str, Any]:
        """
        Execute networking service operations
        
        Supported operations:
        - vpc: describe_vpcs, describe_subnets, describe_security_groups, etc.
        - cloudfront: list_distributions, get_distribution, etc.
        - apigateway: get_rest_apis, get_resources, etc.
        - route53: list_hosted_zones, list_resource_record_sets, etc.
        - directconnect: describe_connections, describe_virtual_interfaces, etc.
        - globalaccelerator: list_accelerators, describe_accelerator, etc.
        """
        service = kwargs.pop('service', 'vpc')
        
        try:
            if service == 'vpc':
                return self._check_vpc(operation, **kwargs)
            elif service == 'cloudfront':
                return self._check_cloudfront(operation, **kwargs)
            elif service == 'apigateway':
                return self._check_apigateway(operation, **kwargs)
            elif service == 'route53':
                return self._check_route53(operation, **kwargs)
            elif service == 'directconnect':
                return self._check_directconnect(operation, **kwargs)
            elif service == 'globalaccelerator':
                return self._check_globalaccelerator(operation, **kwargs)
            else:
                raise ValueError(f"Unsupported networking service: {service}")
        except (ClientError, BotoCoreError) as e:
            return self._handle_error(e, operation)
    
    def _check_vpc(self, operation: str, **kwargs) -> Dict[str, Any]:
        """VPC operations (via EC2 client)"""
        if not hasattr(self.ec2_client, operation):
            raise ValueError(f"Unsupported VPC operation: {operation}")
        
        method = getattr(self.ec2_client, operation)
        response = method(**kwargs)
        
        return {
            "service": "vpc",
            "operation": operation,
            "data": response,
            "success": True,
        }
    
    def _check_cloudfront(self, operation: str, **kwargs) -> Dict[str, Any]:
        """CloudFront operations"""
        if not hasattr(self.cloudfront_client, operation):
            raise ValueError(f"Unsupported CloudFront operation: {operation}")
        
        method = getattr(self.cloudfront_client, operation)
        response = method(**kwargs)
        
        return {
            "service": "cloudfront",
            "operation": operation,
            "data": response,
            "success": True,
        }
    
    def _check_apigateway(self, operation: str, **kwargs) -> Dict[str, Any]:
        """API Gateway operations"""
        if not hasattr(self.apigateway_client, operation):
            raise ValueError(f"Unsupported API Gateway operation: {operation}")
        
        method = getattr(self.apigateway_client, operation)
        response = method(**kwargs)
        
        return {
            "service": "apigateway",
            "operation": operation,
            "data": response,
            "success": True,
        }
    
    def _check_route53(self, operation: str, **kwargs) -> Dict[str, Any]:
        """Route 53 operations"""
        if not hasattr(self.route53_client, operation):
            raise ValueError(f"Unsupported Route 53 operation: {operation}")
        
        method = getattr(self.route53_client, operation)
        response = method(**kwargs)
        
        return {
            "service": "route53",
            "operation": operation,
            "data": response,
            "success": True,
        }
    
    def _check_directconnect(self, operation: str, **kwargs) -> Dict[str, Any]:
        """Direct Connect operations"""
        if not hasattr(self.directconnect_client, operation):
            raise ValueError(f"Unsupported Direct Connect operation: {operation}")
        
        method = getattr(self.directconnect_client, operation)
        response = method(**kwargs)
        
        return {
            "service": "directconnect",
            "operation": operation,
            "data": response,
            "success": True,
        }
    
    def _check_globalaccelerator(self, operation: str, **kwargs) -> Dict[str, Any]:
        """Global Accelerator operations"""
        if not hasattr(self.globalaccelerator_client, operation):
            raise ValueError(f"Unsupported Global Accelerator operation: {operation}")
        
        method = getattr(self.globalaccelerator_client, operation)
        response = method(**kwargs)
        
        return {
            "service": "globalaccelerator",
            "operation": operation,
            "data": response,
            "success": True,
        }
