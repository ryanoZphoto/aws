"""
AWS Credentials model for secure storage
"""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class AWSCredentials(Base):
    """AWS credentials model for secure storage"""
    __tablename__ = "aws_credentials"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String, nullable=False)  # User-friendly name for the credential set
    aws_access_key_id = Column(String, nullable=True)  # Encrypted
    aws_secret_access_key = Column(Text, nullable=True)  # Encrypted
    aws_session_token = Column(Text, nullable=True)  # Encrypted (for temporary credentials)
    aws_region = Column(String, default="us-east-1")
    iam_role_arn = Column(String, nullable=True)  # For IAM role assumption
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="aws_credentials")
