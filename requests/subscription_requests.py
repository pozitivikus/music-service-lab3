from sqlmodel import Session, select, func
from typing import List, Optional
from datetime import date, timedelta
from decimal import Decimal
from models.subscription_models import SubscriptionPlan, Payment
from models.user_models import User
import uuid

class SubscriptionRequests:
    @staticmethod
    def create_subscription_plan(session: Session, name: str, price: Decimal,
                                description: Optional[str] = None) -> SubscriptionPlan:
        plan = SubscriptionPlan(
            name=name,
            price=price,
            description=description
        )
        session.add(plan)
        session.commit()
        session.refresh(plan)
        return plan
    
    @staticmethod
    def create_payment(session: Session, user_id: uuid.UUID, plan_id: uuid.UUID,
                      amount: Decimal, status: str = "completed",
                      external_payment_id: Optional[str] = None) -> Payment:
        payment = Payment(
            user_id=user_id,
            plan_id=plan_id,
            amount=amount,
            status=status,
            external_payment_id=external_payment_id
        )
        session.add(payment)
        session.commit()
        session.refresh(payment)
        return payment
    
    @staticmethod
    def get_all_plans(session: Session) -> List[SubscriptionPlan]:
        statement = select(SubscriptionPlan)
        return session.exec(statement).all()
    
    @staticmethod
    def get_user_payments(session: Session, user_id: uuid.UUID,
                         limit: int = 20) -> List[Payment]:
        statement = (
            select(Payment)
            .where(Payment.user_id == user_id)
            .order_by(Payment.payment_date.desc())
            .limit(limit)
        )
        return session.exec(statement).all()
    
    @staticmethod
    def activate_premium(session: Session, user_id: uuid.UUID,
                        plan_id: uuid.UUID, payment_id: uuid.UUID) -> Optional[User]:
        plan = session.get(SubscriptionPlan, plan_id)
        if not plan:
            return None
        user = session.get(User, user_id)
        if user:
            user.subscription_type = "premium"
            user.subscription_expiry = date.today() + timedelta(days=30) 
            
            payment = session.get(Payment, payment_id)
            if payment:
                payment.status = "completed"
            
            session.add(user)
            session.commit()
            session.refresh(user)
        return user
    
    @staticmethod
    def get_revenue_by_period(session: Session, start_date: date,
                             end_date: date) -> Decimal:
        statement = (
            select(func.sum(Payment.amount))
            .where(
                Payment.status == "completed",
                func.date(Payment.payment_date) >= start_date,
                func.date(Payment.payment_date) <= end_date
            )
        )
        result = session.exec(statement).first()
        return result or Decimal('0')
    
    @staticmethod
    def get_most_popular_plan(session: Session) -> Optional[SubscriptionPlan]:
        statement = (
            select(SubscriptionPlan, func.count(Payment.payment_id).label("purchase_count"))
            .join(Payment, SubscriptionPlan.plan_id == Payment.plan_id)
            .where(Payment.status == "completed")
            .group_by(SubscriptionPlan.plan_id)
            .order_by(func.count(Payment.payment_id).desc())
        )
        result = session.exec(statement).first()
        return result[0] if result else None