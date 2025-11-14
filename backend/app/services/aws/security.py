"""
Security Services Checker - IAM, Cognito, Secrets Manager, GuardDuty, etc.
"""
from typing import Dict, Any
import boto3
from botocore.exceptions import ClientError, BotoCoreError

from app.services.aws.base import AWSServiceChecker


class SecurityChecker(AWSServiceChecker):
    """Checker for AWS Security services"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.iam_client = self.session.client('iam')
        self.cognito_client = self.session.client('cognito-idp')
        self.secretsmanager_client = self.session.client('secretsmanager')
        self.guardduty_client = self.session.client('guardduty')
        self.inspector_client = self.session.client('inspector2')
        self.macie_client = self.session.client('macie2')
        self.securityhub_client = self.session.client('securityhub')
    
    def get_service_name(self) -> str:
        return "security"
    
    def check_service(self, operation: str, **kwargs) -> Dict[str, Any]:
        """
        Execute security service operations
        
        Supported operations:
        - iam: list_users, list_roles, list_policies, get_account_summary, etc.
        - cognito: list_user_pools, describe_user_pool, etc.
        - secretsmanager: list_secrets, describe_secret, etc.
        - guardduty: list_detectors, get_findings, etc.
        - inspector: list_findings, get_findings, etc.
        - macie: list_findings, get_findings, etc.
        - securityhub: get_findings, list_findings, etc.
        """
        service = kwargs.pop('service', 'iam')
        
        try:
            if service == 'iam':
                return self._check_iam(operation, **kwargs)
            elif service == 'cognito':
                return self._check_cognito(operation, **kwargs)
            elif service == 'secretsmanager':
                return self._check_secretsmanager(operation, **kwargs)
            elif service == 'guardduty':
                return self._check_guardduty(operation, **kwargs)
            elif service == 'inspector':
                return self._check_inspector(operation, **kwargs)
            elif service == 'macie':
                return self._check_macie(operation, **kwargs)
            elif service == 'securityhub':
                return self._check_securityhub(operation, **kwargs)
            else:
                raise ValueError(f"Unsupported security service: {service}")
        except (ClientError, BotoCoreError) as e:
            return self._handle_error(e, operation)
    
    def _check_iam(self, operation: str, **kwargs) -> Dict[str, Any]:
        """IAM operations"""
        if not hasattr(self.iam_client, operation):
            raise ValueError(f"Unsupported IAM operation: {operation}")
        
        method = getattr(self.iam_client, operation)
        response = method(**kwargs)
        
        return {
            "service": "iam",
            "operation": operation,
            "data": response,
            "success": True,
        }
    
    def _check_cognito(self, operation: str, **kwargs) -> Dict[str, Any]:
        """Cognito operations"""
        if not hasattr(self.cognito_client, operation):
            raise ValueError(f"Unsupported Cognito operation: {operation}")
        
        method = getattr(self.cognito_client, operation)
        response = method(**kwargs)
        
        return {
            "service": "cognito",
            "operation": operation,
            "data": response,
            "success": True,
        }
    
    def _check_secretsmanager(self, operation: str, **kwargs) -> Dict[str, Any]:
        """Secrets Manager operations"""
        if not hasattr(self.secretsmanager_client, operation):
            raise ValueError(f"Unsupported Secrets Manager operation: {operation}")
        
        method = getattr(self.secretsmanager_client, operation)
        response = method(**kwargs)
        
        return {
            "service": "secretsmanager",
            "operation": operation,
            "data": response,
            "success": True,
        }
    
    def _check_guardduty(self, operation: str, **kwargs) -> Dict[str, Any]:
        """GuardDuty operations"""
        if not hasattr(self.guardduty_client, operation):
            raise ValueError(f"Unsupported GuardDuty operation: {operation}")
        
        method = getattr(self.guardduty_client, operation)
        response = method(**kwargs)
        
        return {
            "service": "guardduty",
            "operation": operation,
            "data": response,
            "success": True,
        }
    
    def _check_inspector(self, operation: str, **kwargs) -> Dict[str, Any]:
        """Inspector operations"""
        if not hasattr(self.inspector_client, operation):
            raise ValueError(f"Unsupported Inspector operation: {operation}")
        
        method = getattr(self.inspector_client, operation)
        response = method(**kwargs)
        
        return {
            "service": "inspector",
            "operation": operation,
            "data": response,
            "success": True,
        }
    
    def _check_macie(self, operation: str, **kwargs) -> Dict[str, Any]:
        """Macie operations"""
        if not hasattr(self.macie_client, operation):
            raise ValueError(f"Unsupported Macie operation: {operation}")
        
        method = getattr(self.macie_client, operation)
        response = method(**kwargs)
        
        return {
            "service": "macie",
            "operation": operation,
            "data": response,
            "success": True,
        }
    
    def _check_securityhub(self, operation: str, **kwargs) -> Dict[str, Any]:
        """Security Hub operations"""
        if not hasattr(self.securityhub_client, operation):
            raise ValueError(f"Unsupported Security Hub operation: {operation}")
        
        method = getattr(self.securityhub_client, operation)
        response = method(**kwargs)
        
        return {
            "service": "securityhub",
            "operation": operation,
            "data": response,
            "success": True,
        }
