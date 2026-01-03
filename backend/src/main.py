"""
FastAPI application entry point

Integrates all modules: configuration, feature flags, database, and logging.
"""

import uuid
import structlog
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from config.loader import ConfigLoader
from feature_flags.evaluator import FeatureFlagEvaluator
from feature_flags.types import Feature
from database.adapters.factory import get_database_adapter
from logging_lib.logger import configure_logging
from logging_lib.correlation import CorrelationContext
from src.config import settings
from src.middleware.rate_limiter import RateLimitMiddleware
from src.api.routes import reports, webhooks, stream, health, cron


# Load environment variables from .env file
load_dotenv()

# Initialize logging first (before any other modules)
logger = configure_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager
    Handles startup and shutdown events with full module integration
    """
    # Startup
    logger.info("application_starting")

    try:
        # 1. Load and validate configuration
        logger.info("loading_configuration")
        config = ConfigLoader.load()
        app.state.config = config
        logger.info(
            "configuration_loaded",
            environment=config.ENVIRONMENT_MODE,
            app_version=config.APP_VERSION,
        )

        # 2. Initialize feature flags
        logger.info("initializing_feature_flags")
        feature_flags = FeatureFlagEvaluator()
        app.state.feature_flags = feature_flags

        # Log active feature flags
        active_flags = feature_flags.get_all_flags()
        logger.info(
            "feature_flags_initialized",
            flags=active_flags,
            supabase=active_flags.get(Feature.SUPABASE.value),
            payments=active_flags.get(Feature.PAYMENTS.value),
            rate_limiting=active_flags.get(Feature.RATE_LIMITING.value),
            observability=active_flags.get(Feature.OBSERVABILITY.value),
        )

        # 3. Initialize database adapter
        logger.info("initializing_database")
        try:
            db_adapter = get_database_adapter()
            app.state.db = db_adapter
            logger.info(
                "database_initialized",
                adapter_type=type(db_adapter).__name__,
                supabase_enabled=feature_flags.is_enabled(Feature.SUPABASE),
            )
        except Exception as e:
            logger.error("database_initialization_failed", error=str(e), exc_info=True)
            raise

        # 4. Validate required configurations
        if config.ENVIRONMENT_MODE == "production":
            logger.info("validating_production_requirements")
            if not (
                feature_flags.is_enabled(Feature.SUPABASE)
                and feature_flags.is_enabled(Feature.PAYMENTS)
            ):
                raise ValueError(
                    "Production mode requires ENABLE_SUPABASE=true and ENABLE_PAYMENTS=true"
                )

        logger.info(
            "application_started",
            environment=config.ENVIRONMENT_MODE,
            version=config.APP_VERSION,
            port=config.PORT,
        )

        yield

    except Exception as e:
        logger.error("application_startup_failed", error=str(e), exc_info=True)
        raise

    # Shutdown
    logger.info("application_shutting_down")

    # Close database connections if needed
    if hasattr(app.state, "db"):
        try:
            # Database adapters manage their own connection pools
            # No explicit cleanup needed currently
            logger.info("database_connections_closed")
        except Exception as e:
            logger.error("database_cleanup_failed", error=str(e), exc_info=True)

    logger.info("application_shutdown_complete")


# Create FastAPI app (after loading config in lifespan)
# We'll use defaults here and update from config in lifespan
app = FastAPI(
    title="UK Study & Migration Research API",
    description="AI-powered research reports for students (£2.99 per query)",
    version="0.1.0",  # Will be updated from config
    docs_url="/docs",  # Will be conditional based on environment
    redoc_url="/redoc",  # Will be conditional based on environment
    lifespan=lifespan,
)


# CORS middleware (will be configured dynamically after config loads)
# For now, we'll add a startup event to configure CORS
@app.on_event("startup")
async def configure_cors():
    """Configure CORS after config is loaded"""
    # CORS is already added via middleware below, this is just for reference
    pass


# Add CORS middleware with origins from configuration
# In production, ALLOWED_ORIGINS should only include the frontend domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS
    if hasattr(settings, "ALLOWED_ORIGINS")
    else ["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Add rate limiting middleware (if enabled via feature flag)
if settings.ENABLE_RATE_LIMITING:
    app.add_middleware(
        RateLimitMiddleware, requests_per_minute=settings.RATE_LIMIT_MAX
    )


@app.middleware("http")
async def correlation_id_middleware(request: Request, call_next):
    """
    Correlation ID middleware

    Extracts or generates correlation ID for request tracing.
    Propagates correlation ID through logs and response headers.
    """
    # Extract correlation ID from header or generate new one
    correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))

    # Set correlation ID in context for logging
    with CorrelationContext(correlation_id):
        try:
            response = await call_next(request)
            response.headers["X-Correlation-ID"] = correlation_id
            return response
        except Exception as e:
            logger.error(
                "request_failed_in_correlation_middleware",
                error=str(e),
                exc_info=True,
            )
            response = JSONResponse(
                status_code=500,
                content={
                    "error": "Internal server error",
                    "correlation_id": correlation_id,
                },
            )
            response.headers["X-Correlation-ID"] = correlation_id
            return response


@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    """
    Request/Response logging middleware

    Logs all incoming requests and outgoing responses with sanitization.
    Adds request metadata to structured logging context.
    """
    import time
    from logging_lib.sanitizer import sanitize_log_data

    # Bind request context to logger
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(
        method=request.method,
        path=request.url.path,
        client_host=request.client.host if request.client else None,
    )

    # Extract user_id from Authorization header if present
    auth_header = request.headers.get("authorization")
    if auth_header:
        structlog.contextvars.bind_contextvars(has_auth=True)

    # Log request start
    start_time = time.time()
    logger.info(
        "request_started",
        query_params=sanitize_log_data(dict(request.query_params)),
    )

    try:
        # Process request
        response = await call_next(request)

        # Calculate request duration
        duration_ms = (time.time() - start_time) * 1000

        # Bind response context
        structlog.contextvars.bind_contextvars(
            status_code=response.status_code,
            duration_ms=round(duration_ms, 2),
        )

        # Log request completion
        logger.info("request_completed")

        # Add request ID to response (if not already set by correlation middleware)
        if "X-Request-ID" not in response.headers:
            response.headers["X-Request-ID"] = str(uuid.uuid4())

        return response

    except Exception as e:
        duration_ms = (time.time() - start_time) * 1000

        logger.error(
            "request_failed",
            error=str(e),
            duration_ms=round(duration_ms, 2),
            exc_info=True,
        )

        return JSONResponse(
            status_code=500,
            content={
                "error": "Internal server error",
                "message": str(e) if app.state.config.ENVIRONMENT_MODE != "production" else None,
            },
        )


# Include routers
app.include_router(health.router, tags=["Health"])
app.include_router(reports.router)
app.include_router(webhooks.router)
app.include_router(stream.router)
app.include_router(cron.router)


@app.get("/")
async def root(request: Request):
    """Root endpoint with dynamic configuration"""
    config = request.app.state.config
    feature_flags = request.app.state.feature_flags

    return {
        "message": "UK Study & Migration Research API",
        "version": config.APP_VERSION,
        "environment": config.ENVIRONMENT_MODE,
        "docs": "/docs" if config.ENVIRONMENT_MODE in ["dev", "test"] else None,
        "features": {
            "supabase": feature_flags.is_enabled(Feature.SUPABASE),
            "payments": feature_flags.is_enabled(Feature.PAYMENTS),
            "rate_limiting": feature_flags.is_enabled(Feature.RATE_LIMITING),
        },
    }
