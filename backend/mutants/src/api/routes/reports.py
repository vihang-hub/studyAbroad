"""
Reports API routes
Handles report creation, generation, and retrieval

Integrates with dependency injection for database, logging, and feature flags.
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List
import structlog

from api.models.report import (
    CreateReportRequest,
    CreateReportResponse,
    Report,
    ReportListItem,
)
from api.services.auth_service import get_current_user_id
from api.services.report_service import (
    create_report,
    get_report,
    list_user_reports,
    soft_delete_report,
)
from api.services.payment_service import create_checkout_session
from dependencies import (
    get_db,
    get_request_logger,
    get_feature_flags,
    get_correlation_id,
)
from database.types import DatabaseAdapter
from feature_flags.evaluator import FeatureFlagEvaluator
from feature_flags.types import Feature

router = APIRouter(prefix="/reports", tags=["Reports"])
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


@router.post("/initiate", response_model=CreateReportResponse)
async def initiate_report(
    request_data: CreateReportRequest,
    http_request: Request,
    user_id: str = Depends(get_current_user_id),
    db: DatabaseAdapter = Depends(get_db),
    logger: structlog.BoundLogger = Depends(get_request_logger),
    feature_flags: FeatureFlagEvaluator = Depends(get_feature_flags),
    correlation_id: str = Depends(get_correlation_id),
):
    """
    Initiate report generation with payment
    Creates report record and Stripe checkout session

    Flow:
    1. Check feature flags (payments enabled/disabled)
    2. Create report with status=pending
    3. Create Stripe payment intent (if payments enabled)
    4. Return payment details to frontend
    5. Frontend completes payment
    6. Webhook triggers report generation
    """
    logger.info(
        "report_initiation_started",
        user_id=user_id,
        query_length=len(request_data.query),
    )

    try:
        # Create report record
        report_response = await create_report(user_id, request_data.query)

        logger.info(
            "report_created",
            report_id=report_response.report_id,
            status=report_response.status,
        )

        # Check if payments are enabled
        if feature_flags.is_enabled(Feature.PAYMENTS):
            # Create Stripe checkout session
            logger.info("creating_checkout_session", report_id=report_response.report_id)

            checkout = await create_checkout_session(
                user_id=user_id,
                report_id=report_response.report_id,
                query=request_data.query,
            )

            logger.info(
                "checkout_session_created",
                report_id=report_response.report_id,
                session_id=checkout.session_id if hasattr(checkout, "session_id") else None,
            )

            # Return combined response
            return CreateReportResponse(
                report_id=report_response.report_id,
                status=report_response.status,
                estimated_completion_seconds=report_response.estimated_completion_seconds,
                # Add payment details for frontend
                **checkout.dict(),
            )
        else:
            # Dev mode: Skip payment, return report directly
            logger.info(
                "payments_disabled_skipping_checkout",
                report_id=report_response.report_id,
            )

            return report_response

    except ValueError as e:
        logger.warning("report_initiation_validation_error", error=str(e), user_id=user_id)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(
            "report_initiation_failed",
            error=str(e),
            user_id=user_id,
            exc_info=True,
        )
        raise HTTPException(status_code=500, detail=f"Failed to initiate report: {str(e)}")


@router.get("/{report_id}", response_model=Report)
async def get_report_by_id(
    report_id: str,
    user_id: str = Depends(get_current_user_id),
    db: DatabaseAdapter = Depends(get_db),
    logger: structlog.BoundLogger = Depends(get_request_logger),
):
    """
    Get report by ID
    Only returns reports owned by the authenticated user
    """
    logger.info("fetching_report", report_id=report_id, user_id=user_id)

    report = await get_report(report_id, user_id)

    if not report:
        logger.warning("report_not_found", report_id=report_id, user_id=user_id)
        raise HTTPException(status_code=404, detail="Report not found")

    logger.info("report_fetched", report_id=report_id, status=report.status)
    return report


@router.get("/", response_model=List[ReportListItem])
async def list_reports(
    limit: int = 50,
    user_id: str = Depends(get_current_user_id),
    db: DatabaseAdapter = Depends(get_db),
    logger: structlog.BoundLogger = Depends(get_request_logger),
):
    """
    List all reports for authenticated user
    """
    logger.info("listing_reports", user_id=user_id, limit=limit)

    reports = await list_user_reports(user_id, limit)

    logger.info("reports_listed", user_id=user_id, count=len(reports))
    return reports


@router.delete("/{report_id}")
async def delete_report(
    report_id: str,
    user_id: str = Depends(get_current_user_id),
    db: DatabaseAdapter = Depends(get_db),
    logger: structlog.BoundLogger = Depends(get_request_logger),
):
    """
    Soft delete a report
    Sets deleted_at timestamp (30-day retention policy)
    """
    logger.info("deleting_report", report_id=report_id, user_id=user_id)

    success = await soft_delete_report(report_id, user_id)

    if not success:
        logger.warning("report_delete_failed_not_found", report_id=report_id, user_id=user_id)
        raise HTTPException(status_code=404, detail="Report not found")

    logger.info("report_deleted", report_id=report_id, user_id=user_id)
    return {"message": "Report deleted successfully"}
