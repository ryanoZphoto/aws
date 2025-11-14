"""Task scheduler for daily task execution."""
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy import select, and_
from app.core.database import AsyncSessionLocal
from app.core.config import settings
from app.models.task import Task, TaskFrequency
from app.tasks.executor import TaskExecutor
from app.tasks.celery_tasks import execute_task_async
from app.core.logging import logger


async def execute_daily_tasks():
    """Execute all daily tasks."""
    async with AsyncSessionLocal() as db:
        # Get all active daily tasks
        result = await db.execute(
            select(Task).where(
                and_(
                    Task.is_active == True,
                    Task.frequency == TaskFrequency.DAILY,
                )
            )
        )
        tasks = result.scalars().all()
        
        logger.info(
            "daily_task_execution_started",
            task_count=len(tasks),
        )
        
        for task in tasks:
            try:
                # Queue task for async execution
                execute_task_async.delay(task.id)
                logger.info(
                    "task_queued",
                    task_id=task.id,
                    task_name=task.name,
                )
            except Exception as e:
                logger.error(
                    "task_queue_failed",
                    task_id=task.id,
                    error=str(e),
                    exc_info=True,
                )


def execute_daily_tasks_sync():
    """Synchronous wrapper for Celery beat."""
    import asyncio
    asyncio.run(execute_daily_tasks())
