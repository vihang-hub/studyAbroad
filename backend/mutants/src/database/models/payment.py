"""
Payment Model

SQLAlchemy model for payments table.
Maps to data-model.md payments table schema.
"""

from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, DateTime, ForeignKey, Text, func, Enum as SQLEnum, Numeric
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column
from database.models.user import Base
import uuid
import enum
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg is not None:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


class PaymentStatus(str, enum.Enum):
    """Payment status enumeration"""

    PENDING = "pending"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    REFUNDED = "refunded"


class Payment(Base):
    """
    Payment Model

    Represents Stripe payment transactions.

    Columns:
        payment_id: Internal unique identifier
        user_id: Paying user (foreign key)
        report_id: Associated report (nullable until report created)
        stripe_checkout_session_id: Stripe Checkout Session ID
        stripe_payment_intent_id: Stripe Payment Intent ID
        amount_gbp: Payment amount (£2.99 fixed)
        currency: Always 'GBP'
        status: Payment state
        payment_method: How user paid (card, Apple Pay, Google Pay)
        stripe_customer_id: Stripe customer ID
        refund_reason: Explanation if refunded
        created_at: When checkout session created
        succeeded_at: When payment succeeded
        refunded_at: When refund issued
        payment_metadata: Additional Stripe data
    """

    __tablename__ = "payments"

    payment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False
    )
    report_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("reports.report_id", ondelete="SET NULL"), nullable=True
    )
    stripe_checkout_session_id: Mapped[str] = mapped_column(
        String, unique=True, nullable=False, index=True
    )
    stripe_payment_intent_id: Mapped[str | None] = mapped_column(
        String, unique=True, nullable=True, index=True
    )
    amount_gbp: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), default=Decimal("2.99"), nullable=False
    )
    currency: Mapped[str] = mapped_column(String(3), default="GBP", nullable=False)
    status: Mapped[PaymentStatus] = mapped_column(
        SQLEnum(PaymentStatus, name="payment_status"), default=PaymentStatus.PENDING, nullable=False
    )
    payment_method: Mapped[str | None] = mapped_column(String, nullable=True)
    stripe_customer_id: Mapped[str | None] = mapped_column(String, nullable=True)
    refund_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    succeeded_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    refunded_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    payment_metadata: Mapped[dict | None] = mapped_column("metadata", JSONB, nullable=True)

    def __repr__(self) -> str:
        return f"<Payment(payment_id={self.payment_id}, amount={self.amount_gbp}, status={self.status})>"
