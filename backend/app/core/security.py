"""
Security utilities for authentication and encryption
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from cryptography.fernet import Fernet
import base64
import os

from app.core.config import settings

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Encryption for AWS credentials
def get_encryption_key() -> bytes:
    """Get or generate encryption key for AWS credentials"""
    key = os.getenv("ENCRYPTION_KEY")
    if not key:
        # In production, this MUST be set via environment variable
        raise ValueError(
            "ENCRYPTION_KEY environment variable is required. "
            "Generate one with: python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())'"
        )
    
    # Validate key format (should be 44 characters for base64-encoded 32 bytes)
    if len(key) != 44:
        raise ValueError(
            f"ENCRYPTION_KEY must be 44 characters (base64-encoded 32 bytes). "
            f"Current length: {len(key)}. Generate with: "
            "python -c 'from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())'"
        )
    
    try:
        # Validate it's a valid Fernet key
        Fernet(key.encode())
    except Exception as e:
        raise ValueError(f"Invalid ENCRYPTION_KEY format: {e}")
    
    return key.encode()

cipher_suite = Fernet(get_encryption_key())


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Decode and verify a JWT token"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None


def encrypt_aws_credentials(credentials: str) -> str:
    """Encrypt AWS credentials for storage"""
    return cipher_suite.encrypt(credentials.encode()).decode()


def decrypt_aws_credentials(encrypted_credentials: str) -> str:
    """Decrypt AWS credentials for use"""
    return cipher_suite.decrypt(encrypted_credentials.encode()).decode()
