"""Celery application configuration."""
from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "aws_automation",
    broker=settings.REDIS_CELERY_URL,
    backend=settings.REDIS_CELERY_URL,
    include=["app.tasks"],
)

# Celery configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=settings.TASK_TIMEOUT_SECONDS,
    worker_prefetch_multiplier=1,
    worker_max_tasks_per_child=1000,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    task_routes={
        "app.tasks.*": {"queue": "default"},
    },
    beat_schedule={
        "daily-task-execution": {
            "task": "app.tasks.celery_tasks.execute_daily_tasks_sync",
            "schedule": 86400.0,  # 24 hours
        },
    },
)
