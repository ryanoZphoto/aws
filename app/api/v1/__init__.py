"""API v1 routes."""
from fastapi import APIRouter
from app.api.v1 import auth, tasks, aws_credentials

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/api/v1")
api_router.include_router(tasks.router, prefix="/api/v1")
api_router.include_router(aws_credentials.router, prefix="/api/v1")
