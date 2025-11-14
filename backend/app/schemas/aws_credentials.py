"""
AWS Credentials schemas
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class AWSCredentialsBase(BaseModel):
    name: str
    aws_region: str = "us-east-1"
    is_default: bool = False
    iam_role_arn: Optional[str] = None


class AWSCredentialsCreate(AWSCredentialsBase):
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_session_token: Optional[str] = None


class AWSCredentialsUpdate(BaseModel):
    name: Optional[str] = None
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_session_token: Optional[str] = None
    aws_region: Optional[str] = None
    is_default: Optional[bool] = None
    iam_role_arn: Optional[str] = None


class AWSCredentials(AWSCredentialsBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
