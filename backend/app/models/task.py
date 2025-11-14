"""
Task models for scheduling and execution
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, JSON, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.core.database import Base


class TaskStatus(str, enum.Enum):
    """Task execution status"""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"


class TaskFrequency(str, enum.Enum):
    """Task execution frequency"""
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    ON_DEMAND = "on_demand"


class Task(Base):
    """Task model for scheduled AWS service checks"""
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    aws_service = Column(String, nullable=False)  # e.g., "ec2", "s3", "lambda"
    aws_operation = Column(String, nullable=False)  # e.g., "describe_instances", "list_buckets"
    frequency = Column(SQLEnum(TaskFrequency), nullable=False, default=TaskFrequency.DAILY)
    is_active = Column(Boolean, default=True)
    config = Column(JSON, nullable=True)  # Additional configuration for the task
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="tasks")
    executions = relationship("TaskExecution", back_populates="task", cascade="all, delete-orphan")


class TaskExecution(Base):
    """Task execution record"""
    __tablename__ = "task_executions"
    
    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    status = Column(SQLEnum(TaskStatus), nullable=False, default=TaskStatus.PENDING)
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)
    
    # Relationships
    task = relationship("Task", back_populates="executions")
    results = relationship("TaskResult", back_populates="execution", cascade="all, delete-orphan")


class TaskResult(Base):
    """Task execution result data"""
    __tablename__ = "task_results"
    
    id = Column(Integer, primary_key=True, index=True)
    execution_id = Column(Integer, ForeignKey("task_executions.id"), nullable=False)
    data = Column(JSON, nullable=False)  # Actual result data from AWS
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    execution = relationship("TaskExecution", back_populates="results")
