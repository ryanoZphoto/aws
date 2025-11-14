"""
AWS Credentials endpoints
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import encrypt_aws_credentials
from app.models.user import User
from app.models.aws_credentials import AWSCredentials
from app.schemas.aws_credentials import (
    AWSCredentials as AWSCredentialsSchema,
    AWSCredentialsCreate,
    AWSCredentialsUpdate
)
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()


@router.post("/", response_model=AWSCredentialsSchema, status_code=status.HTTP_201_CREATED)
def create_aws_credentials(
    credentials: AWSCredentialsCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create AWS credentials"""
    # If this is set as default, unset other defaults
    if credentials.is_default:
        db.query(AWSCredentials).filter(
            AWSCredentials.user_id == current_user.id,
            AWSCredentials.is_default == True
        ).update({"is_default": False})
    
    # Encrypt credentials
    encrypted_data = {
        "user_id": current_user.id,
        "name": credentials.name,
        "aws_region": credentials.aws_region,
        "is_default": credentials.is_default,
        "iam_role_arn": credentials.iam_role_arn,
    }
    
    if credentials.aws_access_key_id:
        encrypted_data["aws_access_key_id"] = encrypt_aws_credentials(credentials.aws_access_key_id)
    if credentials.aws_secret_access_key:
        encrypted_data["aws_secret_access_key"] = encrypt_aws_credentials(credentials.aws_secret_access_key)
    if credentials.aws_session_token:
        encrypted_data["aws_session_token"] = encrypt_aws_credentials(credentials.aws_session_token)
    
    db_credentials = AWSCredentials(**encrypted_data)
    db.add(db_credentials)
    db.commit()
    db.refresh(db_credentials)
    return db_credentials


@router.get("/", response_model=List[AWSCredentialsSchema])
def list_aws_credentials(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List all AWS credentials for current user"""
    credentials = db.query(AWSCredentials).filter(
        AWSCredentials.user_id == current_user.id
    ).all()
    return credentials


@router.get("/{credentials_id}", response_model=AWSCredentialsSchema)
def get_aws_credentials(
    credentials_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific AWS credentials"""
    credentials = db.query(AWSCredentials).filter(
        AWSCredentials.id == credentials_id,
        AWSCredentials.user_id == current_user.id
    ).first()
    if not credentials:
        raise HTTPException(status_code=404, detail="AWS credentials not found")
    return credentials


@router.put("/{credentials_id}", response_model=AWSCredentialsSchema)
def update_aws_credentials(
    credentials_id: int,
    credentials_update: AWSCredentialsUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update AWS credentials"""
    credentials = db.query(AWSCredentials).filter(
        AWSCredentials.id == credentials_id,
        AWSCredentials.user_id == current_user.id
    ).first()
    if not credentials:
        raise HTTPException(status_code=404, detail="AWS credentials not found")
    
    update_data = credentials_update.dict(exclude_unset=True)
    
    # Encrypt credentials if provided
    if "aws_access_key_id" in update_data and update_data["aws_access_key_id"]:
        update_data["aws_access_key_id"] = encrypt_aws_credentials(update_data["aws_access_key_id"])
    if "aws_secret_access_key" in update_data and update_data["aws_secret_access_key"]:
        update_data["aws_secret_access_key"] = encrypt_aws_credentials(update_data["aws_secret_access_key"])
    if "aws_session_token" in update_data and update_data["aws_session_token"]:
        update_data["aws_session_token"] = encrypt_aws_credentials(update_data["aws_session_token"])
    
    # If setting as default, unset other defaults
    if update_data.get("is_default") is True:
        db.query(AWSCredentials).filter(
            AWSCredentials.user_id == current_user.id,
            AWSCredentials.is_default == True,
            AWSCredentials.id != credentials_id
        ).update({"is_default": False})
    
    for field, value in update_data.items():
        setattr(credentials, field, value)
    
    db.commit()
    db.refresh(credentials)
    return credentials


@router.delete("/{credentials_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_aws_credentials(
    credentials_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete AWS credentials"""
    credentials = db.query(AWSCredentials).filter(
        AWSCredentials.id == credentials_id,
        AWSCredentials.user_id == current_user.id
    ).first()
    if not credentials:
        raise HTTPException(status_code=404, detail="AWS credentials not found")
    
    db.delete(credentials)
    db.commit()
    return None
