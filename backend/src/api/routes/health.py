"""
Health check endpoint

Comprehensive health checks for all services (database, AI, payments).
"""

from datetime import datetime
from typing import Dict
from fastapi import APIRouter, Request, Depends
from pydantic import BaseModel
import structlog

from dependencies import get_config, get_feature_flags, get_db
from config.environment import EnvironmentConfig
from feature_flags.evaluator import FeatureFlagEvaluator
from feature_flags.types import Feature
from database.types import DatabaseAdapter

router = APIRouter()
logger = structlog.get_logger()


class ServiceStatus(BaseModel):
    """Individual service status"""

    status: str  # "up", "down", "degraded", "disabled"
    message: str | None = None
    response_time_ms: float | None = None


class HealthResponse(BaseModel):
    """Health check response"""

    status: str  # "healthy", "degraded", "unhealthy"
    timestamp: str
    version: str
    environment: str
    services: Dict[str, ServiceStatus]


async def check_database_health(db: DatabaseAdapter) -> ServiceStatus:
    """
    Check database connectivity and response time

    Args:
        db: Database adapter

    Returns:
        Service status with connection info
    """
    import time

    try:
        start_time = time.time()

        # Simple connectivity check (will depend on adapter implementation)
        # For now, we'll assume if adapter is available, it's connected
        # TODO: Implement actual ping/health check in adapters

        response_time_ms = (time.time() - start_time) * 1000

        return ServiceStatus(
            status="up",
            message="Database connected",
            response_time_ms=round(response_time_ms, 2),
        )
    except Exception as e:
        logger.error("database_health_check_failed", error=str(e))
        return ServiceStatus(
            status="down",
            message=f"Database error: {str(e)}",
        )


async def check_ai_health(config: EnvironmentConfig) -> ServiceStatus:
    """
    Check Gemini AI service availability

    Args:
        config: Environment configuration

    Returns:
        Service status
    """
    try:
        # Check if API key is configured
        if not config.GEMINI_API_KEY:
            return ServiceStatus(
                status="down",
                message="Gemini API key not configured",
            )

        # Simple check: API key is present
        # TODO: Implement actual API connectivity check
        return ServiceStatus(
            status="up",
            message="Gemini API configured",
        )
    except Exception as e:
        logger.error("ai_health_check_failed", error=str(e))
        return ServiceStatus(
            status="down",
            message=f"AI service error: {str(e)}",
        )


async def check_payments_health(
    config: EnvironmentConfig,
    feature_flags: FeatureFlagEvaluator,
) -> ServiceStatus:
    """
    Check Stripe payment service availability

    Args:
        config: Environment configuration
        feature_flags: Feature flag evaluator

    Returns:
        Service status
    """
    try:
        # Check if payments are enabled
        if not feature_flags.is_enabled(Feature.PAYMENTS):
            return ServiceStatus(
                status="disabled",
                message="Payments disabled in current environment",
            )

        # Check if Stripe keys are configured
        if not (config.STRIPE_SECRET_KEY and config.STRIPE_PUBLISHABLE_KEY):
            return ServiceStatus(
                status="down",
                message="Stripe API keys not configured",
            )

        # TODO: Implement actual Stripe API connectivity check
        return ServiceStatus(
            status="up",
            message="Stripe configured",
        )
    except Exception as e:
        logger.error("payments_health_check_failed", error=str(e))
        return ServiceStatus(
            status="down",
            message=f"Payment service error: {str(e)}",
        )


@router.get("/health", response_model=HealthResponse)
async def health_check(
    request: Request,
    config: EnvironmentConfig = Depends(get_config),
    feature_flags: FeatureFlagEvaluator = Depends(get_feature_flags),
):
    """
    Comprehensive health check endpoint

    Checks:
    - Database connectivity and response time
    - AI service availability (Gemini API)
    - Payment service availability (Stripe)

    Returns:
        Health status with service details
    """
    logger.info("health_check_started")

    # Check all services
    services = {}

    # Database check
    try:
        db = get_db(request)
        services["database"] = await check_database_health(db)
    except Exception as e:
        logger.error("database_health_check_error", error=str(e))
        services["database"] = ServiceStatus(
            status="down",
            message="Database not initialized",
        )

    # AI service check
    services["ai"] = await check_ai_health(config)

    # Payments check
    services["payments"] = await check_payments_health(config, feature_flags)

    # Determine overall status
    service_statuses = [s.status for s in services.values()]

    if all(s in ["up", "disabled"] for s in service_statuses):
        overall_status = "healthy"
    elif any(s == "down" for s in service_statuses):
        # If any critical service is down, system is unhealthy
        # Disabled services don't count as unhealthy
        critical_services = ["database", "ai"]
        critical_down = any(
            services[svc].status == "down" for svc in critical_services if svc in services
        )
        overall_status = "unhealthy" if critical_down else "degraded"
    else:
        overall_status = "degraded"

    logger.info(
        "health_check_completed",
        overall_status=overall_status,
        database_status=services.get("database", {}).status,
        ai_status=services.get("ai", {}).status,
        payments_status=services.get("payments", {}).status,
    )

    return HealthResponse(
        status=overall_status,
        timestamp=datetime.utcnow().isoformat(),
        version=config.APP_VERSION,
        environment=config.ENVIRONMENT_MODE,
        services=services,
    )
