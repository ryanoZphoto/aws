"""
Management Services Checker - CloudWatch, CloudFormation, Systems Manager, Config, etc.
"""
from typing import Dict, Any
import boto3
from botocore.exceptions import ClientError, BotoCoreError

from app.services.aws.base import AWSServiceChecker


class ManagementChecker(AWSServiceChecker):
    """Checker for AWS Management & Governance services"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cloudwatch_client = self.session.client('cloudwatch')
        self.cloudformation_client = self.session.client('cloudformation')
        self.ssm_client = self.session.client('ssm')
        self.config_client = self.session.client('config')
        self.organizations_client = self.session.client('organizations')
        self.autoscaling_client = self.session.client('autoscaling')
    
    def get_service_name(self) -> str:
        return "management"
    
    def check_service(self, operation: str, **kwargs) -> Dict[str, Any]:
        """
        Execute management service operations
        
        Supported operations:
        - cloudwatch: list_metrics, get_metric_statistics, describe_alarms, etc.
        - cloudformation: describe_stacks, list_stacks, describe_stack_resources, etc.
        - ssm: describe_instances, get_parameter, list_parameters, etc.
        - config: describe_config_rules, get_compliance_summary_by_config_rule, etc.
        - organizations: list_accounts, describe_organization, etc.
        - autoscaling: describe_auto_scaling_groups, describe_launch_configurations, etc.
        """
        service = kwargs.pop('service', 'cloudwatch')
        
        try:
            if service == 'cloudwatch':
                return self._check_cloudwatch(operation, **kwargs)
            elif service == 'cloudformation':
                return self._check_cloudformation(operation, **kwargs)
            elif service == 'ssm':
                return self._check_ssm(operation, **kwargs)
            elif service == 'config':
                return self._check_config(operation, **kwargs)
            elif service == 'organizations':
                return self._check_organizations(operation, **kwargs)
            elif service == 'autoscaling':
                return self._check_autoscaling(operation, **kwargs)
            else:
                raise ValueError(f"Unsupported management service: {service}")
        except (ClientError, BotoCoreError) as e:
            return self._handle_error(e, operation)
    
    def _check_cloudwatch(self, operation: str, **kwargs) -> Dict[str, Any]:
        """CloudWatch operations"""
        if not hasattr(self.cloudwatch_client, operation):
            raise ValueError(f"Unsupported CloudWatch operation: {operation}")
        
        method = getattr(self.cloudwatch_client, operation)
        response = method(**kwargs)
        
        return {
            "service": "cloudwatch",
            "operation": operation,
            "data": response,
            "success": True,
        }
    
    def _check_cloudformation(self, operation: str, **kwargs) -> Dict[str, Any]:
        """CloudFormation operations"""
        if not hasattr(self.cloudformation_client, operation):
            raise ValueError(f"Unsupported CloudFormation operation: {operation}")
        
        method = getattr(self.cloudformation_client, operation)
        response = method(**kwargs)
        
        return {
            "service": "cloudformation",
            "operation": operation,
            "data": response,
            "success": True,
        }
    
    def _check_ssm(self, operation: str, **kwargs) -> Dict[str, Any]:
        """Systems Manager operations"""
        if not hasattr(self.ssm_client, operation):
            raise ValueError(f"Unsupported SSM operation: {operation}")
        
        method = getattr(self.ssm_client, operation)
        response = method(**kwargs)
        
        return {
            "service": "ssm",
            "operation": operation,
            "data": response,
            "success": True,
        }
    
    def _check_config(self, operation: str, **kwargs) -> Dict[str, Any]:
        """Config operations"""
        if not hasattr(self.config_client, operation):
            raise ValueError(f"Unsupported Config operation: {operation}")
        
        method = getattr(self.config_client, operation)
        response = method(**kwargs)
        
        return {
            "service": "config",
            "operation": operation,
            "data": response,
            "success": True,
        }
    
    def _check_organizations(self, operation: str, **kwargs) -> Dict[str, Any]:
        """Organizations operations"""
        if not hasattr(self.organizations_client, operation):
            raise ValueError(f"Unsupported Organizations operation: {operation}")
        
        method = getattr(self.organizations_client, operation)
        response = method(**kwargs)
        
        return {
            "service": "organizations",
            "operation": operation,
            "data": response,
            "success": True,
        }
    
    def _check_autoscaling(self, operation: str, **kwargs) -> Dict[str, Any]:
        """Auto Scaling operations"""
        if not hasattr(self.autoscaling_client, operation):
            raise ValueError(f"Unsupported Auto Scaling operation: {operation}")
        
        method = getattr(self.autoscaling_client, operation)
        response = method(**kwargs)
        
        return {
            "service": "autoscaling",
            "operation": operation,
            "data": response,
            "success": True,
        }
