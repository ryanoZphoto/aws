"""Base class for AWS service integrations."""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import boto3
from botocore.exceptions import ClientError, BotoCoreError
from app.core.logging import logger


class AWSServiceError(Exception):
    """Base exception for AWS service errors."""
    pass


class AWSAuthenticationError(AWSServiceError):
    """AWS authentication error."""
    pass


class AWSPermissionError(AWSServiceError):
    """AWS permission error."""
    pass


class AWSServiceLimitError(AWSServiceError):
    """AWS service limit error."""
    pass


class AWSServiceBase(ABC):
    """Base class for AWS service integrations."""
    
    def __init__(self, access_key_id: str, secret_access_key: str, region: str = "us-east-1"):
        """
        Initialize AWS service client.
        
        Args:
            access_key_id: AWS access key ID
            secret_access_key: AWS secret access key
            region: AWS region
        """
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.region = region
        self._session = None
        self._clients: Dict[str, Any] = {}
    
    @property
    def session(self):
        """Get or create boto3 session."""
        if self._session is None:
            self._session = boto3.Session(
                aws_access_key_id=self.access_key_id,
                aws_secret_access_key=self.secret_access_key,
                region_name=self.region,
            )
        return self._session
    
    def get_client(self, service_name: str):
        """Get or create boto3 client for a service."""
        if service_name not in self._clients:
            self._clients[service_name] = self.session.client(service_name)
        return self._clients[service_name]
    
    def _handle_error(self, error: Exception, operation: str) -> None:
        """
        Handle AWS errors according to the no-fallback policy.
        Errors interrupt execution immediately.
        
        Args:
            error: The exception that occurred
            operation: Description of the operation that failed
        """
        error_code = None
        error_message = str(error)
        
        if isinstance(error, ClientError):
            error_code = error.response.get("Error", {}).get("Code", "")
            error_message = error.response.get("Error", {}).get("Message", str(error))
        
        logger.error(
            "aws_service_error",
            service=self.__class__.__name__,
            operation=operation,
            error_code=error_code,
            error_message=error_message,
            exc_info=True,
        )
        
        # Categorize and raise appropriate exception
        if error_code in ["InvalidClientTokenId", "SignatureDoesNotMatch", "AuthFailure"]:
            raise AWSAuthenticationError(f"Authentication failed: {error_message}") from error
        elif error_code in ["AccessDenied", "UnauthorizedOperation"]:
            raise AWSPermissionError(f"Permission denied: {error_message}") from error
        elif error_code in ["Throttling", "ServiceUnavailable", "RequestLimitExceeded"]:
            raise AWSServiceLimitError(f"Service limit exceeded: {error_message}") from error
        else:
            raise AWSServiceError(f"Operation '{operation}' failed: {error_message}") from error
    
    @abstractmethod
    def health_check(self) -> Dict[str, Any]:
        """
        Perform a health check on the service.
        
        Returns:
            Dict with health check results
        """
        pass
    
    @abstractmethod
    def list_resources(self, **kwargs) -> Dict[str, Any]:
        """
        List resources in the service.
        
        Returns:
            Dict with resource list
        """
        pass
