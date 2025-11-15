"""Task models."""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base


class TaskStatus(str, enum.Enum):
    """Task execution status."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskFrequency(str, enum.Enum):
    """Task execution frequency."""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    ON_DEMAND = "on_demand"


class Task(Base):
    """Task definition model."""
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    aws_service_category = Column(String(100), nullable=False)  # e.g., "compute", "storage"
    aws_service = Column(String(100), nullable=False)  # e.g., "ec2", "s3"
    task_type = Column(String(100), nullable=False)  # e.g., "health_check", "resource_list", "cost_analysis"
    configuration = Column(JSON, nullable=False)  # Task-specific configuration
    frequency = Column(Enum(TaskFrequency), default=TaskFrequency.DAILY)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="tasks")
    executions = relationship("TaskExecution", back_populates="task", cascade="all, delete-orphan")


class TaskExecution(Base):
    """Task execution record."""
    __tablename__ = "task_executions"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    error_message = Column(Text, nullable=True)
    error_type = Column(String(100), nullable=True)  # e.g., "AuthenticationError", "PermissionError"
    celery_task_id = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    task = relationship("Task", back_populates="executions")
    result = relationship("TaskResult", back_populates="execution", uselist=False, cascade="all, delete-orphan")


class TaskResult(Base):
    """Task execution result."""
    __tablename__ = "task_results"
    
    id = Column(Integer, primary_key=True, index=True)
    execution_id = Column(Integer, ForeignKey("task_executions.id"), unique=True, nullable=False)
    data = Column(JSON, nullable=True)  # Result data
    metrics = Column(JSON, nullable=True)  # Performance metrics
    aws_request_id = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    execution = relationship("TaskExecution", back_populates="result")
