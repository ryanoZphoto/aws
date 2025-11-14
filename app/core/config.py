"""Application configuration."""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    APP_NAME: str = "AWS Automation Platform"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    
    # Redis
    REDIS_URL: str
    REDIS_CELERY_URL: str
    
    # AWS
    AWS_DEFAULT_REGION: str = "us-east-1"
    
    # Security
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    
    # CORS
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"
    
    # Task Execution
    TASK_TIMEOUT_SECONDS: int = 3600
    MAX_CONCURRENT_TASKS: int = 50
    WORKER_POOL_SIZE: int = 10
    
    # CloudWatch
    CLOUDWATCH_LOG_GROUP: str = "/aws/automation-platform"
    CLOUDWATCH_REGION: str = "us-east-1"
    
    # Subscription & Billing
    STRIPE_SECRET_KEY: str = ""
    STRIPE_WEBHOOK_SECRET: str = ""
    
    # Frontend
    FRONTEND_URL: str = "http://localhost:3000"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Convert CORS origins string to list."""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
