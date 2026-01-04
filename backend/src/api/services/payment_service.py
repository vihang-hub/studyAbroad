"""
Payment service for Stripe integration
Handles checkout session creation and webhook processing
"""

import stripe
from datetime import datetime
from typing import Optional
from src.config import settings
from src.api.models.payment import Payment, PaymentStatus, CreateCheckoutResponse
from src.feature_flags import feature_flags, Feature

# Note: get_supabase is imported dynamically in _get_supabase() to avoid
# initialization errors when Supabase is disabled

# Initialize Stripe (will be None if key not set)
stripe.api_key = settings.STRIPE_SECRET_KEY


def _is_payments_enabled() -> bool:
    """Check if payments are enabled via feature flag"""
    return feature_flags.is_enabled(Feature.PAYMENTS)


def _is_supabase_enabled() -> bool:
    """Check if Supabase is enabled via feature flag"""
    return feature_flags.is_enabled(Feature.SUPABASE)


def _get_supabase():
    """Get Supabase client only when enabled"""
    if not _is_supabase_enabled():
        raise RuntimeError("Supabase is disabled in dev mode")
    from src.lib.supabase import get_supabase
    return get_supabase()


async def create_checkout_session(
    user_id: str, report_id: str, query: str
) -> CreateCheckoutResponse:
    """
    Create Stripe payment intent for report generation
    Returns client secret for frontend Stripe Elements
    """
    # In dev mode without payments enabled, this shouldn't be called
    # but provide protection anyway
    if not _is_payments_enabled():
        raise RuntimeError("Payments are disabled in dev mode")

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

        # Create Payment record in database (only if Supabase is enabled)
        if _is_supabase_enabled():
            supabase = _get_supabase()
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


async def update_payment_status(
    payment_intent_id: str, status: PaymentStatus, error_message: Optional[str] = None
) -> Optional[Payment]:
    """
    Update payment status after webhook event
    """
    # In dev mode without Supabase, return None
    if not _is_supabase_enabled():
        return None

    supabase = _get_supabase()

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


async def get_payment_by_intent_id(payment_intent_id: str) -> Optional[Payment]:
    """
    Get payment record by Stripe payment intent ID
    """
    # In dev mode without Supabase, return None
    if not _is_supabase_enabled():
        return None

    supabase = _get_supabase()

    result = (
        supabase.table("payments")
        .select("*")
        .eq("stripe_payment_intent_id", payment_intent_id)
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Payment(**result.data[0])
    return None


def verify_webhook_signature(payload: bytes, sig_header: str) -> dict:
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
