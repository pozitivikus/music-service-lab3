from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from uuid import UUID, uuid4
from decimal import Decimal

class SubscriptionPlan(SQLModel, table=True):
    __tablename__ = "subscription_plans"
    plan_id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True, max_length=50)
    price: Decimal = Field(max_digits=10, decimal_places=2)
    description: Optional[str] = Field(default=None)
    payments: List["Payment"] = Relationship(back_populates="plan")

class Payment(SQLModel, table=True):
    __tablename__ = "payments"
    payment_id: Optional[UUID] = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.user_id")
    plan_id: UUID = Field(foreign_key="subscription_plans.plan_id")
    amount: Decimal = Field(max_digits=10, decimal_places=2)
    payment_date: datetime = Field(default_factory=datetime.utcnow)
    status: str = Field(default='pending', max_length=20)
    external_payment_id: Optional[str] = Field(default=None, max_length=255)
    user: "User" = Relationship(back_populates="payments")
    plan: SubscriptionPlan = Relationship(back_populates="payments")