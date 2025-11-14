"""
Subscription endpoints
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.models.subscription import Subscription
from app.schemas.subscription import (
    Subscription as SubscriptionSchema,
    SubscriptionCreate,
    SubscriptionUpdate
)
from app.api.v1.endpoints.auth import get_current_user

router = APIRouter()


@router.get("/", response_model=SubscriptionSchema)
def get_subscription(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user's subscription"""
    subscription = db.query(Subscription).filter(
        Subscription.user_id == current_user.id
    ).first()
    
    if not subscription:
        # Create default free subscription
        subscription = Subscription(
            user_id=current_user.id,
            tier="free",
            status="trialing"
        )
        db.add(subscription)
        db.commit()
        db.refresh(subscription)
    
    return subscription


@router.put("/", response_model=SubscriptionSchema)
def update_subscription(
    subscription_update: SubscriptionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update subscription"""
    subscription = db.query(Subscription).filter(
        Subscription.user_id == current_user.id
    ).first()
    
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    
    update_data = subscription_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(subscription, field, value)
    
    db.commit()
    db.refresh(subscription)
    return subscription
