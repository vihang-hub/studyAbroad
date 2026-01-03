"""
Payment Pydantic models
"""

from datetime import datetime
from typing import Optional
from enum import Enum
from pydantic import BaseModel


class PaymentStatus(str, Enum):
    """Payment status (Stripe)"""

    PENDING = "pending"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    REFUNDED = "refunded"


class Payment(BaseModel):
    """Payment model"""

    id: str
    user_id: str
    report_id: str
    stripe_payment_intent_id: str
    amount: int  # In pence
    currency: str = "gbp"
    status: PaymentStatus
    error_message: Optional[str] = None
    refunded_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CreateCheckoutRequest(BaseModel):
    """Request to create a checkout session"""

    report_id: Optional[str] = None
    query: Optional[str] = None


class CreateCheckoutResponse(BaseModel):
    """Response with Stripe checkout details"""

    client_secret: str
    payment_intent_id: str
    amount: int
    currency: str


class PaymentIntentStatus(BaseModel):
    """Payment intent status check"""

    payment_intent_id: str
    status: PaymentStatus
    report_id: Optional[str] = None
