"""Task management endpoints."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.core.database import get_db
from app.api.dependencies import get_current_active_user
from app.models.user import User
from app.models.task import Task, TaskExecution, TaskResult
from app.schemas.task import (
    TaskCreate,
    TaskUpdate,
    TaskResponse,
    TaskExecutionResponse,
    TaskResultResponse,
)
from app.tasks.executor import TaskExecutor
from app.tasks.celery_tasks import execute_task_async
from app.core.logging import logger

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new task."""
    task = Task(
        user_id=current_user.id,
        **task_data.model_dump(),
    )
    
    db.add(task)
    await db.commit()
    await db.refresh(task)
    
    logger.info("task_created", task_id=task.id, user_id=current_user.id)
    
    return task


@router.get("", response_model=List[TaskResponse])
async def list_tasks(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """List user's tasks."""
    result = await db.execute(
        select(Task)
        .where(Task.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
    )
    tasks = result.scalars().all()
    return tasks


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a specific task."""
    result = await db.execute(
        select(Task).where(
            and_(Task.id == task_id, Task.user_id == current_user.id)
        )
    )
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    
    return task


@router.patch("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Update a task."""
    result = await db.execute(
        select(Task).where(
            and_(Task.id == task_id, Task.user_id == current_user.id)
        )
    )
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    
    # Update fields
    update_data = task_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)
    
    await db.commit()
    await db.refresh(task)
    
    logger.info("task_updated", task_id=task.id, user_id=current_user.id)
    
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a task."""
    result = await db.execute(
        select(Task).where(
            and_(Task.id == task_id, Task.user_id == current_user.id)
        )
    )
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    
    await db.delete(task)
    await db.commit()
    
    logger.info("task_deleted", task_id=task_id, user_id=current_user.id)


@router.post("/{task_id}/execute", response_model=TaskExecutionResponse)
async def execute_task(
    task_id: int,
    aws_credentials_id: Optional[int] = None,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Execute a task immediately."""
    result = await db.execute(
        select(Task).where(
            and_(Task.id == task_id, Task.user_id == current_user.id)
        )
    )
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    
    # Execute task asynchronously
    celery_task = execute_task_async.delay(task_id, aws_credentials_id)
    
    # Create execution record
    from app.models.task import TaskExecution, TaskStatus
    from datetime import datetime
    
    execution = TaskExecution(
        task_id=task.id,
        status=TaskStatus.PENDING,
        celery_task_id=celery_task.id,
    )
    db.add(execution)
    await db.commit()
    await db.refresh(execution)
    
    logger.info(
        "task_execution_triggered",
        task_id=task_id,
        execution_id=execution.id,
        celery_task_id=celery_task.id,
    )
    
    return execution


@router.get("/{task_id}/executions", response_model=List[TaskExecutionResponse])
async def list_task_executions(
    task_id: int,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """List executions for a task."""
    # Verify task ownership
    result = await db.execute(
        select(Task).where(
            and_(Task.id == task_id, Task.user_id == current_user.id)
        )
    )
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )
    
    # Get executions
    result = await db.execute(
        select(TaskExecution)
        .where(TaskExecution.task_id == task_id)
        .order_by(TaskExecution.started_at.desc())
        .offset(skip)
        .limit(limit)
    )
    executions = result.scalars().all()
    return executions


@router.get("/executions/{execution_id}/result", response_model=TaskResultResponse)
async def get_execution_result(
    execution_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get result for a task execution."""
    # Get execution and verify ownership
    result = await db.execute(
        select(TaskExecution).where(TaskExecution.id == execution_id)
    )
    execution = result.scalar_one_or_none()
    
    if not execution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Execution not found",
        )
    
    # Verify task ownership
    result = await db.execute(
        select(Task).where(
            and_(Task.id == execution.task_id, Task.user_id == current_user.id)
        )
    )
    task = result.scalar_one_or_none()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )
    
    # Get result
    result = await db.execute(
        select(TaskResult).where(TaskResult.execution_id == execution_id)
    )
    task_result = result.scalar_one_or_none()
    
    if not task_result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Result not found",
        )
    
    return task_result
