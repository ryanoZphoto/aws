"""
Task execution engine for running AWS service checks
"""
from typing import Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from app.models.task import Task, TaskExecution, TaskResult, TaskStatus
from app.models.aws_credentials import AWSCredentials
from app.core.security import decrypt_aws_credentials
from app.services.aws import (
    ComputeChecker,
    StorageChecker,
    DatabaseChecker,
    NetworkingChecker,
    SecurityChecker,
    ManagementChecker,
)


class TaskExecutor:
    """Execute AWS service check tasks"""
    
    # Map AWS service categories to checker classes
    SERVICE_CHECKERS = {
        "compute": ComputeChecker,
        "storage": StorageChecker,
        "database": DatabaseChecker,
        "networking": NetworkingChecker,
        "security": SecurityChecker,
        "management": ManagementChecker,
    }
    
    def __init__(self, db: Session):
        self.db = db
    
    def execute_task(self, task: Task, credentials_id: Optional[int] = None) -> TaskExecution:
        """
        Execute a task and return the execution record
        
        Args:
            task: The task to execute
            credentials_id: Optional AWS credentials ID to use
            
        Returns:
            TaskExecution record with results
            
        Raises:
            Exception: Any errors during execution (no fallbacks)
        """
        # Create execution record
        execution = TaskExecution(
            task_id=task.id,
            status=TaskStatus.RUNNING,
            started_at=datetime.utcnow(),
        )
        self.db.add(execution)
        self.db.commit()
        self.db.refresh(execution)
        
        try:
            # Get AWS credentials
            aws_creds = self._get_aws_credentials(task.user_id, credentials_id)
            
            # Determine service category from AWS service name
            service_category = self._get_service_category(task.aws_service)
            
            # Get appropriate checker
            checker_class = self.SERVICE_CHECKERS.get(service_category)
            if not checker_class:
                raise ValueError(f"Unsupported service category: {service_category}")
            
            # Initialize checker with credentials
            checker = checker_class(
                aws_access_key_id=aws_creds.get("aws_access_key_id"),
                aws_secret_access_key=aws_creds.get("aws_secret_access_key"),
                aws_session_token=aws_creds.get("aws_session_token"),
                region_name=aws_creds.get("aws_region", "us-east-1"),
                iam_role_arn=aws_creds.get("iam_role_arn"),
            )
            
            # Prepare operation parameters
            operation_params = task.config or {}
            operation_params["service"] = task.aws_service
            
            # Execute the check
            result_data = checker.check_service(task.aws_operation, **operation_params)
            
            # Store result
            task_result = TaskResult(
                execution_id=execution.id,
                data=result_data,
            )
            self.db.add(task_result)
            
            # Update execution status
            execution.status = TaskStatus.SUCCESS
            execution.completed_at = datetime.utcnow()
            
            self.db.commit()
            self.db.refresh(execution)
            
            return execution
            
        except Exception as e:
            # No fallbacks - record the error and raise
            execution.status = TaskStatus.FAILED
            execution.error_message = str(e)
            execution.completed_at = datetime.utcnow()
            
            self.db.commit()
            self.db.refresh(execution)
            
            # Re-raise the error (no fallbacks)
            raise
    
    def _get_aws_credentials(self, user_id: int, credentials_id: Optional[int] = None) -> Dict[str, Any]:
        """Get AWS credentials for a user"""
        if credentials_id:
            creds = self.db.query(AWSCredentials).filter(
                AWSCredentials.id == credentials_id,
                AWSCredentials.user_id == user_id
            ).first()
        else:
            # Get default credentials
            creds = self.db.query(AWSCredentials).filter(
                AWSCredentials.user_id == user_id,
                AWSCredentials.is_default == True
            ).first()
        
        if not creds:
            raise ValueError("No AWS credentials found for user")
        
        # Decrypt credentials
        return {
            "aws_access_key_id": decrypt_aws_credentials(creds.aws_access_key_id) if creds.aws_access_key_id else None,
            "aws_secret_access_key": decrypt_aws_credentials(creds.aws_secret_access_key) if creds.aws_secret_access_key else None,
            "aws_session_token": decrypt_aws_credentials(creds.aws_session_token) if creds.aws_session_token else None,
            "aws_region": creds.aws_region,
            "iam_role_arn": creds.iam_role_arn,
        }
    
    def _get_service_category(self, aws_service: str) -> str:
        """Map AWS service name to service category"""
        service_lower = aws_service.lower()
        
        # Compute services
        if service_lower in ["ec2", "lambda", "lightsail", "batch", "elasticbeanstalk", "apprunner"]:
            return "compute"
        
        # Storage services
        elif service_lower in ["s3", "efs", "fsx", "glacier", "backup"]:
            return "storage"
        
        # Database services
        elif service_lower in ["rds", "aurora", "dynamodb", "elasticache", "neptune", "docdb", "timestream"]:
            return "database"
        
        # Networking services
        elif service_lower in ["vpc", "cloudfront", "apigateway", "route53", "directconnect", "globalaccelerator"]:
            return "networking"
        
        # Security services
        elif service_lower in ["iam", "cognito", "secretsmanager", "guardduty", "inspector", "macie", "securityhub"]:
            return "security"
        
        # Management services
        elif service_lower in ["cloudwatch", "cloudformation", "ssm", "config", "organizations", "autoscaling"]:
            return "management"
        
        else:
            # Default to compute for unknown services
            return "compute"
