"""
Base AWS Service Checker class
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import boto3
from botocore.exceptions import ClientError, BotoCoreError


class AWSServiceChecker(ABC):
    """Base class for all AWS service checkers"""
    
    def __init__(self, aws_access_key_id: Optional[str] = None,
                 aws_secret_access_key: Optional[str] = None,
                 aws_session_token: Optional[str] = None,
                 region_name: str = "us-east-1",
                 iam_role_arn: Optional[str] = None):
        """
        Initialize AWS service checker
        
        Args:
            aws_access_key_id: AWS access key ID
            aws_secret_access_key: AWS secret access key
            aws_session_token: AWS session token (for temporary credentials)
            region_name: AWS region name
            iam_role_arn: IAM role ARN for role assumption
        """
        self.region_name = region_name
        self.iam_role_arn = iam_role_arn
        
        # Create session
        if iam_role_arn:
            # Use role assumption
            sts_client = boto3.client('sts', region_name=region_name)
            assumed_role = sts_client.assume_role(
                RoleArn=iam_role_arn,
                RoleSessionName='aws-service-checker'
            )
            credentials = assumed_role['Credentials']
            self.session = boto3.Session(
                aws_access_key_id=credentials['AccessKeyId'],
                aws_secret_access_key=credentials['SecretAccessKey'],
                aws_session_token=credentials['SessionToken'],
                region_name=region_name
            )
        else:
            # Use provided credentials or default
            session_kwargs = {"region_name": region_name}
            if aws_access_key_id and aws_secret_access_key:
                session_kwargs.update({
                    "aws_access_key_id": aws_access_key_id,
                    "aws_secret_access_key": aws_secret_access_key,
                })
                if aws_session_token:
                    session_kwargs["aws_session_token"] = aws_session_token
            
            self.session = boto3.Session(**session_kwargs)
    
    @abstractmethod
    def get_service_name(self) -> str:
        """Return the AWS service name"""
        pass
    
    @abstractmethod
    def check_service(self, operation: str, **kwargs) -> Dict[str, Any]:
        """
        Execute a check operation on the AWS service
        
        Args:
            operation: The operation to perform (e.g., 'describe_instances')
            **kwargs: Additional parameters for the operation
            
        Returns:
            Dict containing the result of the operation
            
        Raises:
            ClientError: AWS service error
            BotoCoreError: Boto3 error
            Exception: Other errors (no fallbacks - errors interrupt)
        """
        pass
    
    def _handle_error(self, error: Exception, operation: str) -> Dict[str, Any]:
        """
        Handle errors - no fallbacks, errors interrupt
        
        Args:
            error: The exception that occurred
            operation: The operation that failed
            
        Returns:
            Dict with error information (but raises exception)
        """
        error_info = {
            "error": True,
            "service": self.get_service_name(),
            "operation": operation,
            "error_type": type(error).__name__,
            "error_message": str(error),
        }
        
        if isinstance(error, ClientError):
            error_info.update({
                "aws_error_code": error.response.get("Error", {}).get("Code"),
                "aws_error_message": error.response.get("Error", {}).get("Message"),
                "http_status_code": error.response.get("ResponseMetadata", {}).get("HTTPStatusCode"),
            })
        
        # No fallbacks - raise the error
        raise error
