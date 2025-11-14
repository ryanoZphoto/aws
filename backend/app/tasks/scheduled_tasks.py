"""
Scheduled tasks for daily AWS service checks
"""
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.task import Task, TaskFrequency
from app.tasks.executor import TaskExecutor
from app.tasks.celery_app import celery_app


@celery_app.task(name="execute_daily_tasks")
def execute_daily_tasks():
    """Execute all daily tasks"""
    db: Session = SessionLocal()
    try:
        tasks = db.query(Task).filter(
            Task.is_active == True,
            Task.frequency == TaskFrequency.DAILY
        ).all()
        
        executor = TaskExecutor(db)
        results = []
        
        for task in tasks:
            try:
                execution = executor.execute_task(task)
                results.append({
                    "task_id": task.id,
                    "execution_id": execution.id,
                    "status": execution.status.value,
                    "success": True
                })
            except Exception as e:
                results.append({
                    "task_id": task.id,
                    "status": "failed",
                    "error": str(e),
                    "success": False
                })
        
        return results
    finally:
        db.close()


@celery_app.task(name="execute_weekly_tasks")
def execute_weekly_tasks():
    """Execute all weekly tasks"""
    db: Session = SessionLocal()
    try:
        tasks = db.query(Task).filter(
            Task.is_active == True,
            Task.frequency == TaskFrequency.WEEKLY
        ).all()
        
        executor = TaskExecutor(db)
        results = []
        
        for task in tasks:
            try:
                execution = executor.execute_task(task)
                results.append({
                    "task_id": task.id,
                    "execution_id": execution.id,
                    "status": execution.status.value,
                    "success": True
                })
            except Exception as e:
                results.append({
                    "task_id": task.id,
                    "status": "failed",
                    "error": str(e),
                    "success": False
                })
        
        return results
    finally:
        db.close()


@celery_app.task(name="execute_monthly_tasks")
def execute_monthly_tasks():
    """Execute all monthly tasks"""
    db: Session = SessionLocal()
    try:
        tasks = db.query(Task).filter(
            Task.is_active == True,
            Task.frequency == TaskFrequency.MONTHLY
        ).all()
        
        executor = TaskExecutor(db)
        results = []
        
        for task in tasks:
            try:
                execution = executor.execute_task(task)
                results.append({
                    "task_id": task.id,
                    "execution_id": execution.id,
                    "status": execution.status.value,
                    "success": True
                })
            except Exception as e:
                results.append({
                    "task_id": task.id,
                    "status": "failed",
                    "error": str(e),
                    "success": False
                })
        
        return results
    finally:
        db.close()


# Celery beat schedule
celery_app.conf.beat_schedule = {
    "execute-daily-tasks": {
        "task": "execute_daily_tasks",
        "schedule": timedelta(days=1),
        "options": {"timezone": "UTC"}
    },
    "execute-weekly-tasks": {
        "task": "execute_weekly_tasks",
        "schedule": timedelta(weeks=1),
        "options": {"timezone": "UTC"}
    },
    "execute-monthly-tasks": {
        "task": "execute_monthly_tasks",
        "schedule": timedelta(days=30),
        "options": {"timezone": "UTC"}
    },
}
