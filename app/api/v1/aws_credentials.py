"""AWS credentials management endpoints."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.core.database import get_db
from app.api.dependencies import get_current_active_user
from app.models.user import User
from app.models.aws_credentials import AWSCredentials
from app.schemas.aws_credentials import (
    AWSCredentialsCreate,
    AWSCredentialsUpdate,
    AWSCredentialsResponse,
)
from app.core.logging import logger

router = APIRouter(prefix="/aws-credentials", tags=["aws-credentials"])


@router.post("", response_model=AWSCredentialsResponse, status_code=status.HTTP_201_CREATED)
async def create_aws_credentials(
    creds_data: AWSCredentialsCreate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Create AWS credentials."""
    # If this is set as default, unset other defaults
    if creds_data.is_default:
        result = await db.execute(
            select(AWSCredentials).where(
                and_(
                    AWSCredentials.user_id == current_user.id,
                    AWSCredentials.is_default == True,
                )
            )
        )
        existing_defaults = result.scalars().all()
        for default in existing_defaults:
            default.is_default = False
    
    credentials = AWSCredentials(
        user_id=current_user.id,
        **creds_data.model_dump(),
    )
    
    db.add(credentials)
    await db.commit()
    await db.refresh(credentials)
    
    logger.info(
        "aws_credentials_created",
        credentials_id=credentials.id,
        user_id=current_user.id,
    )
    
    return credentials


@router.get("", response_model=List[AWSCredentialsResponse])
async def list_aws_credentials(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """List user's AWS credentials."""
    result = await db.execute(
        select(AWSCredentials).where(AWSCredentials.user_id == current_user.id)
    )
    credentials = result.scalars().all()
    return credentials


@router.get("/{credentials_id}", response_model=AWSCredentialsResponse)
async def get_aws_credentials(
    credentials_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Get specific AWS credentials."""
    result = await db.execute(
        select(AWSCredentials).where(
            and_(
                AWSCredentials.id == credentials_id,
                AWSCredentials.user_id == current_user.id,
            )
        )
    )
    credentials = result.scalar_one_or_none()
    
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="AWS credentials not found",
        )
    
    return credentials


@router.patch("/{credentials_id}", response_model=AWSCredentialsResponse)
async def update_aws_credentials(
    credentials_id: int,
    creds_data: AWSCredentialsUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Update AWS credentials."""
    result = await db.execute(
        select(AWSCredentials).where(
            and_(
                AWSCredentials.id == credentials_id,
                AWSCredentials.user_id == current_user.id,
            )
        )
    )
    credentials = result.scalar_one_or_none()
    
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="AWS credentials not found",
        )
    
    # If setting as default, unset other defaults
    if creds_data.is_default:
        result = await db.execute(
            select(AWSCredentials).where(
                and_(
                    AWSCredentials.user_id == current_user.id,
                    AWSCredentials.is_default == True,
                    AWSCredentials.id != credentials_id,
                )
            )
        )
        existing_defaults = result.scalars().all()
        for default in existing_defaults:
            default.is_default = False
    
    # Update fields
    update_data = creds_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(credentials, field, value)
    
    await db.commit()
    await db.refresh(credentials)
    
    logger.info(
        "aws_credentials_updated",
        credentials_id=credentials_id,
        user_id=current_user.id,
    )
    
    return credentials


@router.delete("/{credentials_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_aws_credentials(
    credentials_id: int,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete AWS credentials."""
    result = await db.execute(
        select(AWSCredentials).where(
            and_(
                AWSCredentials.id == credentials_id,
                AWSCredentials.user_id == current_user.id,
            )
        )
    )
    credentials = result.scalar_one_or_none()
    
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="AWS credentials not found",
        )
    
    await db.delete(credentials)
    await db.commit()
    
    logger.info(
        "aws_credentials_deleted",
        credentials_id=credentials_id,
        user_id=current_user.id,
    )
