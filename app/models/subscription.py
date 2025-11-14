"""Subscription models."""
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from app.core.database import Base


class SubscriptionStatus(str, enum.Enum):
    """Subscription status."""
    ACTIVE = "active"
    CANCELLED = "cancelled"
    EXPIRED = "expired"
    SUSPENDED = "suspended"


class SubscriptionPlan(Base):
    """Subscription plan model."""
    __tablename__ = "subscription_plans"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    price_monthly = Column(Integer, nullable=False)  # in cents
    price_yearly = Column(Integer, nullable=True)  # in cents
    max_tasks_per_day = Column(Integer, nullable=False)
    max_concurrent_tasks = Column(Integer, nullable=False)
    aws_service_categories = Column(JSON, nullable=False)  # List of allowed service categories
    features = Column(JSON, nullable=True)  # List of feature flags
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Subscription(Base):
    """Subscription model."""
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    plan_id = Column(Integer, ForeignKey("subscription_plans.id"), nullable=False)
    status = Column(Enum(SubscriptionStatus), default=SubscriptionStatus.ACTIVE)
    stripe_subscription_id = Column(String(255), unique=True, nullable=True)
    stripe_customer_id = Column(String(255), nullable=True)
    current_period_start = Column(DateTime(timezone=True), nullable=False)
    current_period_end = Column(DateTime(timezone=True), nullable=False)
    cancel_at_period_end = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="subscriptions")
    plan = relationship("SubscriptionPlan")
