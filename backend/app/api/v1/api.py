"""
Main API router
"""
from fastapi import APIRouter

from app.api.v1.endpoints import auth, tasks, aws_credentials, subscriptions, users

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])
api_router.include_router(aws_credentials.router, prefix="/aws-credentials", tags=["aws-credentials"])
api_router.include_router(subscriptions.router, prefix="/subscriptions", tags=["subscriptions"])
