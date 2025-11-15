"""Task execution logic."""
from typing import Dict, Any, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.task import Task, TaskExecution, TaskResult, TaskStatus
from app.models.aws_credentials import AWSCredentials
from app.aws import (
    ComputeService,
    StorageService,
    DatabaseService,
    NetworkingService,
    SecurityService,
    AnalyticsService,
)
from app.aws.base import (
    AWSServiceError,
    AWSAuthenticationError,
    AWSPermissionError,
    AWSServiceLimitError,
)
from app.core.logging import logger


class TaskExecutor:
    """Execute AWS automation tasks."""
    
    SERVICE_MAP = {
        "compute": ComputeService,
        "storage": StorageService,
        "database": DatabaseService,
        "networking": NetworkingService,
        "security": SecurityService,
        "analytics": AnalyticsService,
    }
    
    @staticmethod
    async def execute_task(
        db: AsyncSession,
        task_id: int,
        aws_credentials_id: Optional[int] = None,
    ) -> TaskExecution:
        """
        Execute a task.
        
        Args:
            db: Database session
            task_id: Task ID to execute
            aws_credentials_id: Optional AWS credentials ID (uses default if not provided)
        
        Returns:
            TaskExecution record
        """
        # Get task
        result = await db.execute(select(Task).where(Task.id == task_id))
        task = result.scalar_one_or_none()
        
        if not task:
            raise ValueError(f"Task {task_id} not found")
        
        if not task.is_active:
            raise ValueError(f"Task {task_id} is not active")
        
        # Get AWS credentials
        if aws_credentials_id:
            creds_result = await db.execute(
                select(AWSCredentials).where(AWSCredentials.id == aws_credentials_id)
            )
            credentials = creds_result.scalar_one_or_none()
        else:
            # Get default credentials for user
            creds_result = await db.execute(
                select(AWSCredentials).where(
                    AWSCredentials.user_id == task.user_id,
                    AWSCredentials.is_default == True,
                    AWSCredentials.is_active == True,
                )
            )
            credentials = creds_result.scalar_one_or_none()
        
        if not credentials:
            raise ValueError("No AWS credentials found for task execution")
        
        # Create execution record
        execution = TaskExecution(
            task_id=task.id,
            status=TaskStatus.RUNNING,
            started_at=datetime.utcnow(),
        )
        db.add(execution)
        await db.commit()
        await db.refresh(execution)
        
        try:
            # Get service class
            service_class = TaskExecutor.SERVICE_MAP.get(task.aws_service_category)
            if not service_class:
                raise ValueError(f"Unknown service category: {task.aws_service_category}")
            
            # Initialize service
            service = service_class(
                access_key_id=credentials.aws_access_key_id,
                secret_access_key=credentials.aws_secret_access_key,
                region=credentials.aws_region or "us-east-1",
            )
            
            # Execute based on task type
            result_data = None
            if task.task_type == "health_check":
                result_data = service.health_check()
            elif task.task_type == "resource_list":
                result_data = service.list_resources(
                    service=task.aws_service,
                    **task.configuration,
                )
            else:
                raise ValueError(f"Unknown task type: {task.task_type}")
            
            # Create result record
            task_result = TaskResult(
                execution_id=execution.id,
                data=result_data,
                metrics={},  # Can add timing metrics here
            )
            db.add(task_result)
            
            # Update execution
            execution.status = TaskStatus.COMPLETED
            execution.completed_at = datetime.utcnow()
            
            await db.commit()
            
            logger.info(
                "task_execution_completed",
                task_id=task_id,
                execution_id=execution.id,
            )
            
        except (AWSAuthenticationError, AWSPermissionError, AWSServiceLimitError) as e:
            # Categorize error
            error_type = type(e).__name__
            execution.status = TaskStatus.FAILED
            execution.error_message = str(e)
            execution.error_type = error_type
            execution.completed_at = datetime.utcnow()
            
            await db.commit()
            
            logger.error(
                "task_execution_failed",
                task_id=task_id,
                execution_id=execution.id,
                error_type=error_type,
                error_message=str(e),
            )
            
            # Re-raise to interrupt execution (no fallback policy)
            raise
            
        except AWSServiceError as e:
            execution.status = TaskStatus.FAILED
            execution.error_message = str(e)
            execution.error_type = "AWSServiceError"
            execution.completed_at = datetime.utcnow()
            
            await db.commit()
            
            logger.error(
                "task_execution_failed",
                task_id=task_id,
                execution_id=execution.id,
                error_type="AWSServiceError",
                error_message=str(e),
            )
            
            raise
            
        except Exception as e:
            execution.status = TaskStatus.FAILED
            execution.error_message = str(e)
            execution.error_type = type(e).__name__
            execution.completed_at = datetime.utcnow()
            
            await db.commit()
            
            logger.error(
                "task_execution_failed",
                task_id=task_id,
                execution_id=execution.id,
                error_type=type(e).__name__,
                error_message=str(e),
                exc_info=True,
            )
            
            raise
        
        return execution
