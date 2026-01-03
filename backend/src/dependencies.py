"""
Dependency Injection Module

Provides FastAPI dependencies for configuration, database, logging, and feature flags.
Used throughout the application for consistent access to shared resources.
"""

from typing import Generator
from fastapi import Request
import structlog

from config.loader import ConfigLoader
from config.environment import EnvironmentConfig
from feature_flags.evaluator import FeatureFlagEvaluator
from database.types import DatabaseAdapter


def get_config() -> EnvironmentConfig:
    """
    Get validated environment configuration

    Returns:
        Validated configuration object

    Raises:
        ValueError: If configuration validation fails
    """
    return ConfigLoader.load()


def get_feature_flags() -> FeatureFlagEvaluator:
    """
    Get feature flag evaluator instance

    Returns:
        Feature flag evaluator
    """
    return FeatureFlagEvaluator()


def get_logger() -> structlog.BoundLogger:
    """
    Get structured logger instance

    Returns:
        Configured structlog logger
    """
    return structlog.get_logger()


def get_db(request: Request) -> DatabaseAdapter:
    """
    Get database adapter from application state

    Args:
        request: FastAPI request object

    Returns:
        Database adapter instance

    Raises:
        RuntimeError: If database not initialized
    """
    if not hasattr(request.app.state, "db"):
        raise RuntimeError(
            "Database not initialized. Ensure lifespan context manager is configured."
        )

    return request.app.state.db


def get_db_session(request: Request) -> Generator:
    """
    Get database session with automatic cleanup

    Args:
        request: FastAPI request object

    Yields:
        Database session

    Note:
        This is a generator function that ensures proper cleanup
        even if an exception occurs during the request.
    """
    db = get_db(request)

    try:
        # For async operations, we return the adapter directly
        # Repository pattern handles transaction management
        yield db
    finally:
        # Cleanup if needed (adapter manages its own connection pool)
        pass


def get_correlation_id(request: Request) -> str:
    """
    Get correlation ID from request

    Args:
        request: FastAPI request object

    Returns:
        Correlation ID from request headers or context
    """
    from logging_lib.correlation import get_correlation_id as get_ctx_correlation_id

    # Try to get from request headers first
    correlation_id = request.headers.get("X-Correlation-ID")

    # Fallback to context variable
    if not correlation_id:
        correlation_id = get_ctx_correlation_id()

    return correlation_id


def get_request_logger(request: Request) -> structlog.BoundLogger:
    """
    Get logger bound to current request context

    Args:
        request: FastAPI request object

    Returns:
        Logger with request context (correlation_id, method, path)
    """
    logger = get_logger()
    correlation_id = get_correlation_id(request)

    return logger.bind(
        correlation_id=correlation_id,
        method=request.method,
        path=request.url.path,
    )
