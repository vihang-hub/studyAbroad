"""
Cron API routes
Handles scheduled jobs for data retention and cleanup

Security:
- All endpoints require X-Cron-Secret header matching environment variable
- Only accessible by Cloud Scheduler or authorized cron services

T135-T141: Data retention cron endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Header, status
import structlog

from dependencies import get_db, get_request_logger, get_correlation_id
from database.types import DatabaseAdapter
from database.repositories.report import ReportRepository
from config import settings

router = APIRouter(prefix="/cron", tags=["Cron Jobs"])


def verify_cron_secret(x_cron_secret: str = Header(...)) -> None:
    """
    Verify cron secret header matches configured secret

    Args:
        x_cron_secret: Secret from X-Cron-Secret header

    Raises:
        HTTPException: 401 if secret doesn't match
    """
    if x_cron_secret != settings.CRON_SECRET:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid cron secret")


@router.post("/expire-reports")
async def expire_reports(
    db: DatabaseAdapter = Depends(get_db),
    logger: structlog.BoundLogger = Depends(get_request_logger),
    correlation_id: str = Depends(get_correlation_id),
    _: None = Depends(verify_cron_secret),
):
    """
    Expire reports past their expires_at date (soft delete)

    T135-T139: Cron endpoint to mark reports as expired

    Security:
    - Requires X-Cron-Secret header

    Returns:
        JSON with count of expired reports
    """
    logger.info("cron.expire_reports.started", correlation_id=correlation_id)

    try:
        # Get repository
        repo = ReportRepository(db)

        # Execute expiry
        expired_count = await repo.expire_old_reports()

        logger.info(
            "cron.expire_reports.success",
            correlation_id=correlation_id,
            expired_count=expired_count,
        )

        return {"success": True, "expired_count": expired_count, "correlation_id": correlation_id}

    except Exception as e:
        logger.error(
            "cron.expire_reports.error", correlation_id=correlation_id, error=str(e), exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to expire reports: {str(e)}",
        )


@router.post("/delete-expired-reports")
async def delete_expired_reports(
    db: DatabaseAdapter = Depends(get_db),
    logger: structlog.BoundLogger = Depends(get_request_logger),
    correlation_id: str = Depends(get_correlation_id),
    _: None = Depends(verify_cron_secret),
):
    """
    Delete expired reports after retention period (hard delete)

    T140-T141: Cron endpoint to permanently delete expired reports

    GDPR Compliance:
    - Reports are soft deleted (status=expired) after 30 days
    - Reports are hard deleted 90 days after expiration (120 days total)

    Security:
    - Requires X-Cron-Secret header

    Returns:
        JSON with count of deleted reports
    """
    logger.info("cron.delete_expired_reports.started", correlation_id=correlation_id)

    try:
        # Get repository
        repo = ReportRepository(db)

        # Execute deletion
        deleted_count = await repo.delete_expired_reports()

        logger.info(
            "cron.delete_expired_reports.success",
            correlation_id=correlation_id,
            deleted_count=deleted_count,
        )

        return {"success": True, "deleted_count": deleted_count, "correlation_id": correlation_id}

    except Exception as e:
        logger.error(
            "cron.delete_expired_reports.error",
            correlation_id=correlation_id,
            error=str(e),
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete expired reports: {str(e)}",
        )
