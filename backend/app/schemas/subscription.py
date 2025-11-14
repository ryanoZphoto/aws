"""
Subscription schemas
"""
from typing import Optional
from datetime import datetime
from pydantic import BaseModel

from app.models.subscription import SubscriptionTier, SubscriptionStatus


class SubscriptionBase(BaseModel):
    tier: SubscriptionTier = SubscriptionTier.FREE
    status: SubscriptionStatus = SubscriptionStatus.TRIALING


class SubscriptionCreate(SubscriptionBase):
    stripe_customer_id: Optional[str] = None


class SubscriptionUpdate(BaseModel):
    tier: Optional[SubscriptionTier] = None
    status: Optional[SubscriptionStatus] = None
    stripe_subscription_id: Optional[str] = None
    cancel_at_period_end: Optional[bool] = None


class Subscription(SubscriptionBase):
    id: int
    user_id: int
    stripe_subscription_id: Optional[str] = None
    stripe_customer_id: Optional[str] = None
    current_period_start: Optional[datetime] = None
    current_period_end: Optional[datetime] = None
    cancel_at_period_end: bool = False
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
