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


def x_verify_cron_secret__mutmut_orig(x_cron_secret: str = Header(...)) -> None:
    """
    Verify cron secret header matches configured secret

    Args:
        x_cron_secret: Secret from X-Cron-Secret header

    Raises:
        HTTPException: 401 if secret doesn't match
    """
    if x_cron_secret != settings.CRON_SECRET:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid cron secret")


def x_verify_cron_secret__mutmut_1(x_cron_secret: str = Header(...)) -> None:
    """
    Verify cron secret header matches configured secret

    Args:
        x_cron_secret: Secret from X-Cron-Secret header

    Raises:
        HTTPException: 401 if secret doesn't match
    """
    if x_cron_secret == settings.CRON_SECRET:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid cron secret")


def x_verify_cron_secret__mutmut_2(x_cron_secret: str = Header(...)) -> None:
    """
    Verify cron secret header matches configured secret

    Args:
        x_cron_secret: Secret from X-Cron-Secret header

    Raises:
        HTTPException: 401 if secret doesn't match
    """
    if x_cron_secret != settings.CRON_SECRET:
        raise HTTPException(status_code=None, detail="Invalid cron secret")


def x_verify_cron_secret__mutmut_3(x_cron_secret: str = Header(...)) -> None:
    """
    Verify cron secret header matches configured secret

    Args:
        x_cron_secret: Secret from X-Cron-Secret header

    Raises:
        HTTPException: 401 if secret doesn't match
    """
    if x_cron_secret != settings.CRON_SECRET:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=None)


def x_verify_cron_secret__mutmut_4(x_cron_secret: str = Header(...)) -> None:
    """
    Verify cron secret header matches configured secret

    Args:
        x_cron_secret: Secret from X-Cron-Secret header

    Raises:
        HTTPException: 401 if secret doesn't match
    """
    if x_cron_secret != settings.CRON_SECRET:
        raise HTTPException(detail="Invalid cron secret")


def x_verify_cron_secret__mutmut_5(x_cron_secret: str = Header(...)) -> None:
    """
    Verify cron secret header matches configured secret

    Args:
        x_cron_secret: Secret from X-Cron-Secret header

    Raises:
        HTTPException: 401 if secret doesn't match
    """
    if x_cron_secret != settings.CRON_SECRET:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, )


def x_verify_cron_secret__mutmut_6(x_cron_secret: str = Header(...)) -> None:
    """
    Verify cron secret header matches configured secret

    Args:
        x_cron_secret: Secret from X-Cron-Secret header

    Raises:
        HTTPException: 401 if secret doesn't match
    """
    if x_cron_secret != settings.CRON_SECRET:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="XXInvalid cron secretXX")


def x_verify_cron_secret__mutmut_7(x_cron_secret: str = Header(...)) -> None:
    """
    Verify cron secret header matches configured secret

    Args:
        x_cron_secret: Secret from X-Cron-Secret header

    Raises:
        HTTPException: 401 if secret doesn't match
    """
    if x_cron_secret != settings.CRON_SECRET:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid cron secret")


def x_verify_cron_secret__mutmut_8(x_cron_secret: str = Header(...)) -> None:
    """
    Verify cron secret header matches configured secret

    Args:
        x_cron_secret: Secret from X-Cron-Secret header

    Raises:
        HTTPException: 401 if secret doesn't match
    """
    if x_cron_secret != settings.CRON_SECRET:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="INVALID CRON SECRET")

x_verify_cron_secret__mutmut_mutants : ClassVar[MutantDict] = {
'x_verify_cron_secret__mutmut_1': x_verify_cron_secret__mutmut_1, 
    'x_verify_cron_secret__mutmut_2': x_verify_cron_secret__mutmut_2, 
    'x_verify_cron_secret__mutmut_3': x_verify_cron_secret__mutmut_3, 
    'x_verify_cron_secret__mutmut_4': x_verify_cron_secret__mutmut_4, 
    'x_verify_cron_secret__mutmut_5': x_verify_cron_secret__mutmut_5, 
    'x_verify_cron_secret__mutmut_6': x_verify_cron_secret__mutmut_6, 
    'x_verify_cron_secret__mutmut_7': x_verify_cron_secret__mutmut_7, 
    'x_verify_cron_secret__mutmut_8': x_verify_cron_secret__mutmut_8
}

def verify_cron_secret(*args, **kwargs):
    result = _mutmut_trampoline(x_verify_cron_secret__mutmut_orig, x_verify_cron_secret__mutmut_mutants, args, kwargs)
    return result 

verify_cron_secret.__signature__ = _mutmut_signature(x_verify_cron_secret__mutmut_orig)
x_verify_cron_secret__mutmut_orig.__name__ = 'x_verify_cron_secret'


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
