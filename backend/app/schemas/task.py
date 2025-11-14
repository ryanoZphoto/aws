"""
Task schemas
"""
from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel

from app.models.task import TaskFrequency, TaskStatus


class TaskBase(BaseModel):
    name: str
    description: Optional[str] = None
    aws_service: str
    aws_operation: str
    frequency: TaskFrequency = TaskFrequency.DAILY
    is_active: bool = True
    config: Optional[Dict[str, Any]] = None


class TaskCreate(TaskBase):
    aws_credentials_id: Optional[int] = None


class TaskUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    aws_service: Optional[str] = None
    aws_operation: Optional[str] = None
    frequency: Optional[TaskFrequency] = None
    is_active: Optional[bool] = None
    config: Optional[Dict[str, Any]] = None


class Task(TaskBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class TaskResult(BaseModel):
    id: int
    execution_id: int
    data: Dict[str, Any]
    created_at: datetime
    
    class Config:
        from_attributes = True


class TaskExecution(BaseModel):
    id: int
    task_id: int
    status: TaskStatus
    started_at: datetime
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    results: list[TaskResult] = []
    
    class Config:
        from_attributes = True
