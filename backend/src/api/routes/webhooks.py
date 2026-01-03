"""
Webhook routes for external service callbacks
Handles Stripe payment webhooks

Integrates with dependency injection for database, logging, and feature flags.
"""

from fastapi import APIRouter, Request, HTTPException, Header, Depends
from typing import Optional
import structlog

from api.services.payment_service import (
    verify_webhook_signature,
    update_payment_status,
)
from api.services.report_service import trigger_report_generation
from api.models.payment import PaymentStatus
from dependencies import (
    get_db,
    get_request_logger,
    get_feature_flags,
)
from database.types import DatabaseAdapter
from feature_flags.evaluator import FeatureFlagEvaluator
from feature_flags.types import Feature

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])


@router.post("/stripe")
async def stripe_webhook(
    request: Request,
    stripe_signature: Optional[str] = Header(None, alias="stripe-signature"),
    db: DatabaseAdapter = Depends(get_db),
    logger: structlog.BoundLogger = Depends(get_request_logger),
    feature_flags: FeatureFlagEvaluator = Depends(get_feature_flags),
):
    """
    Handle Stripe webhook events

    Supported events:
    - payment_intent.succeeded: Payment completed successfully
    - payment_intent.payment_failed: Payment failed
    - charge.refunded: Payment refunded

    Only processes webhooks if ENABLE_PAYMENTS is true.
    """
    # Check if payments are enabled
    if not feature_flags.is_enabled(Feature.PAYMENTS):
        logger.warning("stripe_webhook_received_but_payments_disabled")
        raise HTTPException(
            status_code=403, detail="Payment webhooks are disabled in current environment"
        )

    if not stripe_signature:
        logger.warning("stripe_webhook_missing_signature")
        raise HTTPException(status_code=400, detail="Missing stripe-signature header")

    try:
        # Get raw request body
        payload = await request.body()

        # Verify webhook signature
        event = verify_webhook_signature(payload, stripe_signature)

        logger.info(
            "stripe_webhook_received",
            event_type=event["type"],
            event_id=event["id"],
        )

        # Handle different event types
        event_type = event["type"]
        payment_intent = event["data"]["object"]

        if event_type == "payment_intent.succeeded":
            await handle_payment_succeeded(payment_intent, logger)

        elif event_type == "payment_intent.payment_failed":
            await handle_payment_failed(payment_intent, logger)

        elif event_type == "charge.refunded":
            await handle_charge_refunded(payment_intent, logger)

        else:
            logger.info("stripe_webhook_ignored", event_type=event_type)

        return {"status": "success"}

    except Exception as e:
        logger.error("stripe_webhook_error", error=str(e), exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))


async def handle_payment_succeeded(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle successful payment
    Update payment status and trigger report generation
    """
    payment_intent_id = payment_intent["id"]

    logger.info("payment_succeeded", payment_intent_id=payment_intent_id)

    # Update payment status
    payment = await update_payment_status(
        payment_intent_id=payment_intent_id,
        status=PaymentStatus.SUCCEEDED,
    )

    if not payment:
        logger.error("payment_not_found", payment_intent_id=payment_intent_id)
        return

    # Trigger report generation
    try:
        await trigger_report_generation(payment.report_id)
        logger.info("report_generation_triggered", report_id=payment.report_id)
    except Exception as e:
        logger.error(
            "report_generation_failed",
            report_id=payment.report_id,
            error=str(e),
            exc_info=True,
        )


async def handle_payment_failed(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle failed payment
    Update payment status with error message
    """
    payment_intent_id = payment_intent["id"]
    error_message = payment_intent.get("last_payment_error", {}).get("message", "Payment failed")

    logger.info("payment_failed", payment_intent_id=payment_intent_id, error=error_message)

    await update_payment_status(
        payment_intent_id=payment_intent_id,
        status=PaymentStatus.FAILED,
        error_message=error_message,
    )


async def handle_charge_refunded(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle refunded payment
    Update payment status
    """
    payment_intent_id = payment_intent.get("payment_intent")

    if not payment_intent_id:
        logger.warning("charge_refunded_missing_payment_intent")
        return

    logger.info("charge_refunded", payment_intent_id=payment_intent_id)

    await update_payment_status(
        payment_intent_id=payment_intent_id,
        status=PaymentStatus.REFUNDED,
    )
