"""AWS credentials schemas."""
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AWSCredentialsBase(BaseModel):
    """Base AWS credentials schema."""
    name: str
    aws_region: str = "us-east-1"
    aws_role_arn: Optional[str] = None
    is_default: bool = False


class AWSCredentialsCreate(AWSCredentialsBase):
    """AWS credentials creation schema."""
    aws_access_key_id: str
    aws_secret_access_key: str


class AWSCredentialsUpdate(BaseModel):
    """AWS credentials update schema."""
    name: Optional[str] = None
    aws_region: Optional[str] = None
    aws_role_arn: Optional[str] = None
    is_default: Optional[bool] = None
    is_active: Optional[bool] = None


class AWSCredentialsResponse(AWSCredentialsBase):
    """AWS credentials response schema (without secrets)."""
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
