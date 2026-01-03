"""
Payment Pydantic models
"""

from datetime import datetime
from typing import Optional
from enum import Enum
from pydantic import BaseModel
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
