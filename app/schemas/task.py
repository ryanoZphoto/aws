"""Task schemas."""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any
from app.models.task import TaskFrequency, TaskStatus


class TaskBase(BaseModel):
    """Base task schema."""
    name: str
    description: Optional[str] = None
    aws_service_category: str
    aws_service: str
    task_type: str
    configuration: Dict[str, Any]
    frequency: TaskFrequency = TaskFrequency.DAILY


class TaskCreate(TaskBase):
    """Task creation schema."""
    pass


class TaskUpdate(BaseModel):
    """Task update schema."""
    name: Optional[str] = None
    description: Optional[str] = None
    configuration: Optional[Dict[str, Any]] = None
    is_active: Optional[bool] = None
    frequency: Optional[TaskFrequency] = None


class TaskResponse(TaskBase):
    """Task response schema."""
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class TaskExecutionResponse(BaseModel):
    """Task execution response schema."""
    id: int
    task_id: int
    status: TaskStatus
    started_at: datetime
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    error_type: Optional[str] = None
    
    class Config:
        from_attributes = True


class TaskResultResponse(BaseModel):
    """Task result response schema."""
    id: int
    execution_id: int
    data: Optional[Dict[str, Any]] = None
    metrics: Optional[Dict[str, Any]] = None
    created_at: datetime
    
    class Config:
        from_attributes = True
