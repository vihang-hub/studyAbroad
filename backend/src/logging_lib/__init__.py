"""
Logging Module

Structured logging with rotation, retention, and correlation ID support.
Equivalent to TypeScript @study-abroad/shared-logging package.

This module provides:
- logger: Configured structlog logger instance
- CorrelationContext: Correlation ID management (using contextvars)
- sanitize_log_data: Sensitive data redaction

Usage:
    from logging_lib import logger, CorrelationContext

    with CorrelationContext():
        logger.info("User logged in", user_id=user_id)
"""

from logging_lib.logger import configure_logging, logger
from logging_lib.correlation import CorrelationContext, get_correlation_id, set_correlation_id
from logging_lib.sanitizer import sanitize_log_data

__all__ = [
    "logger",
    "configure_logging",
    "CorrelationContext",
    "get_correlation_id",
    "set_correlation_id",
    "sanitize_log_data",
]
