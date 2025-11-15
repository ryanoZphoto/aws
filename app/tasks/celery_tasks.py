"""Celery task definitions."""
from celery import Task
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import AsyncSessionLocal
from app.tasks.executor import TaskExecutor
from app.core.celery_app import celery_app
from app.core.logging import logger


class DatabaseTask(Task):
    """Base task class with database session."""
    _db: AsyncSession = None
    
    @property
    def db(self):
        """Get database session."""
        if self._db is None:
            self._db = AsyncSessionLocal()
        return self._db
    
    def after_return(self, *args, **kwargs):
        """Close database session after task completion."""
        if self._db:
            self._db.close()
            self._db = None


@celery_app.task(bind=True, base=DatabaseTask)
def execute_task_async(self, task_id: int, aws_credentials_id: int = None):
    """
    Execute a task asynchronously via Celery.
    
    Args:
        task_id: Task ID to execute
        aws_credentials_id: Optional AWS credentials ID
    """
    import asyncio
    
    async def _execute():
        async with AsyncSessionLocal() as db:
            try:
                execution = await TaskExecutor.execute_task(
                    db=db,
                    task_id=task_id,
                    aws_credentials_id=aws_credentials_id,
                )
                logger.info(
                    "celery_task_completed",
                    task_id=task_id,
                    execution_id=execution.id,
                    celery_task_id=self.request.id,
                )
                return {
                    "status": "success",
                    "execution_id": execution.id,
                }
            except Exception as e:
                logger.error(
                    "celery_task_failed",
                    task_id=task_id,
                    celery_task_id=self.request.id,
                    error=str(e),
                    exc_info=True,
                )
                # Re-raise to mark task as failed (no fallback)
                raise
    
    return asyncio.run(_execute())


@celery_app.task
def execute_daily_tasks_sync():
    """Synchronous wrapper for daily task execution."""
    from app.tasks.scheduler import execute_daily_tasks_sync as _execute_daily
    _execute_daily()
