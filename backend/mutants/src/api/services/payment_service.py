"""
Payment service for Stripe integration
Handles checkout session creation and webhook processing
"""

import stripe
from datetime import datetime
from typing import Optional
from src.config import settings
from src.lib.supabase import get_supabase
from src.api.models.payment import Payment, PaymentStatus, CreateCheckoutResponse

# Initialize Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY
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


async def x_create_checkout_session__mutmut_orig(
    user_id: str, report_id: str, query: str
) -> CreateCheckoutResponse:
    """
    Create Stripe payment intent for report generation
    Returns client secret for frontend Stripe Elements
    """
    try:
        # Create Stripe Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
            metadata={
                "user_id": user_id,
                "report_id": report_id,
                "query": query,
            },
            automatic_payment_methods={"enabled": True},
        )

        # Create Payment record in database
        supabase = get_supabase()
        payment_data = {
            "user_id": user_id,
            "report_id": report_id,
            "stripe_payment_intent_id": payment_intent.id,
            "amount": settings.STRIPE_PRICE_AMOUNT,
            "currency": settings.STRIPE_CURRENCY,
            "status": PaymentStatus.PENDING.value,
        }

        supabase.table("payments").insert(payment_data).execute()

        return CreateCheckoutResponse(
            client_secret=payment_intent.client_secret,
            payment_intent_id=payment_intent.id,
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
        )

    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


async def x_create_checkout_session__mutmut_1(
    user_id: str, report_id: str, query: str
) -> CreateCheckoutResponse:
    """
    Create Stripe payment intent for report generation
    Returns client secret for frontend Stripe Elements
    """
    try:
        # Create Stripe Payment Intent
        payment_intent = None

        # Create Payment record in database
        supabase = get_supabase()
        payment_data = {
            "user_id": user_id,
            "report_id": report_id,
            "stripe_payment_intent_id": payment_intent.id,
            "amount": settings.STRIPE_PRICE_AMOUNT,
            "currency": settings.STRIPE_CURRENCY,
            "status": PaymentStatus.PENDING.value,
        }

        supabase.table("payments").insert(payment_data).execute()

        return CreateCheckoutResponse(
            client_secret=payment_intent.client_secret,
            payment_intent_id=payment_intent.id,
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
        )

    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


async def x_create_checkout_session__mutmut_2(
    user_id: str, report_id: str, query: str
) -> CreateCheckoutResponse:
    """
    Create Stripe payment intent for report generation
    Returns client secret for frontend Stripe Elements
    """
    try:
        # Create Stripe Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=None,
            currency=settings.STRIPE_CURRENCY,
            metadata={
                "user_id": user_id,
                "report_id": report_id,
                "query": query,
            },
            automatic_payment_methods={"enabled": True},
        )

        # Create Payment record in database
        supabase = get_supabase()
        payment_data = {
            "user_id": user_id,
            "report_id": report_id,
            "stripe_payment_intent_id": payment_intent.id,
            "amount": settings.STRIPE_PRICE_AMOUNT,
            "currency": settings.STRIPE_CURRENCY,
            "status": PaymentStatus.PENDING.value,
        }

        supabase.table("payments").insert(payment_data).execute()

        return CreateCheckoutResponse(
            client_secret=payment_intent.client_secret,
            payment_intent_id=payment_intent.id,
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
        )

    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


async def x_create_checkout_session__mutmut_3(
    user_id: str, report_id: str, query: str
) -> CreateCheckoutResponse:
    """
    Create Stripe payment intent for report generation
    Returns client secret for frontend Stripe Elements
    """
    try:
        # Create Stripe Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=None,
            metadata={
                "user_id": user_id,
                "report_id": report_id,
                "query": query,
            },
            automatic_payment_methods={"enabled": True},
        )

        # Create Payment record in database
        supabase = get_supabase()
        payment_data = {
            "user_id": user_id,
            "report_id": report_id,
            "stripe_payment_intent_id": payment_intent.id,
            "amount": settings.STRIPE_PRICE_AMOUNT,
            "currency": settings.STRIPE_CURRENCY,
            "status": PaymentStatus.PENDING.value,
        }

        supabase.table("payments").insert(payment_data).execute()

        return CreateCheckoutResponse(
            client_secret=payment_intent.client_secret,
            payment_intent_id=payment_intent.id,
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
        )

    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


async def x_create_checkout_session__mutmut_4(
    user_id: str, report_id: str, query: str
) -> CreateCheckoutResponse:
    """
    Create Stripe payment intent for report generation
    Returns client secret for frontend Stripe Elements
    """
    try:
        # Create Stripe Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
            metadata=None,
            automatic_payment_methods={"enabled": True},
        )

        # Create Payment record in database
        supabase = get_supabase()
        payment_data = {
            "user_id": user_id,
            "report_id": report_id,
            "stripe_payment_intent_id": payment_intent.id,
            "amount": settings.STRIPE_PRICE_AMOUNT,
            "currency": settings.STRIPE_CURRENCY,
            "status": PaymentStatus.PENDING.value,
        }

        supabase.table("payments").insert(payment_data).execute()

        return CreateCheckoutResponse(
            client_secret=payment_intent.client_secret,
            payment_intent_id=payment_intent.id,
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
        )

    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


async def x_create_checkout_session__mutmut_5(
    user_id: str, report_id: str, query: str
) -> CreateCheckoutResponse:
    """
    Create Stripe payment intent for report generation
    Returns client secret for frontend Stripe Elements
    """
    try:
        # Create Stripe Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
            metadata={
                "user_id": user_id,
                "report_id": report_id,
                "query": query,
            },
            automatic_payment_methods=None,
        )

        # Create Payment record in database
        supabase = get_supabase()
        payment_data = {
            "user_id": user_id,
            "report_id": report_id,
            "stripe_payment_intent_id": payment_intent.id,
            "amount": settings.STRIPE_PRICE_AMOUNT,
            "currency": settings.STRIPE_CURRENCY,
            "status": PaymentStatus.PENDING.value,
        }

        supabase.table("payments").insert(payment_data).execute()

        return CreateCheckoutResponse(
            client_secret=payment_intent.client_secret,
            payment_intent_id=payment_intent.id,
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
        )

    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


async def x_create_checkout_session__mutmut_6(
    user_id: str, report_id: str, query: str
) -> CreateCheckoutResponse:
    """
    Create Stripe payment intent for report generation
    Returns client secret for frontend Stripe Elements
    """
    try:
        # Create Stripe Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            currency=settings.STRIPE_CURRENCY,
            metadata={
                "user_id": user_id,
                "report_id": report_id,
                "query": query,
            },
            automatic_payment_methods={"enabled": True},
        )

        # Create Payment record in database
        supabase = get_supabase()
        payment_data = {
            "user_id": user_id,
            "report_id": report_id,
            "stripe_payment_intent_id": payment_intent.id,
            "amount": settings.STRIPE_PRICE_AMOUNT,
            "currency": settings.STRIPE_CURRENCY,
            "status": PaymentStatus.PENDING.value,
        }

        supabase.table("payments").insert(payment_data).execute()

        return CreateCheckoutResponse(
            client_secret=payment_intent.client_secret,
            payment_intent_id=payment_intent.id,
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
        )

    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


async def x_create_checkout_session__mutmut_7(
    user_id: str, report_id: str, query: str
) -> CreateCheckoutResponse:
    """
    Create Stripe payment intent for report generation
    Returns client secret for frontend Stripe Elements
    """
    try:
        # Create Stripe Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=settings.STRIPE_PRICE_AMOUNT,
            metadata={
                "user_id": user_id,
                "report_id": report_id,
                "query": query,
            },
            automatic_payment_methods={"enabled": True},
        )

        # Create Payment record in database
        supabase = get_supabase()
        payment_data = {
            "user_id": user_id,
            "report_id": report_id,
            "stripe_payment_intent_id": payment_intent.id,
            "amount": settings.STRIPE_PRICE_AMOUNT,
            "currency": settings.STRIPE_CURRENCY,
            "status": PaymentStatus.PENDING.value,
        }

        supabase.table("payments").insert(payment_data).execute()

        return CreateCheckoutResponse(
            client_secret=payment_intent.client_secret,
            payment_intent_id=payment_intent.id,
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
        )

    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


async def x_create_checkout_session__mutmut_8(
    user_id: str, report_id: str, query: str
) -> CreateCheckoutResponse:
    """
    Create Stripe payment intent for report generation
    Returns client secret for frontend Stripe Elements
    """
    try:
        # Create Stripe Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
            automatic_payment_methods={"enabled": True},
        )

        # Create Payment record in database
        supabase = get_supabase()
        payment_data = {
            "user_id": user_id,
            "report_id": report_id,
            "stripe_payment_intent_id": payment_intent.id,
            "amount": settings.STRIPE_PRICE_AMOUNT,
            "currency": settings.STRIPE_CURRENCY,
            "status": PaymentStatus.PENDING.value,
        }

        supabase.table("payments").insert(payment_data).execute()

        return CreateCheckoutResponse(
            client_secret=payment_intent.client_secret,
            payment_intent_id=payment_intent.id,
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
        )

    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


async def x_create_checkout_session__mutmut_9(
    user_id: str, report_id: str, query: str
) -> CreateCheckoutResponse:
    """
    Create Stripe payment intent for report generation
    Returns client secret for frontend Stripe Elements
    """
    try:
        # Create Stripe Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
            metadata={
                "user_id": user_id,
                "report_id": report_id,
                "query": query,
            },
            )

        # Create Payment record in database
        supabase = get_supabase()
        payment_data = {
            "user_id": user_id,
            "report_id": report_id,
            "stripe_payment_intent_id": payment_intent.id,
            "amount": settings.STRIPE_PRICE_AMOUNT,
            "currency": settings.STRIPE_CURRENCY,
            "status": PaymentStatus.PENDING.value,
        }

        supabase.table("payments").insert(payment_data).execute()

        return CreateCheckoutResponse(
            client_secret=payment_intent.client_secret,
            payment_intent_id=payment_intent.id,
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
        )

    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


async def x_create_checkout_session__mutmut_10(
    user_id: str, report_id: str, query: str
) -> CreateCheckoutResponse:
    """
    Create Stripe payment intent for report generation
    Returns client secret for frontend Stripe Elements
    """
    try:
        # Create Stripe Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
            metadata={
                "XXuser_idXX": user_id,
                "report_id": report_id,
                "query": query,
            },
            automatic_payment_methods={"enabled": True},
        )

        # Create Payment record in database
        supabase = get_supabase()
        payment_data = {
            "user_id": user_id,
            "report_id": report_id,
            "stripe_payment_intent_id": payment_intent.id,
            "amount": settings.STRIPE_PRICE_AMOUNT,
            "currency": settings.STRIPE_CURRENCY,
            "status": PaymentStatus.PENDING.value,
        }

        supabase.table("payments").insert(payment_data).execute()

        return CreateCheckoutResponse(
            client_secret=payment_intent.client_secret,
            payment_intent_id=payment_intent.id,
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
        )

    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


async def x_create_checkout_session__mutmut_11(
    user_id: str, report_id: str, query: str
) -> CreateCheckoutResponse:
    """
    Create Stripe payment intent for report generation
    Returns client secret for frontend Stripe Elements
    """
    try:
        # Create Stripe Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
            metadata={
                "USER_ID": user_id,
                "report_id": report_id,
                "query": query,
            },
            automatic_payment_methods={"enabled": True},
        )

        # Create Payment record in database
        supabase = get_supabase()
        payment_data = {
            "user_id": user_id,
            "report_id": report_id,
            "stripe_payment_intent_id": payment_intent.id,
            "amount": settings.STRIPE_PRICE_AMOUNT,
            "currency": settings.STRIPE_CURRENCY,
            "status": PaymentStatus.PENDING.value,
        }

        supabase.table("payments").insert(payment_data).execute()

        return CreateCheckoutResponse(
            client_secret=payment_intent.client_secret,
            payment_intent_id=payment_intent.id,
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
        )

    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


async def x_create_checkout_session__mutmut_12(
    user_id: str, report_id: str, query: str
) -> CreateCheckoutResponse:
    """
    Create Stripe payment intent for report generation
    Returns client secret for frontend Stripe Elements
    """
    try:
        # Create Stripe Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
            metadata={
                "user_id": user_id,
                "XXreport_idXX": report_id,
                "query": query,
            },
            automatic_payment_methods={"enabled": True},
        )

        # Create Payment record in database
        supabase = get_supabase()
        payment_data = {
            "user_id": user_id,
            "report_id": report_id,
            "stripe_payment_intent_id": payment_intent.id,
            "amount": settings.STRIPE_PRICE_AMOUNT,
            "currency": settings.STRIPE_CURRENCY,
            "status": PaymentStatus.PENDING.value,
        }

        supabase.table("payments").insert(payment_data).execute()

        return CreateCheckoutResponse(
            client_secret=payment_intent.client_secret,
            payment_intent_id=payment_intent.id,
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
        )

    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


async def x_create_checkout_session__mutmut_13(
    user_id: str, report_id: str, query: str
) -> CreateCheckoutResponse:
    """
    Create Stripe payment intent for report generation
    Returns client secret for frontend Stripe Elements
    """
    try:
        # Create Stripe Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
            metadata={
                "user_id": user_id,
                "REPORT_ID": report_id,
                "query": query,
            },
            automatic_payment_methods={"enabled": True},
        )

        # Create Payment record in database
        supabase = get_supabase()
        payment_data = {
            "user_id": user_id,
            "report_id": report_id,
            "stripe_payment_intent_id": payment_intent.id,
            "amount": settings.STRIPE_PRICE_AMOUNT,
            "currency": settings.STRIPE_CURRENCY,
            "status": PaymentStatus.PENDING.value,
        }

        supabase.table("payments").insert(payment_data).execute()

        return CreateCheckoutResponse(
            client_secret=payment_intent.client_secret,
            payment_intent_id=payment_intent.id,
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
        )

    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


async def x_create_checkout_session__mutmut_14(
    user_id: str, report_id: str, query: str
) -> CreateCheckoutResponse:
    """
    Create Stripe payment intent for report generation
    Returns client secret for frontend Stripe Elements
    """
    try:
        # Create Stripe Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
            metadata={
                "user_id": user_id,
                "report_id": report_id,
                "XXqueryXX": query,
            },
            automatic_payment_methods={"enabled": True},
        )

        # Create Payment record in database
        supabase = get_supabase()
        payment_data = {
            "user_id": user_id,
            "report_id": report_id,
            "stripe_payment_intent_id": payment_intent.id,
            "amount": settings.STRIPE_PRICE_AMOUNT,
            "currency": settings.STRIPE_CURRENCY,
            "status": PaymentStatus.PENDING.value,
        }

        supabase.table("payments").insert(payment_data).execute()

        return CreateCheckoutResponse(
            client_secret=payment_intent.client_secret,
            payment_intent_id=payment_intent.id,
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
        )

    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


async def x_create_checkout_session__mutmut_15(
    user_id: str, report_id: str, query: str
) -> CreateCheckoutResponse:
    """
    Create Stripe payment intent for report generation
    Returns client secret for frontend Stripe Elements
    """
    try:
        # Create Stripe Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
            metadata={
                "user_id": user_id,
                "report_id": report_id,
                "QUERY": query,
            },
            automatic_payment_methods={"enabled": True},
        )

        # Create Payment record in database
        supabase = get_supabase()
        payment_data = {
            "user_id": user_id,
            "report_id": report_id,
            "stripe_payment_intent_id": payment_intent.id,
            "amount": settings.STRIPE_PRICE_AMOUNT,
            "currency": settings.STRIPE_CURRENCY,
            "status": PaymentStatus.PENDING.value,
        }

        supabase.table("payments").insert(payment_data).execute()

        return CreateCheckoutResponse(
            client_secret=payment_intent.client_secret,
            payment_intent_id=payment_intent.id,
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
        )

    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


async def x_create_checkout_session__mutmut_16(
    user_id: str, report_id: str, query: str
) -> CreateCheckoutResponse:
    """
    Create Stripe payment intent for report generation
    Returns client secret for frontend Stripe Elements
    """
    try:
        # Create Stripe Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
            metadata={
                "user_id": user_id,
                "report_id": report_id,
                "query": query,
            },
            automatic_payment_methods={"XXenabledXX": True},
        )

        # Create Payment record in database
        supabase = get_supabase()
        payment_data = {
            "user_id": user_id,
            "report_id": report_id,
            "stripe_payment_intent_id": payment_intent.id,
            "amount": settings.STRIPE_PRICE_AMOUNT,
            "currency": settings.STRIPE_CURRENCY,
            "status": PaymentStatus.PENDING.value,
        }

        supabase.table("payments").insert(payment_data).execute()

        return CreateCheckoutResponse(
            client_secret=payment_intent.client_secret,
            payment_intent_id=payment_intent.id,
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
        )

    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


async def x_create_checkout_session__mutmut_17(
    user_id: str, report_id: str, query: str
) -> CreateCheckoutResponse:
    """
    Create Stripe payment intent for report generation
    Returns client secret for frontend Stripe Elements
    """
    try:
        # Create Stripe Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
            metadata={
                "user_id": user_id,
                "report_id": report_id,
                "query": query,
            },
            automatic_payment_methods={"ENABLED": True},
        )

        # Create Payment record in database
        supabase = get_supabase()
        payment_data = {
            "user_id": user_id,
            "report_id": report_id,
            "stripe_payment_intent_id": payment_intent.id,
            "amount": settings.STRIPE_PRICE_AMOUNT,
            "currency": settings.STRIPE_CURRENCY,
            "status": PaymentStatus.PENDING.value,
        }

        supabase.table("payments").insert(payment_data).execute()

        return CreateCheckoutResponse(
            client_secret=payment_intent.client_secret,
            payment_intent_id=payment_intent.id,
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
        )

    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


async def x_create_checkout_session__mutmut_18(
    user_id: str, report_id: str, query: str
) -> CreateCheckoutResponse:
    """
    Create Stripe payment intent for report generation
    Returns client secret for frontend Stripe Elements
    """
    try:
        # Create Stripe Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
            metadata={
                "user_id": user_id,
                "report_id": report_id,
                "query": query,
            },
            automatic_payment_methods={"enabled": False},
        )

        # Create Payment record in database
        supabase = get_supabase()
        payment_data = {
            "user_id": user_id,
            "report_id": report_id,
            "stripe_payment_intent_id": payment_intent.id,
            "amount": settings.STRIPE_PRICE_AMOUNT,
            "currency": settings.STRIPE_CURRENCY,
            "status": PaymentStatus.PENDING.value,
        }

        supabase.table("payments").insert(payment_data).execute()

        return CreateCheckoutResponse(
            client_secret=payment_intent.client_secret,
            payment_intent_id=payment_intent.id,
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
        )

    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


async def x_create_checkout_session__mutmut_19(
    user_id: str, report_id: str, query: str
) -> CreateCheckoutResponse:
    """
    Create Stripe payment intent for report generation
    Returns client secret for frontend Stripe Elements
    """
    try:
        # Create Stripe Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
            metadata={
                "user_id": user_id,
                "report_id": report_id,
                "query": query,
            },
            automatic_payment_methods={"enabled": True},
        )

        # Create Payment record in database
        supabase = None
        payment_data = {
            "user_id": user_id,
            "report_id": report_id,
            "stripe_payment_intent_id": payment_intent.id,
            "amount": settings.STRIPE_PRICE_AMOUNT,
            "currency": settings.STRIPE_CURRENCY,
            "status": PaymentStatus.PENDING.value,
        }

        supabase.table("payments").insert(payment_data).execute()

        return CreateCheckoutResponse(
            client_secret=payment_intent.client_secret,
            payment_intent_id=payment_intent.id,
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
        )

    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


async def x_create_checkout_session__mutmut_20(
    user_id: str, report_id: str, query: str
) -> CreateCheckoutResponse:
    """
    Create Stripe payment intent for report generation
    Returns client secret for frontend Stripe Elements
    """
    try:
        # Create Stripe Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
            metadata={
                "user_id": user_id,
                "report_id": report_id,
                "query": query,
            },
            automatic_payment_methods={"enabled": True},
        )

        # Create Payment record in database
        supabase = get_supabase()
        payment_data = None

        supabase.table("payments").insert(payment_data).execute()

        return CreateCheckoutResponse(
            client_secret=payment_intent.client_secret,
            payment_intent_id=payment_intent.id,
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
        )

    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


async def x_create_checkout_session__mutmut_21(
    user_id: str, report_id: str, query: str
) -> CreateCheckoutResponse:
    """
    Create Stripe payment intent for report generation
    Returns client secret for frontend Stripe Elements
    """
    try:
        # Create Stripe Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
            metadata={
                "user_id": user_id,
                "report_id": report_id,
                "query": query,
            },
            automatic_payment_methods={"enabled": True},
        )

        # Create Payment record in database
        supabase = get_supabase()
        payment_data = {
            "XXuser_idXX": user_id,
            "report_id": report_id,
            "stripe_payment_intent_id": payment_intent.id,
            "amount": settings.STRIPE_PRICE_AMOUNT,
            "currency": settings.STRIPE_CURRENCY,
            "status": PaymentStatus.PENDING.value,
        }

        supabase.table("payments").insert(payment_data).execute()

        return CreateCheckoutResponse(
            client_secret=payment_intent.client_secret,
            payment_intent_id=payment_intent.id,
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
        )

    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


async def x_create_checkout_session__mutmut_22(
    user_id: str, report_id: str, query: str
) -> CreateCheckoutResponse:
    """
    Create Stripe payment intent for report generation
    Returns client secret for frontend Stripe Elements
    """
    try:
        # Create Stripe Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
            metadata={
                "user_id": user_id,
                "report_id": report_id,
                "query": query,
            },
            automatic_payment_methods={"enabled": True},
        )

        # Create Payment record in database
        supabase = get_supabase()
        payment_data = {
            "USER_ID": user_id,
            "report_id": report_id,
            "stripe_payment_intent_id": payment_intent.id,
            "amount": settings.STRIPE_PRICE_AMOUNT,
            "currency": settings.STRIPE_CURRENCY,
            "status": PaymentStatus.PENDING.value,
        }

        supabase.table("payments").insert(payment_data).execute()

        return CreateCheckoutResponse(
            client_secret=payment_intent.client_secret,
            payment_intent_id=payment_intent.id,
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
        )

    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


async def x_create_checkout_session__mutmut_23(
    user_id: str, report_id: str, query: str
) -> CreateCheckoutResponse:
    """
    Create Stripe payment intent for report generation
    Returns client secret for frontend Stripe Elements
    """
    try:
        # Create Stripe Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
            metadata={
                "user_id": user_id,
                "report_id": report_id,
                "query": query,
            },
            automatic_payment_methods={"enabled": True},
        )

        # Create Payment record in database
        supabase = get_supabase()
        payment_data = {
            "user_id": user_id,
            "XXreport_idXX": report_id,
            "stripe_payment_intent_id": payment_intent.id,
            "amount": settings.STRIPE_PRICE_AMOUNT,
            "currency": settings.STRIPE_CURRENCY,
            "status": PaymentStatus.PENDING.value,
        }

        supabase.table("payments").insert(payment_data).execute()

        return CreateCheckoutResponse(
            client_secret=payment_intent.client_secret,
            payment_intent_id=payment_intent.id,
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
        )

    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


async def x_create_checkout_session__mutmut_24(
    user_id: str, report_id: str, query: str
) -> CreateCheckoutResponse:
    """
    Create Stripe payment intent for report generation
    Returns client secret for frontend Stripe Elements
    """
    try:
        # Create Stripe Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
            metadata={
                "user_id": user_id,
                "report_id": report_id,
                "query": query,
            },
            automatic_payment_methods={"enabled": True},
        )

        # Create Payment record in database
        supabase = get_supabase()
        payment_data = {
            "user_id": user_id,
            "REPORT_ID": report_id,
            "stripe_payment_intent_id": payment_intent.id,
            "amount": settings.STRIPE_PRICE_AMOUNT,
            "currency": settings.STRIPE_CURRENCY,
            "status": PaymentStatus.PENDING.value,
        }

        supabase.table("payments").insert(payment_data).execute()

        return CreateCheckoutResponse(
            client_secret=payment_intent.client_secret,
            payment_intent_id=payment_intent.id,
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
        )

    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


async def x_create_checkout_session__mutmut_25(
    user_id: str, report_id: str, query: str
) -> CreateCheckoutResponse:
    """
    Create Stripe payment intent for report generation
    Returns client secret for frontend Stripe Elements
    """
    try:
        # Create Stripe Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
            metadata={
                "user_id": user_id,
                "report_id": report_id,
                "query": query,
            },
            automatic_payment_methods={"enabled": True},
        )

        # Create Payment record in database
        supabase = get_supabase()
        payment_data = {
            "user_id": user_id,
            "report_id": report_id,
            "XXstripe_payment_intent_idXX": payment_intent.id,
            "amount": settings.STRIPE_PRICE_AMOUNT,
            "currency": settings.STRIPE_CURRENCY,
            "status": PaymentStatus.PENDING.value,
        }

        supabase.table("payments").insert(payment_data).execute()

        return CreateCheckoutResponse(
            client_secret=payment_intent.client_secret,
            payment_intent_id=payment_intent.id,
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
        )

    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


async def x_create_checkout_session__mutmut_26(
    user_id: str, report_id: str, query: str
) -> CreateCheckoutResponse:
    """
    Create Stripe payment intent for report generation
    Returns client secret for frontend Stripe Elements
    """
    try:
        # Create Stripe Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
            metadata={
                "user_id": user_id,
                "report_id": report_id,
                "query": query,
            },
            automatic_payment_methods={"enabled": True},
        )

        # Create Payment record in database
        supabase = get_supabase()
        payment_data = {
            "user_id": user_id,
            "report_id": report_id,
            "STRIPE_PAYMENT_INTENT_ID": payment_intent.id,
            "amount": settings.STRIPE_PRICE_AMOUNT,
            "currency": settings.STRIPE_CURRENCY,
            "status": PaymentStatus.PENDING.value,
        }

        supabase.table("payments").insert(payment_data).execute()

        return CreateCheckoutResponse(
            client_secret=payment_intent.client_secret,
            payment_intent_id=payment_intent.id,
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
        )

    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


async def x_create_checkout_session__mutmut_27(
    user_id: str, report_id: str, query: str
) -> CreateCheckoutResponse:
    """
    Create Stripe payment intent for report generation
    Returns client secret for frontend Stripe Elements
    """
    try:
        # Create Stripe Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
            metadata={
                "user_id": user_id,
                "report_id": report_id,
                "query": query,
            },
            automatic_payment_methods={"enabled": True},
        )

        # Create Payment record in database
        supabase = get_supabase()
        payment_data = {
            "user_id": user_id,
            "report_id": report_id,
            "stripe_payment_intent_id": payment_intent.id,
            "XXamountXX": settings.STRIPE_PRICE_AMOUNT,
            "currency": settings.STRIPE_CURRENCY,
            "status": PaymentStatus.PENDING.value,
        }

        supabase.table("payments").insert(payment_data).execute()

        return CreateCheckoutResponse(
            client_secret=payment_intent.client_secret,
            payment_intent_id=payment_intent.id,
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
        )

    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


async def x_create_checkout_session__mutmut_28(
    user_id: str, report_id: str, query: str
) -> CreateCheckoutResponse:
    """
    Create Stripe payment intent for report generation
    Returns client secret for frontend Stripe Elements
    """
    try:
        # Create Stripe Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
            metadata={
                "user_id": user_id,
                "report_id": report_id,
                "query": query,
            },
            automatic_payment_methods={"enabled": True},
        )

        # Create Payment record in database
        supabase = get_supabase()
        payment_data = {
            "user_id": user_id,
            "report_id": report_id,
            "stripe_payment_intent_id": payment_intent.id,
            "AMOUNT": settings.STRIPE_PRICE_AMOUNT,
            "currency": settings.STRIPE_CURRENCY,
            "status": PaymentStatus.PENDING.value,
        }

        supabase.table("payments").insert(payment_data).execute()

        return CreateCheckoutResponse(
            client_secret=payment_intent.client_secret,
            payment_intent_id=payment_intent.id,
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
        )

    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


async def x_create_checkout_session__mutmut_29(
    user_id: str, report_id: str, query: str
) -> CreateCheckoutResponse:
    """
    Create Stripe payment intent for report generation
    Returns client secret for frontend Stripe Elements
    """
    try:
        # Create Stripe Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
            metadata={
                "user_id": user_id,
                "report_id": report_id,
                "query": query,
            },
            automatic_payment_methods={"enabled": True},
        )

        # Create Payment record in database
        supabase = get_supabase()
        payment_data = {
            "user_id": user_id,
            "report_id": report_id,
            "stripe_payment_intent_id": payment_intent.id,
            "amount": settings.STRIPE_PRICE_AMOUNT,
            "XXcurrencyXX": settings.STRIPE_CURRENCY,
            "status": PaymentStatus.PENDING.value,
        }

        supabase.table("payments").insert(payment_data).execute()

        return CreateCheckoutResponse(
            client_secret=payment_intent.client_secret,
            payment_intent_id=payment_intent.id,
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
        )

    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


async def x_create_checkout_session__mutmut_30(
    user_id: str, report_id: str, query: str
) -> CreateCheckoutResponse:
    """
    Create Stripe payment intent for report generation
    Returns client secret for frontend Stripe Elements
    """
    try:
        # Create Stripe Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
            metadata={
                "user_id": user_id,
                "report_id": report_id,
                "query": query,
            },
            automatic_payment_methods={"enabled": True},
        )

        # Create Payment record in database
        supabase = get_supabase()
        payment_data = {
            "user_id": user_id,
            "report_id": report_id,
            "stripe_payment_intent_id": payment_intent.id,
            "amount": settings.STRIPE_PRICE_AMOUNT,
            "CURRENCY": settings.STRIPE_CURRENCY,
            "status": PaymentStatus.PENDING.value,
        }

        supabase.table("payments").insert(payment_data).execute()

        return CreateCheckoutResponse(
            client_secret=payment_intent.client_secret,
            payment_intent_id=payment_intent.id,
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
        )

    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


async def x_create_checkout_session__mutmut_31(
    user_id: str, report_id: str, query: str
) -> CreateCheckoutResponse:
    """
    Create Stripe payment intent for report generation
    Returns client secret for frontend Stripe Elements
    """
    try:
        # Create Stripe Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
            metadata={
                "user_id": user_id,
                "report_id": report_id,
                "query": query,
            },
            automatic_payment_methods={"enabled": True},
        )

        # Create Payment record in database
        supabase = get_supabase()
        payment_data = {
            "user_id": user_id,
            "report_id": report_id,
            "stripe_payment_intent_id": payment_intent.id,
            "amount": settings.STRIPE_PRICE_AMOUNT,
            "currency": settings.STRIPE_CURRENCY,
            "XXstatusXX": PaymentStatus.PENDING.value,
        }

        supabase.table("payments").insert(payment_data).execute()

        return CreateCheckoutResponse(
            client_secret=payment_intent.client_secret,
            payment_intent_id=payment_intent.id,
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
        )

    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


async def x_create_checkout_session__mutmut_32(
    user_id: str, report_id: str, query: str
) -> CreateCheckoutResponse:
    """
    Create Stripe payment intent for report generation
    Returns client secret for frontend Stripe Elements
    """
    try:
        # Create Stripe Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
            metadata={
                "user_id": user_id,
                "report_id": report_id,
                "query": query,
            },
            automatic_payment_methods={"enabled": True},
        )

        # Create Payment record in database
        supabase = get_supabase()
        payment_data = {
            "user_id": user_id,
            "report_id": report_id,
            "stripe_payment_intent_id": payment_intent.id,
            "amount": settings.STRIPE_PRICE_AMOUNT,
            "currency": settings.STRIPE_CURRENCY,
            "STATUS": PaymentStatus.PENDING.value,
        }

        supabase.table("payments").insert(payment_data).execute()

        return CreateCheckoutResponse(
            client_secret=payment_intent.client_secret,
            payment_intent_id=payment_intent.id,
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
        )

    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


async def x_create_checkout_session__mutmut_33(
    user_id: str, report_id: str, query: str
) -> CreateCheckoutResponse:
    """
    Create Stripe payment intent for report generation
    Returns client secret for frontend Stripe Elements
    """
    try:
        # Create Stripe Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
            metadata={
                "user_id": user_id,
                "report_id": report_id,
                "query": query,
            },
            automatic_payment_methods={"enabled": True},
        )

        # Create Payment record in database
        supabase = get_supabase()
        payment_data = {
            "user_id": user_id,
            "report_id": report_id,
            "stripe_payment_intent_id": payment_intent.id,
            "amount": settings.STRIPE_PRICE_AMOUNT,
            "currency": settings.STRIPE_CURRENCY,
            "status": PaymentStatus.PENDING.value,
        }

        supabase.table("payments").insert(None).execute()

        return CreateCheckoutResponse(
            client_secret=payment_intent.client_secret,
            payment_intent_id=payment_intent.id,
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
        )

    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


async def x_create_checkout_session__mutmut_34(
    user_id: str, report_id: str, query: str
) -> CreateCheckoutResponse:
    """
    Create Stripe payment intent for report generation
    Returns client secret for frontend Stripe Elements
    """
    try:
        # Create Stripe Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
            metadata={
                "user_id": user_id,
                "report_id": report_id,
                "query": query,
            },
            automatic_payment_methods={"enabled": True},
        )

        # Create Payment record in database
        supabase = get_supabase()
        payment_data = {
            "user_id": user_id,
            "report_id": report_id,
            "stripe_payment_intent_id": payment_intent.id,
            "amount": settings.STRIPE_PRICE_AMOUNT,
            "currency": settings.STRIPE_CURRENCY,
            "status": PaymentStatus.PENDING.value,
        }

        supabase.table(None).insert(payment_data).execute()

        return CreateCheckoutResponse(
            client_secret=payment_intent.client_secret,
            payment_intent_id=payment_intent.id,
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
        )

    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


async def x_create_checkout_session__mutmut_35(
    user_id: str, report_id: str, query: str
) -> CreateCheckoutResponse:
    """
    Create Stripe payment intent for report generation
    Returns client secret for frontend Stripe Elements
    """
    try:
        # Create Stripe Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
            metadata={
                "user_id": user_id,
                "report_id": report_id,
                "query": query,
            },
            automatic_payment_methods={"enabled": True},
        )

        # Create Payment record in database
        supabase = get_supabase()
        payment_data = {
            "user_id": user_id,
            "report_id": report_id,
            "stripe_payment_intent_id": payment_intent.id,
            "amount": settings.STRIPE_PRICE_AMOUNT,
            "currency": settings.STRIPE_CURRENCY,
            "status": PaymentStatus.PENDING.value,
        }

        supabase.table("XXpaymentsXX").insert(payment_data).execute()

        return CreateCheckoutResponse(
            client_secret=payment_intent.client_secret,
            payment_intent_id=payment_intent.id,
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
        )

    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


async def x_create_checkout_session__mutmut_36(
    user_id: str, report_id: str, query: str
) -> CreateCheckoutResponse:
    """
    Create Stripe payment intent for report generation
    Returns client secret for frontend Stripe Elements
    """
    try:
        # Create Stripe Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
            metadata={
                "user_id": user_id,
                "report_id": report_id,
                "query": query,
            },
            automatic_payment_methods={"enabled": True},
        )

        # Create Payment record in database
        supabase = get_supabase()
        payment_data = {
            "user_id": user_id,
            "report_id": report_id,
            "stripe_payment_intent_id": payment_intent.id,
            "amount": settings.STRIPE_PRICE_AMOUNT,
            "currency": settings.STRIPE_CURRENCY,
            "status": PaymentStatus.PENDING.value,
        }

        supabase.table("PAYMENTS").insert(payment_data).execute()

        return CreateCheckoutResponse(
            client_secret=payment_intent.client_secret,
            payment_intent_id=payment_intent.id,
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
        )

    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


async def x_create_checkout_session__mutmut_37(
    user_id: str, report_id: str, query: str
) -> CreateCheckoutResponse:
    """
    Create Stripe payment intent for report generation
    Returns client secret for frontend Stripe Elements
    """
    try:
        # Create Stripe Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
            metadata={
                "user_id": user_id,
                "report_id": report_id,
                "query": query,
            },
            automatic_payment_methods={"enabled": True},
        )

        # Create Payment record in database
        supabase = get_supabase()
        payment_data = {
            "user_id": user_id,
            "report_id": report_id,
            "stripe_payment_intent_id": payment_intent.id,
            "amount": settings.STRIPE_PRICE_AMOUNT,
            "currency": settings.STRIPE_CURRENCY,
            "status": PaymentStatus.PENDING.value,
        }

        supabase.table("payments").insert(payment_data).execute()

        return CreateCheckoutResponse(
            client_secret=None,
            payment_intent_id=payment_intent.id,
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
        )

    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


async def x_create_checkout_session__mutmut_38(
    user_id: str, report_id: str, query: str
) -> CreateCheckoutResponse:
    """
    Create Stripe payment intent for report generation
    Returns client secret for frontend Stripe Elements
    """
    try:
        # Create Stripe Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
            metadata={
                "user_id": user_id,
                "report_id": report_id,
                "query": query,
            },
            automatic_payment_methods={"enabled": True},
        )

        # Create Payment record in database
        supabase = get_supabase()
        payment_data = {
            "user_id": user_id,
            "report_id": report_id,
            "stripe_payment_intent_id": payment_intent.id,
            "amount": settings.STRIPE_PRICE_AMOUNT,
            "currency": settings.STRIPE_CURRENCY,
            "status": PaymentStatus.PENDING.value,
        }

        supabase.table("payments").insert(payment_data).execute()

        return CreateCheckoutResponse(
            client_secret=payment_intent.client_secret,
            payment_intent_id=None,
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
        )

    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


async def x_create_checkout_session__mutmut_39(
    user_id: str, report_id: str, query: str
) -> CreateCheckoutResponse:
    """
    Create Stripe payment intent for report generation
    Returns client secret for frontend Stripe Elements
    """
    try:
        # Create Stripe Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
            metadata={
                "user_id": user_id,
                "report_id": report_id,
                "query": query,
            },
            automatic_payment_methods={"enabled": True},
        )

        # Create Payment record in database
        supabase = get_supabase()
        payment_data = {
            "user_id": user_id,
            "report_id": report_id,
            "stripe_payment_intent_id": payment_intent.id,
            "amount": settings.STRIPE_PRICE_AMOUNT,
            "currency": settings.STRIPE_CURRENCY,
            "status": PaymentStatus.PENDING.value,
        }

        supabase.table("payments").insert(payment_data).execute()

        return CreateCheckoutResponse(
            client_secret=payment_intent.client_secret,
            payment_intent_id=payment_intent.id,
            amount=None,
            currency=settings.STRIPE_CURRENCY,
        )

    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


async def x_create_checkout_session__mutmut_40(
    user_id: str, report_id: str, query: str
) -> CreateCheckoutResponse:
    """
    Create Stripe payment intent for report generation
    Returns client secret for frontend Stripe Elements
    """
    try:
        # Create Stripe Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
            metadata={
                "user_id": user_id,
                "report_id": report_id,
                "query": query,
            },
            automatic_payment_methods={"enabled": True},
        )

        # Create Payment record in database
        supabase = get_supabase()
        payment_data = {
            "user_id": user_id,
            "report_id": report_id,
            "stripe_payment_intent_id": payment_intent.id,
            "amount": settings.STRIPE_PRICE_AMOUNT,
            "currency": settings.STRIPE_CURRENCY,
            "status": PaymentStatus.PENDING.value,
        }

        supabase.table("payments").insert(payment_data).execute()

        return CreateCheckoutResponse(
            client_secret=payment_intent.client_secret,
            payment_intent_id=payment_intent.id,
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=None,
        )

    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


async def x_create_checkout_session__mutmut_41(
    user_id: str, report_id: str, query: str
) -> CreateCheckoutResponse:
    """
    Create Stripe payment intent for report generation
    Returns client secret for frontend Stripe Elements
    """
    try:
        # Create Stripe Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
            metadata={
                "user_id": user_id,
                "report_id": report_id,
                "query": query,
            },
            automatic_payment_methods={"enabled": True},
        )

        # Create Payment record in database
        supabase = get_supabase()
        payment_data = {
            "user_id": user_id,
            "report_id": report_id,
            "stripe_payment_intent_id": payment_intent.id,
            "amount": settings.STRIPE_PRICE_AMOUNT,
            "currency": settings.STRIPE_CURRENCY,
            "status": PaymentStatus.PENDING.value,
        }

        supabase.table("payments").insert(payment_data).execute()

        return CreateCheckoutResponse(
            payment_intent_id=payment_intent.id,
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
        )

    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


async def x_create_checkout_session__mutmut_42(
    user_id: str, report_id: str, query: str
) -> CreateCheckoutResponse:
    """
    Create Stripe payment intent for report generation
    Returns client secret for frontend Stripe Elements
    """
    try:
        # Create Stripe Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
            metadata={
                "user_id": user_id,
                "report_id": report_id,
                "query": query,
            },
            automatic_payment_methods={"enabled": True},
        )

        # Create Payment record in database
        supabase = get_supabase()
        payment_data = {
            "user_id": user_id,
            "report_id": report_id,
            "stripe_payment_intent_id": payment_intent.id,
            "amount": settings.STRIPE_PRICE_AMOUNT,
            "currency": settings.STRIPE_CURRENCY,
            "status": PaymentStatus.PENDING.value,
        }

        supabase.table("payments").insert(payment_data).execute()

        return CreateCheckoutResponse(
            client_secret=payment_intent.client_secret,
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
        )

    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


async def x_create_checkout_session__mutmut_43(
    user_id: str, report_id: str, query: str
) -> CreateCheckoutResponse:
    """
    Create Stripe payment intent for report generation
    Returns client secret for frontend Stripe Elements
    """
    try:
        # Create Stripe Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
            metadata={
                "user_id": user_id,
                "report_id": report_id,
                "query": query,
            },
            automatic_payment_methods={"enabled": True},
        )

        # Create Payment record in database
        supabase = get_supabase()
        payment_data = {
            "user_id": user_id,
            "report_id": report_id,
            "stripe_payment_intent_id": payment_intent.id,
            "amount": settings.STRIPE_PRICE_AMOUNT,
            "currency": settings.STRIPE_CURRENCY,
            "status": PaymentStatus.PENDING.value,
        }

        supabase.table("payments").insert(payment_data).execute()

        return CreateCheckoutResponse(
            client_secret=payment_intent.client_secret,
            payment_intent_id=payment_intent.id,
            currency=settings.STRIPE_CURRENCY,
        )

    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


async def x_create_checkout_session__mutmut_44(
    user_id: str, report_id: str, query: str
) -> CreateCheckoutResponse:
    """
    Create Stripe payment intent for report generation
    Returns client secret for frontend Stripe Elements
    """
    try:
        # Create Stripe Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
            metadata={
                "user_id": user_id,
                "report_id": report_id,
                "query": query,
            },
            automatic_payment_methods={"enabled": True},
        )

        # Create Payment record in database
        supabase = get_supabase()
        payment_data = {
            "user_id": user_id,
            "report_id": report_id,
            "stripe_payment_intent_id": payment_intent.id,
            "amount": settings.STRIPE_PRICE_AMOUNT,
            "currency": settings.STRIPE_CURRENCY,
            "status": PaymentStatus.PENDING.value,
        }

        supabase.table("payments").insert(payment_data).execute()

        return CreateCheckoutResponse(
            client_secret=payment_intent.client_secret,
            payment_intent_id=payment_intent.id,
            amount=settings.STRIPE_PRICE_AMOUNT,
            )

    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(e)}")


async def x_create_checkout_session__mutmut_45(
    user_id: str, report_id: str, query: str
) -> CreateCheckoutResponse:
    """
    Create Stripe payment intent for report generation
    Returns client secret for frontend Stripe Elements
    """
    try:
        # Create Stripe Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
            metadata={
                "user_id": user_id,
                "report_id": report_id,
                "query": query,
            },
            automatic_payment_methods={"enabled": True},
        )

        # Create Payment record in database
        supabase = get_supabase()
        payment_data = {
            "user_id": user_id,
            "report_id": report_id,
            "stripe_payment_intent_id": payment_intent.id,
            "amount": settings.STRIPE_PRICE_AMOUNT,
            "currency": settings.STRIPE_CURRENCY,
            "status": PaymentStatus.PENDING.value,
        }

        supabase.table("payments").insert(payment_data).execute()

        return CreateCheckoutResponse(
            client_secret=payment_intent.client_secret,
            payment_intent_id=payment_intent.id,
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
        )

    except stripe.error.StripeError as e:
        raise Exception(None)


async def x_create_checkout_session__mutmut_46(
    user_id: str, report_id: str, query: str
) -> CreateCheckoutResponse:
    """
    Create Stripe payment intent for report generation
    Returns client secret for frontend Stripe Elements
    """
    try:
        # Create Stripe Payment Intent
        payment_intent = stripe.PaymentIntent.create(
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
            metadata={
                "user_id": user_id,
                "report_id": report_id,
                "query": query,
            },
            automatic_payment_methods={"enabled": True},
        )

        # Create Payment record in database
        supabase = get_supabase()
        payment_data = {
            "user_id": user_id,
            "report_id": report_id,
            "stripe_payment_intent_id": payment_intent.id,
            "amount": settings.STRIPE_PRICE_AMOUNT,
            "currency": settings.STRIPE_CURRENCY,
            "status": PaymentStatus.PENDING.value,
        }

        supabase.table("payments").insert(payment_data).execute()

        return CreateCheckoutResponse(
            client_secret=payment_intent.client_secret,
            payment_intent_id=payment_intent.id,
            amount=settings.STRIPE_PRICE_AMOUNT,
            currency=settings.STRIPE_CURRENCY,
        )

    except stripe.error.StripeError as e:
        raise Exception(f"Stripe error: {str(None)}")

x_create_checkout_session__mutmut_mutants : ClassVar[MutantDict] = {
'x_create_checkout_session__mutmut_1': x_create_checkout_session__mutmut_1, 
    'x_create_checkout_session__mutmut_2': x_create_checkout_session__mutmut_2, 
    'x_create_checkout_session__mutmut_3': x_create_checkout_session__mutmut_3, 
    'x_create_checkout_session__mutmut_4': x_create_checkout_session__mutmut_4, 
    'x_create_checkout_session__mutmut_5': x_create_checkout_session__mutmut_5, 
    'x_create_checkout_session__mutmut_6': x_create_checkout_session__mutmut_6, 
    'x_create_checkout_session__mutmut_7': x_create_checkout_session__mutmut_7, 
    'x_create_checkout_session__mutmut_8': x_create_checkout_session__mutmut_8, 
    'x_create_checkout_session__mutmut_9': x_create_checkout_session__mutmut_9, 
    'x_create_checkout_session__mutmut_10': x_create_checkout_session__mutmut_10, 
    'x_create_checkout_session__mutmut_11': x_create_checkout_session__mutmut_11, 
    'x_create_checkout_session__mutmut_12': x_create_checkout_session__mutmut_12, 
    'x_create_checkout_session__mutmut_13': x_create_checkout_session__mutmut_13, 
    'x_create_checkout_session__mutmut_14': x_create_checkout_session__mutmut_14, 
    'x_create_checkout_session__mutmut_15': x_create_checkout_session__mutmut_15, 
    'x_create_checkout_session__mutmut_16': x_create_checkout_session__mutmut_16, 
    'x_create_checkout_session__mutmut_17': x_create_checkout_session__mutmut_17, 
    'x_create_checkout_session__mutmut_18': x_create_checkout_session__mutmut_18, 
    'x_create_checkout_session__mutmut_19': x_create_checkout_session__mutmut_19, 
    'x_create_checkout_session__mutmut_20': x_create_checkout_session__mutmut_20, 
    'x_create_checkout_session__mutmut_21': x_create_checkout_session__mutmut_21, 
    'x_create_checkout_session__mutmut_22': x_create_checkout_session__mutmut_22, 
    'x_create_checkout_session__mutmut_23': x_create_checkout_session__mutmut_23, 
    'x_create_checkout_session__mutmut_24': x_create_checkout_session__mutmut_24, 
    'x_create_checkout_session__mutmut_25': x_create_checkout_session__mutmut_25, 
    'x_create_checkout_session__mutmut_26': x_create_checkout_session__mutmut_26, 
    'x_create_checkout_session__mutmut_27': x_create_checkout_session__mutmut_27, 
    'x_create_checkout_session__mutmut_28': x_create_checkout_session__mutmut_28, 
    'x_create_checkout_session__mutmut_29': x_create_checkout_session__mutmut_29, 
    'x_create_checkout_session__mutmut_30': x_create_checkout_session__mutmut_30, 
    'x_create_checkout_session__mutmut_31': x_create_checkout_session__mutmut_31, 
    'x_create_checkout_session__mutmut_32': x_create_checkout_session__mutmut_32, 
    'x_create_checkout_session__mutmut_33': x_create_checkout_session__mutmut_33, 
    'x_create_checkout_session__mutmut_34': x_create_checkout_session__mutmut_34, 
    'x_create_checkout_session__mutmut_35': x_create_checkout_session__mutmut_35, 
    'x_create_checkout_session__mutmut_36': x_create_checkout_session__mutmut_36, 
    'x_create_checkout_session__mutmut_37': x_create_checkout_session__mutmut_37, 
    'x_create_checkout_session__mutmut_38': x_create_checkout_session__mutmut_38, 
    'x_create_checkout_session__mutmut_39': x_create_checkout_session__mutmut_39, 
    'x_create_checkout_session__mutmut_40': x_create_checkout_session__mutmut_40, 
    'x_create_checkout_session__mutmut_41': x_create_checkout_session__mutmut_41, 
    'x_create_checkout_session__mutmut_42': x_create_checkout_session__mutmut_42, 
    'x_create_checkout_session__mutmut_43': x_create_checkout_session__mutmut_43, 
    'x_create_checkout_session__mutmut_44': x_create_checkout_session__mutmut_44, 
    'x_create_checkout_session__mutmut_45': x_create_checkout_session__mutmut_45, 
    'x_create_checkout_session__mutmut_46': x_create_checkout_session__mutmut_46
}

def create_checkout_session(*args, **kwargs):
    result = _mutmut_trampoline(x_create_checkout_session__mutmut_orig, x_create_checkout_session__mutmut_mutants, args, kwargs)
    return result 

create_checkout_session.__signature__ = _mutmut_signature(x_create_checkout_session__mutmut_orig)
x_create_checkout_session__mutmut_orig.__name__ = 'x_create_checkout_session'


async def x_update_payment_status__mutmut_orig(
    payment_intent_id: str, status: PaymentStatus, error_message: Optional[str] = None
) -> Optional[Payment]:
    """
    Update payment status after webhook event
    """
    supabase = get_supabase()

    update_data = {
        "status": status.value,
        "updated_at": datetime.utcnow().isoformat(),
    }

    if error_message:
        update_data["error_message"] = error_message

    if status == PaymentStatus.REFUNDED:
        update_data["refunded_at"] = datetime.utcnow().isoformat()

    result = (
        supabase.table("payments")
        .update(update_data)
        .eq("stripe_payment_intent_id", payment_intent_id)
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Payment(**result.data[0])
    return None


async def x_update_payment_status__mutmut_1(
    payment_intent_id: str, status: PaymentStatus, error_message: Optional[str] = None
) -> Optional[Payment]:
    """
    Update payment status after webhook event
    """
    supabase = None

    update_data = {
        "status": status.value,
        "updated_at": datetime.utcnow().isoformat(),
    }

    if error_message:
        update_data["error_message"] = error_message

    if status == PaymentStatus.REFUNDED:
        update_data["refunded_at"] = datetime.utcnow().isoformat()

    result = (
        supabase.table("payments")
        .update(update_data)
        .eq("stripe_payment_intent_id", payment_intent_id)
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Payment(**result.data[0])
    return None


async def x_update_payment_status__mutmut_2(
    payment_intent_id: str, status: PaymentStatus, error_message: Optional[str] = None
) -> Optional[Payment]:
    """
    Update payment status after webhook event
    """
    supabase = get_supabase()

    update_data = None

    if error_message:
        update_data["error_message"] = error_message

    if status == PaymentStatus.REFUNDED:
        update_data["refunded_at"] = datetime.utcnow().isoformat()

    result = (
        supabase.table("payments")
        .update(update_data)
        .eq("stripe_payment_intent_id", payment_intent_id)
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Payment(**result.data[0])
    return None


async def x_update_payment_status__mutmut_3(
    payment_intent_id: str, status: PaymentStatus, error_message: Optional[str] = None
) -> Optional[Payment]:
    """
    Update payment status after webhook event
    """
    supabase = get_supabase()

    update_data = {
        "XXstatusXX": status.value,
        "updated_at": datetime.utcnow().isoformat(),
    }

    if error_message:
        update_data["error_message"] = error_message

    if status == PaymentStatus.REFUNDED:
        update_data["refunded_at"] = datetime.utcnow().isoformat()

    result = (
        supabase.table("payments")
        .update(update_data)
        .eq("stripe_payment_intent_id", payment_intent_id)
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Payment(**result.data[0])
    return None


async def x_update_payment_status__mutmut_4(
    payment_intent_id: str, status: PaymentStatus, error_message: Optional[str] = None
) -> Optional[Payment]:
    """
    Update payment status after webhook event
    """
    supabase = get_supabase()

    update_data = {
        "STATUS": status.value,
        "updated_at": datetime.utcnow().isoformat(),
    }

    if error_message:
        update_data["error_message"] = error_message

    if status == PaymentStatus.REFUNDED:
        update_data["refunded_at"] = datetime.utcnow().isoformat()

    result = (
        supabase.table("payments")
        .update(update_data)
        .eq("stripe_payment_intent_id", payment_intent_id)
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Payment(**result.data[0])
    return None


async def x_update_payment_status__mutmut_5(
    payment_intent_id: str, status: PaymentStatus, error_message: Optional[str] = None
) -> Optional[Payment]:
    """
    Update payment status after webhook event
    """
    supabase = get_supabase()

    update_data = {
        "status": status.value,
        "XXupdated_atXX": datetime.utcnow().isoformat(),
    }

    if error_message:
        update_data["error_message"] = error_message

    if status == PaymentStatus.REFUNDED:
        update_data["refunded_at"] = datetime.utcnow().isoformat()

    result = (
        supabase.table("payments")
        .update(update_data)
        .eq("stripe_payment_intent_id", payment_intent_id)
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Payment(**result.data[0])
    return None


async def x_update_payment_status__mutmut_6(
    payment_intent_id: str, status: PaymentStatus, error_message: Optional[str] = None
) -> Optional[Payment]:
    """
    Update payment status after webhook event
    """
    supabase = get_supabase()

    update_data = {
        "status": status.value,
        "UPDATED_AT": datetime.utcnow().isoformat(),
    }

    if error_message:
        update_data["error_message"] = error_message

    if status == PaymentStatus.REFUNDED:
        update_data["refunded_at"] = datetime.utcnow().isoformat()

    result = (
        supabase.table("payments")
        .update(update_data)
        .eq("stripe_payment_intent_id", payment_intent_id)
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Payment(**result.data[0])
    return None


async def x_update_payment_status__mutmut_7(
    payment_intent_id: str, status: PaymentStatus, error_message: Optional[str] = None
) -> Optional[Payment]:
    """
    Update payment status after webhook event
    """
    supabase = get_supabase()

    update_data = {
        "status": status.value,
        "updated_at": datetime.utcnow().isoformat(),
    }

    if error_message:
        update_data["error_message"] = None

    if status == PaymentStatus.REFUNDED:
        update_data["refunded_at"] = datetime.utcnow().isoformat()

    result = (
        supabase.table("payments")
        .update(update_data)
        .eq("stripe_payment_intent_id", payment_intent_id)
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Payment(**result.data[0])
    return None


async def x_update_payment_status__mutmut_8(
    payment_intent_id: str, status: PaymentStatus, error_message: Optional[str] = None
) -> Optional[Payment]:
    """
    Update payment status after webhook event
    """
    supabase = get_supabase()

    update_data = {
        "status": status.value,
        "updated_at": datetime.utcnow().isoformat(),
    }

    if error_message:
        update_data["XXerror_messageXX"] = error_message

    if status == PaymentStatus.REFUNDED:
        update_data["refunded_at"] = datetime.utcnow().isoformat()

    result = (
        supabase.table("payments")
        .update(update_data)
        .eq("stripe_payment_intent_id", payment_intent_id)
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Payment(**result.data[0])
    return None


async def x_update_payment_status__mutmut_9(
    payment_intent_id: str, status: PaymentStatus, error_message: Optional[str] = None
) -> Optional[Payment]:
    """
    Update payment status after webhook event
    """
    supabase = get_supabase()

    update_data = {
        "status": status.value,
        "updated_at": datetime.utcnow().isoformat(),
    }

    if error_message:
        update_data["ERROR_MESSAGE"] = error_message

    if status == PaymentStatus.REFUNDED:
        update_data["refunded_at"] = datetime.utcnow().isoformat()

    result = (
        supabase.table("payments")
        .update(update_data)
        .eq("stripe_payment_intent_id", payment_intent_id)
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Payment(**result.data[0])
    return None


async def x_update_payment_status__mutmut_10(
    payment_intent_id: str, status: PaymentStatus, error_message: Optional[str] = None
) -> Optional[Payment]:
    """
    Update payment status after webhook event
    """
    supabase = get_supabase()

    update_data = {
        "status": status.value,
        "updated_at": datetime.utcnow().isoformat(),
    }

    if error_message:
        update_data["error_message"] = error_message

    if status != PaymentStatus.REFUNDED:
        update_data["refunded_at"] = datetime.utcnow().isoformat()

    result = (
        supabase.table("payments")
        .update(update_data)
        .eq("stripe_payment_intent_id", payment_intent_id)
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Payment(**result.data[0])
    return None


async def x_update_payment_status__mutmut_11(
    payment_intent_id: str, status: PaymentStatus, error_message: Optional[str] = None
) -> Optional[Payment]:
    """
    Update payment status after webhook event
    """
    supabase = get_supabase()

    update_data = {
        "status": status.value,
        "updated_at": datetime.utcnow().isoformat(),
    }

    if error_message:
        update_data["error_message"] = error_message

    if status == PaymentStatus.REFUNDED:
        update_data["refunded_at"] = None

    result = (
        supabase.table("payments")
        .update(update_data)
        .eq("stripe_payment_intent_id", payment_intent_id)
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Payment(**result.data[0])
    return None


async def x_update_payment_status__mutmut_12(
    payment_intent_id: str, status: PaymentStatus, error_message: Optional[str] = None
) -> Optional[Payment]:
    """
    Update payment status after webhook event
    """
    supabase = get_supabase()

    update_data = {
        "status": status.value,
        "updated_at": datetime.utcnow().isoformat(),
    }

    if error_message:
        update_data["error_message"] = error_message

    if status == PaymentStatus.REFUNDED:
        update_data["XXrefunded_atXX"] = datetime.utcnow().isoformat()

    result = (
        supabase.table("payments")
        .update(update_data)
        .eq("stripe_payment_intent_id", payment_intent_id)
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Payment(**result.data[0])
    return None


async def x_update_payment_status__mutmut_13(
    payment_intent_id: str, status: PaymentStatus, error_message: Optional[str] = None
) -> Optional[Payment]:
    """
    Update payment status after webhook event
    """
    supabase = get_supabase()

    update_data = {
        "status": status.value,
        "updated_at": datetime.utcnow().isoformat(),
    }

    if error_message:
        update_data["error_message"] = error_message

    if status == PaymentStatus.REFUNDED:
        update_data["REFUNDED_AT"] = datetime.utcnow().isoformat()

    result = (
        supabase.table("payments")
        .update(update_data)
        .eq("stripe_payment_intent_id", payment_intent_id)
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Payment(**result.data[0])
    return None


async def x_update_payment_status__mutmut_14(
    payment_intent_id: str, status: PaymentStatus, error_message: Optional[str] = None
) -> Optional[Payment]:
    """
    Update payment status after webhook event
    """
    supabase = get_supabase()

    update_data = {
        "status": status.value,
        "updated_at": datetime.utcnow().isoformat(),
    }

    if error_message:
        update_data["error_message"] = error_message

    if status == PaymentStatus.REFUNDED:
        update_data["refunded_at"] = datetime.utcnow().isoformat()

    result = None

    if result.data and len(result.data) > 0:
        return Payment(**result.data[0])
    return None


async def x_update_payment_status__mutmut_15(
    payment_intent_id: str, status: PaymentStatus, error_message: Optional[str] = None
) -> Optional[Payment]:
    """
    Update payment status after webhook event
    """
    supabase = get_supabase()

    update_data = {
        "status": status.value,
        "updated_at": datetime.utcnow().isoformat(),
    }

    if error_message:
        update_data["error_message"] = error_message

    if status == PaymentStatus.REFUNDED:
        update_data["refunded_at"] = datetime.utcnow().isoformat()

    result = (
        supabase.table("payments")
        .update(update_data)
        .eq(None, payment_intent_id)
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Payment(**result.data[0])
    return None


async def x_update_payment_status__mutmut_16(
    payment_intent_id: str, status: PaymentStatus, error_message: Optional[str] = None
) -> Optional[Payment]:
    """
    Update payment status after webhook event
    """
    supabase = get_supabase()

    update_data = {
        "status": status.value,
        "updated_at": datetime.utcnow().isoformat(),
    }

    if error_message:
        update_data["error_message"] = error_message

    if status == PaymentStatus.REFUNDED:
        update_data["refunded_at"] = datetime.utcnow().isoformat()

    result = (
        supabase.table("payments")
        .update(update_data)
        .eq("stripe_payment_intent_id", None)
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Payment(**result.data[0])
    return None


async def x_update_payment_status__mutmut_17(
    payment_intent_id: str, status: PaymentStatus, error_message: Optional[str] = None
) -> Optional[Payment]:
    """
    Update payment status after webhook event
    """
    supabase = get_supabase()

    update_data = {
        "status": status.value,
        "updated_at": datetime.utcnow().isoformat(),
    }

    if error_message:
        update_data["error_message"] = error_message

    if status == PaymentStatus.REFUNDED:
        update_data["refunded_at"] = datetime.utcnow().isoformat()

    result = (
        supabase.table("payments")
        .update(update_data)
        .eq(payment_intent_id)
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Payment(**result.data[0])
    return None


async def x_update_payment_status__mutmut_18(
    payment_intent_id: str, status: PaymentStatus, error_message: Optional[str] = None
) -> Optional[Payment]:
    """
    Update payment status after webhook event
    """
    supabase = get_supabase()

    update_data = {
        "status": status.value,
        "updated_at": datetime.utcnow().isoformat(),
    }

    if error_message:
        update_data["error_message"] = error_message

    if status == PaymentStatus.REFUNDED:
        update_data["refunded_at"] = datetime.utcnow().isoformat()

    result = (
        supabase.table("payments")
        .update(update_data)
        .eq("stripe_payment_intent_id", )
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Payment(**result.data[0])
    return None


async def x_update_payment_status__mutmut_19(
    payment_intent_id: str, status: PaymentStatus, error_message: Optional[str] = None
) -> Optional[Payment]:
    """
    Update payment status after webhook event
    """
    supabase = get_supabase()

    update_data = {
        "status": status.value,
        "updated_at": datetime.utcnow().isoformat(),
    }

    if error_message:
        update_data["error_message"] = error_message

    if status == PaymentStatus.REFUNDED:
        update_data["refunded_at"] = datetime.utcnow().isoformat()

    result = (
        supabase.table("payments")
        .update(None)
        .eq("stripe_payment_intent_id", payment_intent_id)
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Payment(**result.data[0])
    return None


async def x_update_payment_status__mutmut_20(
    payment_intent_id: str, status: PaymentStatus, error_message: Optional[str] = None
) -> Optional[Payment]:
    """
    Update payment status after webhook event
    """
    supabase = get_supabase()

    update_data = {
        "status": status.value,
        "updated_at": datetime.utcnow().isoformat(),
    }

    if error_message:
        update_data["error_message"] = error_message

    if status == PaymentStatus.REFUNDED:
        update_data["refunded_at"] = datetime.utcnow().isoformat()

    result = (
        supabase.table(None)
        .update(update_data)
        .eq("stripe_payment_intent_id", payment_intent_id)
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Payment(**result.data[0])
    return None


async def x_update_payment_status__mutmut_21(
    payment_intent_id: str, status: PaymentStatus, error_message: Optional[str] = None
) -> Optional[Payment]:
    """
    Update payment status after webhook event
    """
    supabase = get_supabase()

    update_data = {
        "status": status.value,
        "updated_at": datetime.utcnow().isoformat(),
    }

    if error_message:
        update_data["error_message"] = error_message

    if status == PaymentStatus.REFUNDED:
        update_data["refunded_at"] = datetime.utcnow().isoformat()

    result = (
        supabase.table("XXpaymentsXX")
        .update(update_data)
        .eq("stripe_payment_intent_id", payment_intent_id)
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Payment(**result.data[0])
    return None


async def x_update_payment_status__mutmut_22(
    payment_intent_id: str, status: PaymentStatus, error_message: Optional[str] = None
) -> Optional[Payment]:
    """
    Update payment status after webhook event
    """
    supabase = get_supabase()

    update_data = {
        "status": status.value,
        "updated_at": datetime.utcnow().isoformat(),
    }

    if error_message:
        update_data["error_message"] = error_message

    if status == PaymentStatus.REFUNDED:
        update_data["refunded_at"] = datetime.utcnow().isoformat()

    result = (
        supabase.table("PAYMENTS")
        .update(update_data)
        .eq("stripe_payment_intent_id", payment_intent_id)
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Payment(**result.data[0])
    return None


async def x_update_payment_status__mutmut_23(
    payment_intent_id: str, status: PaymentStatus, error_message: Optional[str] = None
) -> Optional[Payment]:
    """
    Update payment status after webhook event
    """
    supabase = get_supabase()

    update_data = {
        "status": status.value,
        "updated_at": datetime.utcnow().isoformat(),
    }

    if error_message:
        update_data["error_message"] = error_message

    if status == PaymentStatus.REFUNDED:
        update_data["refunded_at"] = datetime.utcnow().isoformat()

    result = (
        supabase.table("payments")
        .update(update_data)
        .eq("XXstripe_payment_intent_idXX", payment_intent_id)
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Payment(**result.data[0])
    return None


async def x_update_payment_status__mutmut_24(
    payment_intent_id: str, status: PaymentStatus, error_message: Optional[str] = None
) -> Optional[Payment]:
    """
    Update payment status after webhook event
    """
    supabase = get_supabase()

    update_data = {
        "status": status.value,
        "updated_at": datetime.utcnow().isoformat(),
    }

    if error_message:
        update_data["error_message"] = error_message

    if status == PaymentStatus.REFUNDED:
        update_data["refunded_at"] = datetime.utcnow().isoformat()

    result = (
        supabase.table("payments")
        .update(update_data)
        .eq("STRIPE_PAYMENT_INTENT_ID", payment_intent_id)
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Payment(**result.data[0])
    return None


async def x_update_payment_status__mutmut_25(
    payment_intent_id: str, status: PaymentStatus, error_message: Optional[str] = None
) -> Optional[Payment]:
    """
    Update payment status after webhook event
    """
    supabase = get_supabase()

    update_data = {
        "status": status.value,
        "updated_at": datetime.utcnow().isoformat(),
    }

    if error_message:
        update_data["error_message"] = error_message

    if status == PaymentStatus.REFUNDED:
        update_data["refunded_at"] = datetime.utcnow().isoformat()

    result = (
        supabase.table("payments")
        .update(update_data)
        .eq("stripe_payment_intent_id", payment_intent_id)
        .execute()
    )

    if result.data or len(result.data) > 0:
        return Payment(**result.data[0])
    return None


async def x_update_payment_status__mutmut_26(
    payment_intent_id: str, status: PaymentStatus, error_message: Optional[str] = None
) -> Optional[Payment]:
    """
    Update payment status after webhook event
    """
    supabase = get_supabase()

    update_data = {
        "status": status.value,
        "updated_at": datetime.utcnow().isoformat(),
    }

    if error_message:
        update_data["error_message"] = error_message

    if status == PaymentStatus.REFUNDED:
        update_data["refunded_at"] = datetime.utcnow().isoformat()

    result = (
        supabase.table("payments")
        .update(update_data)
        .eq("stripe_payment_intent_id", payment_intent_id)
        .execute()
    )

    if result.data and len(result.data) >= 0:
        return Payment(**result.data[0])
    return None


async def x_update_payment_status__mutmut_27(
    payment_intent_id: str, status: PaymentStatus, error_message: Optional[str] = None
) -> Optional[Payment]:
    """
    Update payment status after webhook event
    """
    supabase = get_supabase()

    update_data = {
        "status": status.value,
        "updated_at": datetime.utcnow().isoformat(),
    }

    if error_message:
        update_data["error_message"] = error_message

    if status == PaymentStatus.REFUNDED:
        update_data["refunded_at"] = datetime.utcnow().isoformat()

    result = (
        supabase.table("payments")
        .update(update_data)
        .eq("stripe_payment_intent_id", payment_intent_id)
        .execute()
    )

    if result.data and len(result.data) > 1:
        return Payment(**result.data[0])
    return None


async def x_update_payment_status__mutmut_28(
    payment_intent_id: str, status: PaymentStatus, error_message: Optional[str] = None
) -> Optional[Payment]:
    """
    Update payment status after webhook event
    """
    supabase = get_supabase()

    update_data = {
        "status": status.value,
        "updated_at": datetime.utcnow().isoformat(),
    }

    if error_message:
        update_data["error_message"] = error_message

    if status == PaymentStatus.REFUNDED:
        update_data["refunded_at"] = datetime.utcnow().isoformat()

    result = (
        supabase.table("payments")
        .update(update_data)
        .eq("stripe_payment_intent_id", payment_intent_id)
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Payment(**result.data[1])
    return None

x_update_payment_status__mutmut_mutants : ClassVar[MutantDict] = {
'x_update_payment_status__mutmut_1': x_update_payment_status__mutmut_1, 
    'x_update_payment_status__mutmut_2': x_update_payment_status__mutmut_2, 
    'x_update_payment_status__mutmut_3': x_update_payment_status__mutmut_3, 
    'x_update_payment_status__mutmut_4': x_update_payment_status__mutmut_4, 
    'x_update_payment_status__mutmut_5': x_update_payment_status__mutmut_5, 
    'x_update_payment_status__mutmut_6': x_update_payment_status__mutmut_6, 
    'x_update_payment_status__mutmut_7': x_update_payment_status__mutmut_7, 
    'x_update_payment_status__mutmut_8': x_update_payment_status__mutmut_8, 
    'x_update_payment_status__mutmut_9': x_update_payment_status__mutmut_9, 
    'x_update_payment_status__mutmut_10': x_update_payment_status__mutmut_10, 
    'x_update_payment_status__mutmut_11': x_update_payment_status__mutmut_11, 
    'x_update_payment_status__mutmut_12': x_update_payment_status__mutmut_12, 
    'x_update_payment_status__mutmut_13': x_update_payment_status__mutmut_13, 
    'x_update_payment_status__mutmut_14': x_update_payment_status__mutmut_14, 
    'x_update_payment_status__mutmut_15': x_update_payment_status__mutmut_15, 
    'x_update_payment_status__mutmut_16': x_update_payment_status__mutmut_16, 
    'x_update_payment_status__mutmut_17': x_update_payment_status__mutmut_17, 
    'x_update_payment_status__mutmut_18': x_update_payment_status__mutmut_18, 
    'x_update_payment_status__mutmut_19': x_update_payment_status__mutmut_19, 
    'x_update_payment_status__mutmut_20': x_update_payment_status__mutmut_20, 
    'x_update_payment_status__mutmut_21': x_update_payment_status__mutmut_21, 
    'x_update_payment_status__mutmut_22': x_update_payment_status__mutmut_22, 
    'x_update_payment_status__mutmut_23': x_update_payment_status__mutmut_23, 
    'x_update_payment_status__mutmut_24': x_update_payment_status__mutmut_24, 
    'x_update_payment_status__mutmut_25': x_update_payment_status__mutmut_25, 
    'x_update_payment_status__mutmut_26': x_update_payment_status__mutmut_26, 
    'x_update_payment_status__mutmut_27': x_update_payment_status__mutmut_27, 
    'x_update_payment_status__mutmut_28': x_update_payment_status__mutmut_28
}

def update_payment_status(*args, **kwargs):
    result = _mutmut_trampoline(x_update_payment_status__mutmut_orig, x_update_payment_status__mutmut_mutants, args, kwargs)
    return result 

update_payment_status.__signature__ = _mutmut_signature(x_update_payment_status__mutmut_orig)
x_update_payment_status__mutmut_orig.__name__ = 'x_update_payment_status'


async def x_get_payment_by_intent_id__mutmut_orig(payment_intent_id: str) -> Optional[Payment]:
    """
    Get payment record by Stripe payment intent ID
    """
    supabase = get_supabase()

    result = (
        supabase.table("payments")
        .select("*")
        .eq("stripe_payment_intent_id", payment_intent_id)
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Payment(**result.data[0])
    return None


async def x_get_payment_by_intent_id__mutmut_1(payment_intent_id: str) -> Optional[Payment]:
    """
    Get payment record by Stripe payment intent ID
    """
    supabase = None

    result = (
        supabase.table("payments")
        .select("*")
        .eq("stripe_payment_intent_id", payment_intent_id)
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Payment(**result.data[0])
    return None


async def x_get_payment_by_intent_id__mutmut_2(payment_intent_id: str) -> Optional[Payment]:
    """
    Get payment record by Stripe payment intent ID
    """
    supabase = get_supabase()

    result = None

    if result.data and len(result.data) > 0:
        return Payment(**result.data[0])
    return None


async def x_get_payment_by_intent_id__mutmut_3(payment_intent_id: str) -> Optional[Payment]:
    """
    Get payment record by Stripe payment intent ID
    """
    supabase = get_supabase()

    result = (
        supabase.table("payments")
        .select("*")
        .eq(None, payment_intent_id)
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Payment(**result.data[0])
    return None


async def x_get_payment_by_intent_id__mutmut_4(payment_intent_id: str) -> Optional[Payment]:
    """
    Get payment record by Stripe payment intent ID
    """
    supabase = get_supabase()

    result = (
        supabase.table("payments")
        .select("*")
        .eq("stripe_payment_intent_id", None)
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Payment(**result.data[0])
    return None


async def x_get_payment_by_intent_id__mutmut_5(payment_intent_id: str) -> Optional[Payment]:
    """
    Get payment record by Stripe payment intent ID
    """
    supabase = get_supabase()

    result = (
        supabase.table("payments")
        .select("*")
        .eq(payment_intent_id)
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Payment(**result.data[0])
    return None


async def x_get_payment_by_intent_id__mutmut_6(payment_intent_id: str) -> Optional[Payment]:
    """
    Get payment record by Stripe payment intent ID
    """
    supabase = get_supabase()

    result = (
        supabase.table("payments")
        .select("*")
        .eq("stripe_payment_intent_id", )
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Payment(**result.data[0])
    return None


async def x_get_payment_by_intent_id__mutmut_7(payment_intent_id: str) -> Optional[Payment]:
    """
    Get payment record by Stripe payment intent ID
    """
    supabase = get_supabase()

    result = (
        supabase.table("payments")
        .select(None)
        .eq("stripe_payment_intent_id", payment_intent_id)
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Payment(**result.data[0])
    return None


async def x_get_payment_by_intent_id__mutmut_8(payment_intent_id: str) -> Optional[Payment]:
    """
    Get payment record by Stripe payment intent ID
    """
    supabase = get_supabase()

    result = (
        supabase.table(None)
        .select("*")
        .eq("stripe_payment_intent_id", payment_intent_id)
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Payment(**result.data[0])
    return None


async def x_get_payment_by_intent_id__mutmut_9(payment_intent_id: str) -> Optional[Payment]:
    """
    Get payment record by Stripe payment intent ID
    """
    supabase = get_supabase()

    result = (
        supabase.table("XXpaymentsXX")
        .select("*")
        .eq("stripe_payment_intent_id", payment_intent_id)
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Payment(**result.data[0])
    return None


async def x_get_payment_by_intent_id__mutmut_10(payment_intent_id: str) -> Optional[Payment]:
    """
    Get payment record by Stripe payment intent ID
    """
    supabase = get_supabase()

    result = (
        supabase.table("PAYMENTS")
        .select("*")
        .eq("stripe_payment_intent_id", payment_intent_id)
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Payment(**result.data[0])
    return None


async def x_get_payment_by_intent_id__mutmut_11(payment_intent_id: str) -> Optional[Payment]:
    """
    Get payment record by Stripe payment intent ID
    """
    supabase = get_supabase()

    result = (
        supabase.table("payments")
        .select("XX*XX")
        .eq("stripe_payment_intent_id", payment_intent_id)
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Payment(**result.data[0])
    return None


async def x_get_payment_by_intent_id__mutmut_12(payment_intent_id: str) -> Optional[Payment]:
    """
    Get payment record by Stripe payment intent ID
    """
    supabase = get_supabase()

    result = (
        supabase.table("payments")
        .select("*")
        .eq("XXstripe_payment_intent_idXX", payment_intent_id)
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Payment(**result.data[0])
    return None


async def x_get_payment_by_intent_id__mutmut_13(payment_intent_id: str) -> Optional[Payment]:
    """
    Get payment record by Stripe payment intent ID
    """
    supabase = get_supabase()

    result = (
        supabase.table("payments")
        .select("*")
        .eq("STRIPE_PAYMENT_INTENT_ID", payment_intent_id)
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Payment(**result.data[0])
    return None


async def x_get_payment_by_intent_id__mutmut_14(payment_intent_id: str) -> Optional[Payment]:
    """
    Get payment record by Stripe payment intent ID
    """
    supabase = get_supabase()

    result = (
        supabase.table("payments")
        .select("*")
        .eq("stripe_payment_intent_id", payment_intent_id)
        .execute()
    )

    if result.data or len(result.data) > 0:
        return Payment(**result.data[0])
    return None


async def x_get_payment_by_intent_id__mutmut_15(payment_intent_id: str) -> Optional[Payment]:
    """
    Get payment record by Stripe payment intent ID
    """
    supabase = get_supabase()

    result = (
        supabase.table("payments")
        .select("*")
        .eq("stripe_payment_intent_id", payment_intent_id)
        .execute()
    )

    if result.data and len(result.data) >= 0:
        return Payment(**result.data[0])
    return None


async def x_get_payment_by_intent_id__mutmut_16(payment_intent_id: str) -> Optional[Payment]:
    """
    Get payment record by Stripe payment intent ID
    """
    supabase = get_supabase()

    result = (
        supabase.table("payments")
        .select("*")
        .eq("stripe_payment_intent_id", payment_intent_id)
        .execute()
    )

    if result.data and len(result.data) > 1:
        return Payment(**result.data[0])
    return None


async def x_get_payment_by_intent_id__mutmut_17(payment_intent_id: str) -> Optional[Payment]:
    """
    Get payment record by Stripe payment intent ID
    """
    supabase = get_supabase()

    result = (
        supabase.table("payments")
        .select("*")
        .eq("stripe_payment_intent_id", payment_intent_id)
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Payment(**result.data[1])
    return None

x_get_payment_by_intent_id__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_payment_by_intent_id__mutmut_1': x_get_payment_by_intent_id__mutmut_1, 
    'x_get_payment_by_intent_id__mutmut_2': x_get_payment_by_intent_id__mutmut_2, 
    'x_get_payment_by_intent_id__mutmut_3': x_get_payment_by_intent_id__mutmut_3, 
    'x_get_payment_by_intent_id__mutmut_4': x_get_payment_by_intent_id__mutmut_4, 
    'x_get_payment_by_intent_id__mutmut_5': x_get_payment_by_intent_id__mutmut_5, 
    'x_get_payment_by_intent_id__mutmut_6': x_get_payment_by_intent_id__mutmut_6, 
    'x_get_payment_by_intent_id__mutmut_7': x_get_payment_by_intent_id__mutmut_7, 
    'x_get_payment_by_intent_id__mutmut_8': x_get_payment_by_intent_id__mutmut_8, 
    'x_get_payment_by_intent_id__mutmut_9': x_get_payment_by_intent_id__mutmut_9, 
    'x_get_payment_by_intent_id__mutmut_10': x_get_payment_by_intent_id__mutmut_10, 
    'x_get_payment_by_intent_id__mutmut_11': x_get_payment_by_intent_id__mutmut_11, 
    'x_get_payment_by_intent_id__mutmut_12': x_get_payment_by_intent_id__mutmut_12, 
    'x_get_payment_by_intent_id__mutmut_13': x_get_payment_by_intent_id__mutmut_13, 
    'x_get_payment_by_intent_id__mutmut_14': x_get_payment_by_intent_id__mutmut_14, 
    'x_get_payment_by_intent_id__mutmut_15': x_get_payment_by_intent_id__mutmut_15, 
    'x_get_payment_by_intent_id__mutmut_16': x_get_payment_by_intent_id__mutmut_16, 
    'x_get_payment_by_intent_id__mutmut_17': x_get_payment_by_intent_id__mutmut_17
}

def get_payment_by_intent_id(*args, **kwargs):
    result = _mutmut_trampoline(x_get_payment_by_intent_id__mutmut_orig, x_get_payment_by_intent_id__mutmut_mutants, args, kwargs)
    return result 

get_payment_by_intent_id.__signature__ = _mutmut_signature(x_get_payment_by_intent_id__mutmut_orig)
x_get_payment_by_intent_id__mutmut_orig.__name__ = 'x_get_payment_by_intent_id'


def x_verify_webhook_signature__mutmut_orig(payload: bytes, sig_header: str) -> dict:
    """
    Verify Stripe webhook signature
    Returns the event object if valid
    """
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
        return event
    except ValueError:
        raise Exception("Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise Exception("Invalid signature")


def x_verify_webhook_signature__mutmut_1(payload: bytes, sig_header: str) -> dict:
    """
    Verify Stripe webhook signature
    Returns the event object if valid
    """
    try:
        event = None
        return event
    except ValueError:
        raise Exception("Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise Exception("Invalid signature")


def x_verify_webhook_signature__mutmut_2(payload: bytes, sig_header: str) -> dict:
    """
    Verify Stripe webhook signature
    Returns the event object if valid
    """
    try:
        event = stripe.Webhook.construct_event(None, sig_header, settings.STRIPE_WEBHOOK_SECRET)
        return event
    except ValueError:
        raise Exception("Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise Exception("Invalid signature")


def x_verify_webhook_signature__mutmut_3(payload: bytes, sig_header: str) -> dict:
    """
    Verify Stripe webhook signature
    Returns the event object if valid
    """
    try:
        event = stripe.Webhook.construct_event(payload, None, settings.STRIPE_WEBHOOK_SECRET)
        return event
    except ValueError:
        raise Exception("Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise Exception("Invalid signature")


def x_verify_webhook_signature__mutmut_4(payload: bytes, sig_header: str) -> dict:
    """
    Verify Stripe webhook signature
    Returns the event object if valid
    """
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, None)
        return event
    except ValueError:
        raise Exception("Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise Exception("Invalid signature")


def x_verify_webhook_signature__mutmut_5(payload: bytes, sig_header: str) -> dict:
    """
    Verify Stripe webhook signature
    Returns the event object if valid
    """
    try:
        event = stripe.Webhook.construct_event(sig_header, settings.STRIPE_WEBHOOK_SECRET)
        return event
    except ValueError:
        raise Exception("Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise Exception("Invalid signature")


def x_verify_webhook_signature__mutmut_6(payload: bytes, sig_header: str) -> dict:
    """
    Verify Stripe webhook signature
    Returns the event object if valid
    """
    try:
        event = stripe.Webhook.construct_event(payload, settings.STRIPE_WEBHOOK_SECRET)
        return event
    except ValueError:
        raise Exception("Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise Exception("Invalid signature")


def x_verify_webhook_signature__mutmut_7(payload: bytes, sig_header: str) -> dict:
    """
    Verify Stripe webhook signature
    Returns the event object if valid
    """
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, )
        return event
    except ValueError:
        raise Exception("Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise Exception("Invalid signature")


def x_verify_webhook_signature__mutmut_8(payload: bytes, sig_header: str) -> dict:
    """
    Verify Stripe webhook signature
    Returns the event object if valid
    """
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
        return event
    except ValueError:
        raise Exception(None)
    except stripe.error.SignatureVerificationError:
        raise Exception("Invalid signature")


def x_verify_webhook_signature__mutmut_9(payload: bytes, sig_header: str) -> dict:
    """
    Verify Stripe webhook signature
    Returns the event object if valid
    """
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
        return event
    except ValueError:
        raise Exception("XXInvalid payloadXX")
    except stripe.error.SignatureVerificationError:
        raise Exception("Invalid signature")


def x_verify_webhook_signature__mutmut_10(payload: bytes, sig_header: str) -> dict:
    """
    Verify Stripe webhook signature
    Returns the event object if valid
    """
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
        return event
    except ValueError:
        raise Exception("invalid payload")
    except stripe.error.SignatureVerificationError:
        raise Exception("Invalid signature")


def x_verify_webhook_signature__mutmut_11(payload: bytes, sig_header: str) -> dict:
    """
    Verify Stripe webhook signature
    Returns the event object if valid
    """
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
        return event
    except ValueError:
        raise Exception("INVALID PAYLOAD")
    except stripe.error.SignatureVerificationError:
        raise Exception("Invalid signature")


def x_verify_webhook_signature__mutmut_12(payload: bytes, sig_header: str) -> dict:
    """
    Verify Stripe webhook signature
    Returns the event object if valid
    """
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
        return event
    except ValueError:
        raise Exception("Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise Exception(None)


def x_verify_webhook_signature__mutmut_13(payload: bytes, sig_header: str) -> dict:
    """
    Verify Stripe webhook signature
    Returns the event object if valid
    """
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
        return event
    except ValueError:
        raise Exception("Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise Exception("XXInvalid signatureXX")


def x_verify_webhook_signature__mutmut_14(payload: bytes, sig_header: str) -> dict:
    """
    Verify Stripe webhook signature
    Returns the event object if valid
    """
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
        return event
    except ValueError:
        raise Exception("Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise Exception("invalid signature")


def x_verify_webhook_signature__mutmut_15(payload: bytes, sig_header: str) -> dict:
    """
    Verify Stripe webhook signature
    Returns the event object if valid
    """
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
        return event
    except ValueError:
        raise Exception("Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise Exception("INVALID SIGNATURE")

x_verify_webhook_signature__mutmut_mutants : ClassVar[MutantDict] = {
'x_verify_webhook_signature__mutmut_1': x_verify_webhook_signature__mutmut_1, 
    'x_verify_webhook_signature__mutmut_2': x_verify_webhook_signature__mutmut_2, 
    'x_verify_webhook_signature__mutmut_3': x_verify_webhook_signature__mutmut_3, 
    'x_verify_webhook_signature__mutmut_4': x_verify_webhook_signature__mutmut_4, 
    'x_verify_webhook_signature__mutmut_5': x_verify_webhook_signature__mutmut_5, 
    'x_verify_webhook_signature__mutmut_6': x_verify_webhook_signature__mutmut_6, 
    'x_verify_webhook_signature__mutmut_7': x_verify_webhook_signature__mutmut_7, 
    'x_verify_webhook_signature__mutmut_8': x_verify_webhook_signature__mutmut_8, 
    'x_verify_webhook_signature__mutmut_9': x_verify_webhook_signature__mutmut_9, 
    'x_verify_webhook_signature__mutmut_10': x_verify_webhook_signature__mutmut_10, 
    'x_verify_webhook_signature__mutmut_11': x_verify_webhook_signature__mutmut_11, 
    'x_verify_webhook_signature__mutmut_12': x_verify_webhook_signature__mutmut_12, 
    'x_verify_webhook_signature__mutmut_13': x_verify_webhook_signature__mutmut_13, 
    'x_verify_webhook_signature__mutmut_14': x_verify_webhook_signature__mutmut_14, 
    'x_verify_webhook_signature__mutmut_15': x_verify_webhook_signature__mutmut_15
}

def verify_webhook_signature(*args, **kwargs):
    result = _mutmut_trampoline(x_verify_webhook_signature__mutmut_orig, x_verify_webhook_signature__mutmut_mutants, args, kwargs)
    return result 

verify_webhook_signature.__signature__ = _mutmut_signature(x_verify_webhook_signature__mutmut_orig)
x_verify_webhook_signature__mutmut_orig.__name__ = 'x_verify_webhook_signature'
