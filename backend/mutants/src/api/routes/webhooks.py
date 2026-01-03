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


async def x_handle_payment_succeeded__mutmut_orig(payment_intent: dict, logger: structlog.BoundLogger):
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


async def x_handle_payment_succeeded__mutmut_1(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle successful payment
    Update payment status and trigger report generation
    """
    payment_intent_id = None

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


async def x_handle_payment_succeeded__mutmut_2(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle successful payment
    Update payment status and trigger report generation
    """
    payment_intent_id = payment_intent["XXidXX"]

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


async def x_handle_payment_succeeded__mutmut_3(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle successful payment
    Update payment status and trigger report generation
    """
    payment_intent_id = payment_intent["ID"]

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


async def x_handle_payment_succeeded__mutmut_4(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle successful payment
    Update payment status and trigger report generation
    """
    payment_intent_id = payment_intent["id"]

    logger.info(None, payment_intent_id=payment_intent_id)

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


async def x_handle_payment_succeeded__mutmut_5(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle successful payment
    Update payment status and trigger report generation
    """
    payment_intent_id = payment_intent["id"]

    logger.info("payment_succeeded", payment_intent_id=None)

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


async def x_handle_payment_succeeded__mutmut_6(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle successful payment
    Update payment status and trigger report generation
    """
    payment_intent_id = payment_intent["id"]

    logger.info(payment_intent_id=payment_intent_id)

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


async def x_handle_payment_succeeded__mutmut_7(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle successful payment
    Update payment status and trigger report generation
    """
    payment_intent_id = payment_intent["id"]

    logger.info("payment_succeeded", )

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


async def x_handle_payment_succeeded__mutmut_8(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle successful payment
    Update payment status and trigger report generation
    """
    payment_intent_id = payment_intent["id"]

    logger.info("XXpayment_succeededXX", payment_intent_id=payment_intent_id)

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


async def x_handle_payment_succeeded__mutmut_9(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle successful payment
    Update payment status and trigger report generation
    """
    payment_intent_id = payment_intent["id"]

    logger.info("PAYMENT_SUCCEEDED", payment_intent_id=payment_intent_id)

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


async def x_handle_payment_succeeded__mutmut_10(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle successful payment
    Update payment status and trigger report generation
    """
    payment_intent_id = payment_intent["id"]

    logger.info("payment_succeeded", payment_intent_id=payment_intent_id)

    # Update payment status
    payment = None

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


async def x_handle_payment_succeeded__mutmut_11(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle successful payment
    Update payment status and trigger report generation
    """
    payment_intent_id = payment_intent["id"]

    logger.info("payment_succeeded", payment_intent_id=payment_intent_id)

    # Update payment status
    payment = await update_payment_status(
        payment_intent_id=None,
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


async def x_handle_payment_succeeded__mutmut_12(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle successful payment
    Update payment status and trigger report generation
    """
    payment_intent_id = payment_intent["id"]

    logger.info("payment_succeeded", payment_intent_id=payment_intent_id)

    # Update payment status
    payment = await update_payment_status(
        payment_intent_id=payment_intent_id,
        status=None,
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


async def x_handle_payment_succeeded__mutmut_13(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle successful payment
    Update payment status and trigger report generation
    """
    payment_intent_id = payment_intent["id"]

    logger.info("payment_succeeded", payment_intent_id=payment_intent_id)

    # Update payment status
    payment = await update_payment_status(
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


async def x_handle_payment_succeeded__mutmut_14(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle successful payment
    Update payment status and trigger report generation
    """
    payment_intent_id = payment_intent["id"]

    logger.info("payment_succeeded", payment_intent_id=payment_intent_id)

    # Update payment status
    payment = await update_payment_status(
        payment_intent_id=payment_intent_id,
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


async def x_handle_payment_succeeded__mutmut_15(payment_intent: dict, logger: structlog.BoundLogger):
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

    if payment:
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


async def x_handle_payment_succeeded__mutmut_16(payment_intent: dict, logger: structlog.BoundLogger):
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
        logger.error(None, payment_intent_id=payment_intent_id)
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


async def x_handle_payment_succeeded__mutmut_17(payment_intent: dict, logger: structlog.BoundLogger):
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
        logger.error("payment_not_found", payment_intent_id=None)
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


async def x_handle_payment_succeeded__mutmut_18(payment_intent: dict, logger: structlog.BoundLogger):
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
        logger.error(payment_intent_id=payment_intent_id)
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


async def x_handle_payment_succeeded__mutmut_19(payment_intent: dict, logger: structlog.BoundLogger):
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
        logger.error("payment_not_found", )
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


async def x_handle_payment_succeeded__mutmut_20(payment_intent: dict, logger: structlog.BoundLogger):
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
        logger.error("XXpayment_not_foundXX", payment_intent_id=payment_intent_id)
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


async def x_handle_payment_succeeded__mutmut_21(payment_intent: dict, logger: structlog.BoundLogger):
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
        logger.error("PAYMENT_NOT_FOUND", payment_intent_id=payment_intent_id)
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


async def x_handle_payment_succeeded__mutmut_22(payment_intent: dict, logger: structlog.BoundLogger):
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
        await trigger_report_generation(None)
        logger.info("report_generation_triggered", report_id=payment.report_id)
    except Exception as e:
        logger.error(
            "report_generation_failed",
            report_id=payment.report_id,
            error=str(e),
            exc_info=True,
        )


async def x_handle_payment_succeeded__mutmut_23(payment_intent: dict, logger: structlog.BoundLogger):
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
        logger.info(None, report_id=payment.report_id)
    except Exception as e:
        logger.error(
            "report_generation_failed",
            report_id=payment.report_id,
            error=str(e),
            exc_info=True,
        )


async def x_handle_payment_succeeded__mutmut_24(payment_intent: dict, logger: structlog.BoundLogger):
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
        logger.info("report_generation_triggered", report_id=None)
    except Exception as e:
        logger.error(
            "report_generation_failed",
            report_id=payment.report_id,
            error=str(e),
            exc_info=True,
        )


async def x_handle_payment_succeeded__mutmut_25(payment_intent: dict, logger: structlog.BoundLogger):
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
        logger.info(report_id=payment.report_id)
    except Exception as e:
        logger.error(
            "report_generation_failed",
            report_id=payment.report_id,
            error=str(e),
            exc_info=True,
        )


async def x_handle_payment_succeeded__mutmut_26(payment_intent: dict, logger: structlog.BoundLogger):
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
        logger.info("report_generation_triggered", )
    except Exception as e:
        logger.error(
            "report_generation_failed",
            report_id=payment.report_id,
            error=str(e),
            exc_info=True,
        )


async def x_handle_payment_succeeded__mutmut_27(payment_intent: dict, logger: structlog.BoundLogger):
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
        logger.info("XXreport_generation_triggeredXX", report_id=payment.report_id)
    except Exception as e:
        logger.error(
            "report_generation_failed",
            report_id=payment.report_id,
            error=str(e),
            exc_info=True,
        )


async def x_handle_payment_succeeded__mutmut_28(payment_intent: dict, logger: structlog.BoundLogger):
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
        logger.info("REPORT_GENERATION_TRIGGERED", report_id=payment.report_id)
    except Exception as e:
        logger.error(
            "report_generation_failed",
            report_id=payment.report_id,
            error=str(e),
            exc_info=True,
        )


async def x_handle_payment_succeeded__mutmut_29(payment_intent: dict, logger: structlog.BoundLogger):
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
            None,
            report_id=payment.report_id,
            error=str(e),
            exc_info=True,
        )


async def x_handle_payment_succeeded__mutmut_30(payment_intent: dict, logger: structlog.BoundLogger):
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
            report_id=None,
            error=str(e),
            exc_info=True,
        )


async def x_handle_payment_succeeded__mutmut_31(payment_intent: dict, logger: structlog.BoundLogger):
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
            error=None,
            exc_info=True,
        )


async def x_handle_payment_succeeded__mutmut_32(payment_intent: dict, logger: structlog.BoundLogger):
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
            exc_info=None,
        )


async def x_handle_payment_succeeded__mutmut_33(payment_intent: dict, logger: structlog.BoundLogger):
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
            report_id=payment.report_id,
            error=str(e),
            exc_info=True,
        )


async def x_handle_payment_succeeded__mutmut_34(payment_intent: dict, logger: structlog.BoundLogger):
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
            error=str(e),
            exc_info=True,
        )


async def x_handle_payment_succeeded__mutmut_35(payment_intent: dict, logger: structlog.BoundLogger):
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
            exc_info=True,
        )


async def x_handle_payment_succeeded__mutmut_36(payment_intent: dict, logger: structlog.BoundLogger):
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
            )


async def x_handle_payment_succeeded__mutmut_37(payment_intent: dict, logger: structlog.BoundLogger):
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
            "XXreport_generation_failedXX",
            report_id=payment.report_id,
            error=str(e),
            exc_info=True,
        )


async def x_handle_payment_succeeded__mutmut_38(payment_intent: dict, logger: structlog.BoundLogger):
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
            "REPORT_GENERATION_FAILED",
            report_id=payment.report_id,
            error=str(e),
            exc_info=True,
        )


async def x_handle_payment_succeeded__mutmut_39(payment_intent: dict, logger: structlog.BoundLogger):
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
            error=str(None),
            exc_info=True,
        )


async def x_handle_payment_succeeded__mutmut_40(payment_intent: dict, logger: structlog.BoundLogger):
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
            exc_info=False,
        )

x_handle_payment_succeeded__mutmut_mutants : ClassVar[MutantDict] = {
'x_handle_payment_succeeded__mutmut_1': x_handle_payment_succeeded__mutmut_1, 
    'x_handle_payment_succeeded__mutmut_2': x_handle_payment_succeeded__mutmut_2, 
    'x_handle_payment_succeeded__mutmut_3': x_handle_payment_succeeded__mutmut_3, 
    'x_handle_payment_succeeded__mutmut_4': x_handle_payment_succeeded__mutmut_4, 
    'x_handle_payment_succeeded__mutmut_5': x_handle_payment_succeeded__mutmut_5, 
    'x_handle_payment_succeeded__mutmut_6': x_handle_payment_succeeded__mutmut_6, 
    'x_handle_payment_succeeded__mutmut_7': x_handle_payment_succeeded__mutmut_7, 
    'x_handle_payment_succeeded__mutmut_8': x_handle_payment_succeeded__mutmut_8, 
    'x_handle_payment_succeeded__mutmut_9': x_handle_payment_succeeded__mutmut_9, 
    'x_handle_payment_succeeded__mutmut_10': x_handle_payment_succeeded__mutmut_10, 
    'x_handle_payment_succeeded__mutmut_11': x_handle_payment_succeeded__mutmut_11, 
    'x_handle_payment_succeeded__mutmut_12': x_handle_payment_succeeded__mutmut_12, 
    'x_handle_payment_succeeded__mutmut_13': x_handle_payment_succeeded__mutmut_13, 
    'x_handle_payment_succeeded__mutmut_14': x_handle_payment_succeeded__mutmut_14, 
    'x_handle_payment_succeeded__mutmut_15': x_handle_payment_succeeded__mutmut_15, 
    'x_handle_payment_succeeded__mutmut_16': x_handle_payment_succeeded__mutmut_16, 
    'x_handle_payment_succeeded__mutmut_17': x_handle_payment_succeeded__mutmut_17, 
    'x_handle_payment_succeeded__mutmut_18': x_handle_payment_succeeded__mutmut_18, 
    'x_handle_payment_succeeded__mutmut_19': x_handle_payment_succeeded__mutmut_19, 
    'x_handle_payment_succeeded__mutmut_20': x_handle_payment_succeeded__mutmut_20, 
    'x_handle_payment_succeeded__mutmut_21': x_handle_payment_succeeded__mutmut_21, 
    'x_handle_payment_succeeded__mutmut_22': x_handle_payment_succeeded__mutmut_22, 
    'x_handle_payment_succeeded__mutmut_23': x_handle_payment_succeeded__mutmut_23, 
    'x_handle_payment_succeeded__mutmut_24': x_handle_payment_succeeded__mutmut_24, 
    'x_handle_payment_succeeded__mutmut_25': x_handle_payment_succeeded__mutmut_25, 
    'x_handle_payment_succeeded__mutmut_26': x_handle_payment_succeeded__mutmut_26, 
    'x_handle_payment_succeeded__mutmut_27': x_handle_payment_succeeded__mutmut_27, 
    'x_handle_payment_succeeded__mutmut_28': x_handle_payment_succeeded__mutmut_28, 
    'x_handle_payment_succeeded__mutmut_29': x_handle_payment_succeeded__mutmut_29, 
    'x_handle_payment_succeeded__mutmut_30': x_handle_payment_succeeded__mutmut_30, 
    'x_handle_payment_succeeded__mutmut_31': x_handle_payment_succeeded__mutmut_31, 
    'x_handle_payment_succeeded__mutmut_32': x_handle_payment_succeeded__mutmut_32, 
    'x_handle_payment_succeeded__mutmut_33': x_handle_payment_succeeded__mutmut_33, 
    'x_handle_payment_succeeded__mutmut_34': x_handle_payment_succeeded__mutmut_34, 
    'x_handle_payment_succeeded__mutmut_35': x_handle_payment_succeeded__mutmut_35, 
    'x_handle_payment_succeeded__mutmut_36': x_handle_payment_succeeded__mutmut_36, 
    'x_handle_payment_succeeded__mutmut_37': x_handle_payment_succeeded__mutmut_37, 
    'x_handle_payment_succeeded__mutmut_38': x_handle_payment_succeeded__mutmut_38, 
    'x_handle_payment_succeeded__mutmut_39': x_handle_payment_succeeded__mutmut_39, 
    'x_handle_payment_succeeded__mutmut_40': x_handle_payment_succeeded__mutmut_40
}

def handle_payment_succeeded(*args, **kwargs):
    result = _mutmut_trampoline(x_handle_payment_succeeded__mutmut_orig, x_handle_payment_succeeded__mutmut_mutants, args, kwargs)
    return result 

handle_payment_succeeded.__signature__ = _mutmut_signature(x_handle_payment_succeeded__mutmut_orig)
x_handle_payment_succeeded__mutmut_orig.__name__ = 'x_handle_payment_succeeded'


async def x_handle_payment_failed__mutmut_orig(payment_intent: dict, logger: structlog.BoundLogger):
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


async def x_handle_payment_failed__mutmut_1(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle failed payment
    Update payment status with error message
    """
    payment_intent_id = None
    error_message = payment_intent.get("last_payment_error", {}).get("message", "Payment failed")

    logger.info("payment_failed", payment_intent_id=payment_intent_id, error=error_message)

    await update_payment_status(
        payment_intent_id=payment_intent_id,
        status=PaymentStatus.FAILED,
        error_message=error_message,
    )


async def x_handle_payment_failed__mutmut_2(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle failed payment
    Update payment status with error message
    """
    payment_intent_id = payment_intent["XXidXX"]
    error_message = payment_intent.get("last_payment_error", {}).get("message", "Payment failed")

    logger.info("payment_failed", payment_intent_id=payment_intent_id, error=error_message)

    await update_payment_status(
        payment_intent_id=payment_intent_id,
        status=PaymentStatus.FAILED,
        error_message=error_message,
    )


async def x_handle_payment_failed__mutmut_3(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle failed payment
    Update payment status with error message
    """
    payment_intent_id = payment_intent["ID"]
    error_message = payment_intent.get("last_payment_error", {}).get("message", "Payment failed")

    logger.info("payment_failed", payment_intent_id=payment_intent_id, error=error_message)

    await update_payment_status(
        payment_intent_id=payment_intent_id,
        status=PaymentStatus.FAILED,
        error_message=error_message,
    )


async def x_handle_payment_failed__mutmut_4(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle failed payment
    Update payment status with error message
    """
    payment_intent_id = payment_intent["id"]
    error_message = None

    logger.info("payment_failed", payment_intent_id=payment_intent_id, error=error_message)

    await update_payment_status(
        payment_intent_id=payment_intent_id,
        status=PaymentStatus.FAILED,
        error_message=error_message,
    )


async def x_handle_payment_failed__mutmut_5(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle failed payment
    Update payment status with error message
    """
    payment_intent_id = payment_intent["id"]
    error_message = payment_intent.get("last_payment_error", {}).get(None, "Payment failed")

    logger.info("payment_failed", payment_intent_id=payment_intent_id, error=error_message)

    await update_payment_status(
        payment_intent_id=payment_intent_id,
        status=PaymentStatus.FAILED,
        error_message=error_message,
    )


async def x_handle_payment_failed__mutmut_6(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle failed payment
    Update payment status with error message
    """
    payment_intent_id = payment_intent["id"]
    error_message = payment_intent.get("last_payment_error", {}).get("message", None)

    logger.info("payment_failed", payment_intent_id=payment_intent_id, error=error_message)

    await update_payment_status(
        payment_intent_id=payment_intent_id,
        status=PaymentStatus.FAILED,
        error_message=error_message,
    )


async def x_handle_payment_failed__mutmut_7(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle failed payment
    Update payment status with error message
    """
    payment_intent_id = payment_intent["id"]
    error_message = payment_intent.get("last_payment_error", {}).get("Payment failed")

    logger.info("payment_failed", payment_intent_id=payment_intent_id, error=error_message)

    await update_payment_status(
        payment_intent_id=payment_intent_id,
        status=PaymentStatus.FAILED,
        error_message=error_message,
    )


async def x_handle_payment_failed__mutmut_8(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle failed payment
    Update payment status with error message
    """
    payment_intent_id = payment_intent["id"]
    error_message = payment_intent.get("last_payment_error", {}).get("message", )

    logger.info("payment_failed", payment_intent_id=payment_intent_id, error=error_message)

    await update_payment_status(
        payment_intent_id=payment_intent_id,
        status=PaymentStatus.FAILED,
        error_message=error_message,
    )


async def x_handle_payment_failed__mutmut_9(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle failed payment
    Update payment status with error message
    """
    payment_intent_id = payment_intent["id"]
    error_message = payment_intent.get(None, {}).get("message", "Payment failed")

    logger.info("payment_failed", payment_intent_id=payment_intent_id, error=error_message)

    await update_payment_status(
        payment_intent_id=payment_intent_id,
        status=PaymentStatus.FAILED,
        error_message=error_message,
    )


async def x_handle_payment_failed__mutmut_10(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle failed payment
    Update payment status with error message
    """
    payment_intent_id = payment_intent["id"]
    error_message = payment_intent.get("last_payment_error", None).get("message", "Payment failed")

    logger.info("payment_failed", payment_intent_id=payment_intent_id, error=error_message)

    await update_payment_status(
        payment_intent_id=payment_intent_id,
        status=PaymentStatus.FAILED,
        error_message=error_message,
    )


async def x_handle_payment_failed__mutmut_11(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle failed payment
    Update payment status with error message
    """
    payment_intent_id = payment_intent["id"]
    error_message = payment_intent.get({}).get("message", "Payment failed")

    logger.info("payment_failed", payment_intent_id=payment_intent_id, error=error_message)

    await update_payment_status(
        payment_intent_id=payment_intent_id,
        status=PaymentStatus.FAILED,
        error_message=error_message,
    )


async def x_handle_payment_failed__mutmut_12(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle failed payment
    Update payment status with error message
    """
    payment_intent_id = payment_intent["id"]
    error_message = payment_intent.get("last_payment_error", ).get("message", "Payment failed")

    logger.info("payment_failed", payment_intent_id=payment_intent_id, error=error_message)

    await update_payment_status(
        payment_intent_id=payment_intent_id,
        status=PaymentStatus.FAILED,
        error_message=error_message,
    )


async def x_handle_payment_failed__mutmut_13(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle failed payment
    Update payment status with error message
    """
    payment_intent_id = payment_intent["id"]
    error_message = payment_intent.get("XXlast_payment_errorXX", {}).get("message", "Payment failed")

    logger.info("payment_failed", payment_intent_id=payment_intent_id, error=error_message)

    await update_payment_status(
        payment_intent_id=payment_intent_id,
        status=PaymentStatus.FAILED,
        error_message=error_message,
    )


async def x_handle_payment_failed__mutmut_14(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle failed payment
    Update payment status with error message
    """
    payment_intent_id = payment_intent["id"]
    error_message = payment_intent.get("LAST_PAYMENT_ERROR", {}).get("message", "Payment failed")

    logger.info("payment_failed", payment_intent_id=payment_intent_id, error=error_message)

    await update_payment_status(
        payment_intent_id=payment_intent_id,
        status=PaymentStatus.FAILED,
        error_message=error_message,
    )


async def x_handle_payment_failed__mutmut_15(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle failed payment
    Update payment status with error message
    """
    payment_intent_id = payment_intent["id"]
    error_message = payment_intent.get("last_payment_error", {}).get("XXmessageXX", "Payment failed")

    logger.info("payment_failed", payment_intent_id=payment_intent_id, error=error_message)

    await update_payment_status(
        payment_intent_id=payment_intent_id,
        status=PaymentStatus.FAILED,
        error_message=error_message,
    )


async def x_handle_payment_failed__mutmut_16(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle failed payment
    Update payment status with error message
    """
    payment_intent_id = payment_intent["id"]
    error_message = payment_intent.get("last_payment_error", {}).get("MESSAGE", "Payment failed")

    logger.info("payment_failed", payment_intent_id=payment_intent_id, error=error_message)

    await update_payment_status(
        payment_intent_id=payment_intent_id,
        status=PaymentStatus.FAILED,
        error_message=error_message,
    )


async def x_handle_payment_failed__mutmut_17(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle failed payment
    Update payment status with error message
    """
    payment_intent_id = payment_intent["id"]
    error_message = payment_intent.get("last_payment_error", {}).get("message", "XXPayment failedXX")

    logger.info("payment_failed", payment_intent_id=payment_intent_id, error=error_message)

    await update_payment_status(
        payment_intent_id=payment_intent_id,
        status=PaymentStatus.FAILED,
        error_message=error_message,
    )


async def x_handle_payment_failed__mutmut_18(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle failed payment
    Update payment status with error message
    """
    payment_intent_id = payment_intent["id"]
    error_message = payment_intent.get("last_payment_error", {}).get("message", "payment failed")

    logger.info("payment_failed", payment_intent_id=payment_intent_id, error=error_message)

    await update_payment_status(
        payment_intent_id=payment_intent_id,
        status=PaymentStatus.FAILED,
        error_message=error_message,
    )


async def x_handle_payment_failed__mutmut_19(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle failed payment
    Update payment status with error message
    """
    payment_intent_id = payment_intent["id"]
    error_message = payment_intent.get("last_payment_error", {}).get("message", "PAYMENT FAILED")

    logger.info("payment_failed", payment_intent_id=payment_intent_id, error=error_message)

    await update_payment_status(
        payment_intent_id=payment_intent_id,
        status=PaymentStatus.FAILED,
        error_message=error_message,
    )


async def x_handle_payment_failed__mutmut_20(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle failed payment
    Update payment status with error message
    """
    payment_intent_id = payment_intent["id"]
    error_message = payment_intent.get("last_payment_error", {}).get("message", "Payment failed")

    logger.info(None, payment_intent_id=payment_intent_id, error=error_message)

    await update_payment_status(
        payment_intent_id=payment_intent_id,
        status=PaymentStatus.FAILED,
        error_message=error_message,
    )


async def x_handle_payment_failed__mutmut_21(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle failed payment
    Update payment status with error message
    """
    payment_intent_id = payment_intent["id"]
    error_message = payment_intent.get("last_payment_error", {}).get("message", "Payment failed")

    logger.info("payment_failed", payment_intent_id=None, error=error_message)

    await update_payment_status(
        payment_intent_id=payment_intent_id,
        status=PaymentStatus.FAILED,
        error_message=error_message,
    )


async def x_handle_payment_failed__mutmut_22(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle failed payment
    Update payment status with error message
    """
    payment_intent_id = payment_intent["id"]
    error_message = payment_intent.get("last_payment_error", {}).get("message", "Payment failed")

    logger.info("payment_failed", payment_intent_id=payment_intent_id, error=None)

    await update_payment_status(
        payment_intent_id=payment_intent_id,
        status=PaymentStatus.FAILED,
        error_message=error_message,
    )


async def x_handle_payment_failed__mutmut_23(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle failed payment
    Update payment status with error message
    """
    payment_intent_id = payment_intent["id"]
    error_message = payment_intent.get("last_payment_error", {}).get("message", "Payment failed")

    logger.info(payment_intent_id=payment_intent_id, error=error_message)

    await update_payment_status(
        payment_intent_id=payment_intent_id,
        status=PaymentStatus.FAILED,
        error_message=error_message,
    )


async def x_handle_payment_failed__mutmut_24(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle failed payment
    Update payment status with error message
    """
    payment_intent_id = payment_intent["id"]
    error_message = payment_intent.get("last_payment_error", {}).get("message", "Payment failed")

    logger.info("payment_failed", error=error_message)

    await update_payment_status(
        payment_intent_id=payment_intent_id,
        status=PaymentStatus.FAILED,
        error_message=error_message,
    )


async def x_handle_payment_failed__mutmut_25(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle failed payment
    Update payment status with error message
    """
    payment_intent_id = payment_intent["id"]
    error_message = payment_intent.get("last_payment_error", {}).get("message", "Payment failed")

    logger.info("payment_failed", payment_intent_id=payment_intent_id, )

    await update_payment_status(
        payment_intent_id=payment_intent_id,
        status=PaymentStatus.FAILED,
        error_message=error_message,
    )


async def x_handle_payment_failed__mutmut_26(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle failed payment
    Update payment status with error message
    """
    payment_intent_id = payment_intent["id"]
    error_message = payment_intent.get("last_payment_error", {}).get("message", "Payment failed")

    logger.info("XXpayment_failedXX", payment_intent_id=payment_intent_id, error=error_message)

    await update_payment_status(
        payment_intent_id=payment_intent_id,
        status=PaymentStatus.FAILED,
        error_message=error_message,
    )


async def x_handle_payment_failed__mutmut_27(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle failed payment
    Update payment status with error message
    """
    payment_intent_id = payment_intent["id"]
    error_message = payment_intent.get("last_payment_error", {}).get("message", "Payment failed")

    logger.info("PAYMENT_FAILED", payment_intent_id=payment_intent_id, error=error_message)

    await update_payment_status(
        payment_intent_id=payment_intent_id,
        status=PaymentStatus.FAILED,
        error_message=error_message,
    )


async def x_handle_payment_failed__mutmut_28(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle failed payment
    Update payment status with error message
    """
    payment_intent_id = payment_intent["id"]
    error_message = payment_intent.get("last_payment_error", {}).get("message", "Payment failed")

    logger.info("payment_failed", payment_intent_id=payment_intent_id, error=error_message)

    await update_payment_status(
        payment_intent_id=None,
        status=PaymentStatus.FAILED,
        error_message=error_message,
    )


async def x_handle_payment_failed__mutmut_29(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle failed payment
    Update payment status with error message
    """
    payment_intent_id = payment_intent["id"]
    error_message = payment_intent.get("last_payment_error", {}).get("message", "Payment failed")

    logger.info("payment_failed", payment_intent_id=payment_intent_id, error=error_message)

    await update_payment_status(
        payment_intent_id=payment_intent_id,
        status=None,
        error_message=error_message,
    )


async def x_handle_payment_failed__mutmut_30(payment_intent: dict, logger: structlog.BoundLogger):
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
        error_message=None,
    )


async def x_handle_payment_failed__mutmut_31(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle failed payment
    Update payment status with error message
    """
    payment_intent_id = payment_intent["id"]
    error_message = payment_intent.get("last_payment_error", {}).get("message", "Payment failed")

    logger.info("payment_failed", payment_intent_id=payment_intent_id, error=error_message)

    await update_payment_status(
        status=PaymentStatus.FAILED,
        error_message=error_message,
    )


async def x_handle_payment_failed__mutmut_32(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle failed payment
    Update payment status with error message
    """
    payment_intent_id = payment_intent["id"]
    error_message = payment_intent.get("last_payment_error", {}).get("message", "Payment failed")

    logger.info("payment_failed", payment_intent_id=payment_intent_id, error=error_message)

    await update_payment_status(
        payment_intent_id=payment_intent_id,
        error_message=error_message,
    )


async def x_handle_payment_failed__mutmut_33(payment_intent: dict, logger: structlog.BoundLogger):
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
        )

x_handle_payment_failed__mutmut_mutants : ClassVar[MutantDict] = {
'x_handle_payment_failed__mutmut_1': x_handle_payment_failed__mutmut_1, 
    'x_handle_payment_failed__mutmut_2': x_handle_payment_failed__mutmut_2, 
    'x_handle_payment_failed__mutmut_3': x_handle_payment_failed__mutmut_3, 
    'x_handle_payment_failed__mutmut_4': x_handle_payment_failed__mutmut_4, 
    'x_handle_payment_failed__mutmut_5': x_handle_payment_failed__mutmut_5, 
    'x_handle_payment_failed__mutmut_6': x_handle_payment_failed__mutmut_6, 
    'x_handle_payment_failed__mutmut_7': x_handle_payment_failed__mutmut_7, 
    'x_handle_payment_failed__mutmut_8': x_handle_payment_failed__mutmut_8, 
    'x_handle_payment_failed__mutmut_9': x_handle_payment_failed__mutmut_9, 
    'x_handle_payment_failed__mutmut_10': x_handle_payment_failed__mutmut_10, 
    'x_handle_payment_failed__mutmut_11': x_handle_payment_failed__mutmut_11, 
    'x_handle_payment_failed__mutmut_12': x_handle_payment_failed__mutmut_12, 
    'x_handle_payment_failed__mutmut_13': x_handle_payment_failed__mutmut_13, 
    'x_handle_payment_failed__mutmut_14': x_handle_payment_failed__mutmut_14, 
    'x_handle_payment_failed__mutmut_15': x_handle_payment_failed__mutmut_15, 
    'x_handle_payment_failed__mutmut_16': x_handle_payment_failed__mutmut_16, 
    'x_handle_payment_failed__mutmut_17': x_handle_payment_failed__mutmut_17, 
    'x_handle_payment_failed__mutmut_18': x_handle_payment_failed__mutmut_18, 
    'x_handle_payment_failed__mutmut_19': x_handle_payment_failed__mutmut_19, 
    'x_handle_payment_failed__mutmut_20': x_handle_payment_failed__mutmut_20, 
    'x_handle_payment_failed__mutmut_21': x_handle_payment_failed__mutmut_21, 
    'x_handle_payment_failed__mutmut_22': x_handle_payment_failed__mutmut_22, 
    'x_handle_payment_failed__mutmut_23': x_handle_payment_failed__mutmut_23, 
    'x_handle_payment_failed__mutmut_24': x_handle_payment_failed__mutmut_24, 
    'x_handle_payment_failed__mutmut_25': x_handle_payment_failed__mutmut_25, 
    'x_handle_payment_failed__mutmut_26': x_handle_payment_failed__mutmut_26, 
    'x_handle_payment_failed__mutmut_27': x_handle_payment_failed__mutmut_27, 
    'x_handle_payment_failed__mutmut_28': x_handle_payment_failed__mutmut_28, 
    'x_handle_payment_failed__mutmut_29': x_handle_payment_failed__mutmut_29, 
    'x_handle_payment_failed__mutmut_30': x_handle_payment_failed__mutmut_30, 
    'x_handle_payment_failed__mutmut_31': x_handle_payment_failed__mutmut_31, 
    'x_handle_payment_failed__mutmut_32': x_handle_payment_failed__mutmut_32, 
    'x_handle_payment_failed__mutmut_33': x_handle_payment_failed__mutmut_33
}

def handle_payment_failed(*args, **kwargs):
    result = _mutmut_trampoline(x_handle_payment_failed__mutmut_orig, x_handle_payment_failed__mutmut_mutants, args, kwargs)
    return result 

handle_payment_failed.__signature__ = _mutmut_signature(x_handle_payment_failed__mutmut_orig)
x_handle_payment_failed__mutmut_orig.__name__ = 'x_handle_payment_failed'


async def x_handle_charge_refunded__mutmut_orig(payment_intent: dict, logger: structlog.BoundLogger):
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


async def x_handle_charge_refunded__mutmut_1(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle refunded payment
    Update payment status
    """
    payment_intent_id = None

    if not payment_intent_id:
        logger.warning("charge_refunded_missing_payment_intent")
        return

    logger.info("charge_refunded", payment_intent_id=payment_intent_id)

    await update_payment_status(
        payment_intent_id=payment_intent_id,
        status=PaymentStatus.REFUNDED,
    )


async def x_handle_charge_refunded__mutmut_2(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle refunded payment
    Update payment status
    """
    payment_intent_id = payment_intent.get(None)

    if not payment_intent_id:
        logger.warning("charge_refunded_missing_payment_intent")
        return

    logger.info("charge_refunded", payment_intent_id=payment_intent_id)

    await update_payment_status(
        payment_intent_id=payment_intent_id,
        status=PaymentStatus.REFUNDED,
    )


async def x_handle_charge_refunded__mutmut_3(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle refunded payment
    Update payment status
    """
    payment_intent_id = payment_intent.get("XXpayment_intentXX")

    if not payment_intent_id:
        logger.warning("charge_refunded_missing_payment_intent")
        return

    logger.info("charge_refunded", payment_intent_id=payment_intent_id)

    await update_payment_status(
        payment_intent_id=payment_intent_id,
        status=PaymentStatus.REFUNDED,
    )


async def x_handle_charge_refunded__mutmut_4(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle refunded payment
    Update payment status
    """
    payment_intent_id = payment_intent.get("PAYMENT_INTENT")

    if not payment_intent_id:
        logger.warning("charge_refunded_missing_payment_intent")
        return

    logger.info("charge_refunded", payment_intent_id=payment_intent_id)

    await update_payment_status(
        payment_intent_id=payment_intent_id,
        status=PaymentStatus.REFUNDED,
    )


async def x_handle_charge_refunded__mutmut_5(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle refunded payment
    Update payment status
    """
    payment_intent_id = payment_intent.get("payment_intent")

    if payment_intent_id:
        logger.warning("charge_refunded_missing_payment_intent")
        return

    logger.info("charge_refunded", payment_intent_id=payment_intent_id)

    await update_payment_status(
        payment_intent_id=payment_intent_id,
        status=PaymentStatus.REFUNDED,
    )


async def x_handle_charge_refunded__mutmut_6(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle refunded payment
    Update payment status
    """
    payment_intent_id = payment_intent.get("payment_intent")

    if not payment_intent_id:
        logger.warning(None)
        return

    logger.info("charge_refunded", payment_intent_id=payment_intent_id)

    await update_payment_status(
        payment_intent_id=payment_intent_id,
        status=PaymentStatus.REFUNDED,
    )


async def x_handle_charge_refunded__mutmut_7(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle refunded payment
    Update payment status
    """
    payment_intent_id = payment_intent.get("payment_intent")

    if not payment_intent_id:
        logger.warning("XXcharge_refunded_missing_payment_intentXX")
        return

    logger.info("charge_refunded", payment_intent_id=payment_intent_id)

    await update_payment_status(
        payment_intent_id=payment_intent_id,
        status=PaymentStatus.REFUNDED,
    )


async def x_handle_charge_refunded__mutmut_8(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle refunded payment
    Update payment status
    """
    payment_intent_id = payment_intent.get("payment_intent")

    if not payment_intent_id:
        logger.warning("CHARGE_REFUNDED_MISSING_PAYMENT_INTENT")
        return

    logger.info("charge_refunded", payment_intent_id=payment_intent_id)

    await update_payment_status(
        payment_intent_id=payment_intent_id,
        status=PaymentStatus.REFUNDED,
    )


async def x_handle_charge_refunded__mutmut_9(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle refunded payment
    Update payment status
    """
    payment_intent_id = payment_intent.get("payment_intent")

    if not payment_intent_id:
        logger.warning("charge_refunded_missing_payment_intent")
        return

    logger.info(None, payment_intent_id=payment_intent_id)

    await update_payment_status(
        payment_intent_id=payment_intent_id,
        status=PaymentStatus.REFUNDED,
    )


async def x_handle_charge_refunded__mutmut_10(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle refunded payment
    Update payment status
    """
    payment_intent_id = payment_intent.get("payment_intent")

    if not payment_intent_id:
        logger.warning("charge_refunded_missing_payment_intent")
        return

    logger.info("charge_refunded", payment_intent_id=None)

    await update_payment_status(
        payment_intent_id=payment_intent_id,
        status=PaymentStatus.REFUNDED,
    )


async def x_handle_charge_refunded__mutmut_11(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle refunded payment
    Update payment status
    """
    payment_intent_id = payment_intent.get("payment_intent")

    if not payment_intent_id:
        logger.warning("charge_refunded_missing_payment_intent")
        return

    logger.info(payment_intent_id=payment_intent_id)

    await update_payment_status(
        payment_intent_id=payment_intent_id,
        status=PaymentStatus.REFUNDED,
    )


async def x_handle_charge_refunded__mutmut_12(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle refunded payment
    Update payment status
    """
    payment_intent_id = payment_intent.get("payment_intent")

    if not payment_intent_id:
        logger.warning("charge_refunded_missing_payment_intent")
        return

    logger.info("charge_refunded", )

    await update_payment_status(
        payment_intent_id=payment_intent_id,
        status=PaymentStatus.REFUNDED,
    )


async def x_handle_charge_refunded__mutmut_13(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle refunded payment
    Update payment status
    """
    payment_intent_id = payment_intent.get("payment_intent")

    if not payment_intent_id:
        logger.warning("charge_refunded_missing_payment_intent")
        return

    logger.info("XXcharge_refundedXX", payment_intent_id=payment_intent_id)

    await update_payment_status(
        payment_intent_id=payment_intent_id,
        status=PaymentStatus.REFUNDED,
    )


async def x_handle_charge_refunded__mutmut_14(payment_intent: dict, logger: structlog.BoundLogger):
    """
    Handle refunded payment
    Update payment status
    """
    payment_intent_id = payment_intent.get("payment_intent")

    if not payment_intent_id:
        logger.warning("charge_refunded_missing_payment_intent")
        return

    logger.info("CHARGE_REFUNDED", payment_intent_id=payment_intent_id)

    await update_payment_status(
        payment_intent_id=payment_intent_id,
        status=PaymentStatus.REFUNDED,
    )


async def x_handle_charge_refunded__mutmut_15(payment_intent: dict, logger: structlog.BoundLogger):
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
        payment_intent_id=None,
        status=PaymentStatus.REFUNDED,
    )


async def x_handle_charge_refunded__mutmut_16(payment_intent: dict, logger: structlog.BoundLogger):
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
        status=None,
    )


async def x_handle_charge_refunded__mutmut_17(payment_intent: dict, logger: structlog.BoundLogger):
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
        status=PaymentStatus.REFUNDED,
    )


async def x_handle_charge_refunded__mutmut_18(payment_intent: dict, logger: structlog.BoundLogger):
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
        )

x_handle_charge_refunded__mutmut_mutants : ClassVar[MutantDict] = {
'x_handle_charge_refunded__mutmut_1': x_handle_charge_refunded__mutmut_1, 
    'x_handle_charge_refunded__mutmut_2': x_handle_charge_refunded__mutmut_2, 
    'x_handle_charge_refunded__mutmut_3': x_handle_charge_refunded__mutmut_3, 
    'x_handle_charge_refunded__mutmut_4': x_handle_charge_refunded__mutmut_4, 
    'x_handle_charge_refunded__mutmut_5': x_handle_charge_refunded__mutmut_5, 
    'x_handle_charge_refunded__mutmut_6': x_handle_charge_refunded__mutmut_6, 
    'x_handle_charge_refunded__mutmut_7': x_handle_charge_refunded__mutmut_7, 
    'x_handle_charge_refunded__mutmut_8': x_handle_charge_refunded__mutmut_8, 
    'x_handle_charge_refunded__mutmut_9': x_handle_charge_refunded__mutmut_9, 
    'x_handle_charge_refunded__mutmut_10': x_handle_charge_refunded__mutmut_10, 
    'x_handle_charge_refunded__mutmut_11': x_handle_charge_refunded__mutmut_11, 
    'x_handle_charge_refunded__mutmut_12': x_handle_charge_refunded__mutmut_12, 
    'x_handle_charge_refunded__mutmut_13': x_handle_charge_refunded__mutmut_13, 
    'x_handle_charge_refunded__mutmut_14': x_handle_charge_refunded__mutmut_14, 
    'x_handle_charge_refunded__mutmut_15': x_handle_charge_refunded__mutmut_15, 
    'x_handle_charge_refunded__mutmut_16': x_handle_charge_refunded__mutmut_16, 
    'x_handle_charge_refunded__mutmut_17': x_handle_charge_refunded__mutmut_17, 
    'x_handle_charge_refunded__mutmut_18': x_handle_charge_refunded__mutmut_18
}

def handle_charge_refunded(*args, **kwargs):
    result = _mutmut_trampoline(x_handle_charge_refunded__mutmut_orig, x_handle_charge_refunded__mutmut_mutants, args, kwargs)
    return result 

handle_charge_refunded.__signature__ = _mutmut_signature(x_handle_charge_refunded__mutmut_orig)
x_handle_charge_refunded__mutmut_orig.__name__ = 'x_handle_charge_refunded'
