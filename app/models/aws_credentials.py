"""AWS credentials model."""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy_utils import EncryptedType
from sqlalchemy_utils.types.encrypted.encrypted_type import AesEngine
from app.core.database import Base
from app.core.config import settings


class AWSCredentials(Base):
    """AWS credentials model (encrypted)."""
    __tablename__ = "aws_credentials"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    name = Column(String(255), nullable=False)  # User-friendly name
    aws_access_key_id = Column(
        EncryptedType(String(255), settings.SECRET_KEY, AesEngine, "pkcs5"),
        nullable=False
    )
    aws_secret_access_key = Column(
        EncryptedType(String(255), settings.SECRET_KEY, AesEngine, "pkcs5"),
        nullable=False
    )
    aws_region = Column(String(50), default="us-east-1")
    aws_role_arn = Column(String(500), nullable=True)  # For role-based access
    is_default = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="aws_credentials")
