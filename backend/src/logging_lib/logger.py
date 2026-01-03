"""
Structured Logger Configuration

Configures structlog with rotation, retention, and correlation ID support.
Equivalent to TypeScript logger.ts.
"""

import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime
import structlog
from structlog.types import FilteringBoundLogger

from logging_lib.correlation import get_correlation_id
from logging_lib.sanitizer import sanitize_log_data


def add_correlation_id(logger, method_name, event_dict):
    """
    Processor to add correlation ID to log entries

    Args:
        logger: Logger instance
        method_name: Log method name
        event_dict: Event dictionary

    Returns:
        Updated event dictionary with correlation_id
    """
    event_dict["correlation_id"] = get_correlation_id()
    return event_dict


def sanitize_processor(logger, method_name, event_dict):
    """
    Processor to sanitize sensitive data from log entries

    Args:
        logger: Logger instance
        method_name: Log method name
        event_dict: Event dictionary

    Returns:
        Sanitized event dictionary
    """
    return sanitize_log_data(event_dict)


def configure_logging() -> FilteringBoundLogger:
    """
    Configure structured logging with rotation and retention

    Sets up structlog with:
    - Correlation ID injection
    - Sensitive data sanitization
    - File rotation (100MB OR daily)
    - Console and file outputs
    - Environment-specific formatting

    Returns:
        Configured logger instance
    """
    # Import config here to avoid circular dependency
    from config import config_loader

    config = config_loader.load()

    # Ensure log directory exists
    os.makedirs(config.LOG_DIR, exist_ok=True)

    # Create handlers
    handlers = []

    # Console handler
    if config.LOG_CONSOLE_ENABLED:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(config.LOG_LEVEL)
        handlers.append(console_handler)

    # File handler with rotation
    log_filename = os.path.join(config.LOG_DIR, f"app-{datetime.now().strftime('%Y-%m-%d')}-1.log")

    # Hybrid rotation: size OR time-based
    file_handler = RotatingFileHandler(
        log_filename,
        maxBytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        backupCount=config.LOG_RETENTION_DAYS,
    )
    file_handler.setLevel(config.LOG_LEVEL)
    handlers.append(file_handler)

    # Configure structlog processors
    processors = [
        structlog.contextvars.merge_contextvars,
        add_correlation_id,
        structlog.processors.add_log_level,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.TimeStamper(fmt="iso"),
        sanitize_processor,
    ]

    # Add appropriate renderer based on environment
    if config.LOG_PRETTY_PRINT:
        processors.append(structlog.dev.ConsoleRenderer())
    else:
        processors.append(structlog.processors.JSONRenderer())

    # Configure structlog
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(logging.getLevelName(config.LOG_LEVEL)),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Configure root logger
    logging.basicConfig(
        format="%(message)s",
        level=config.LOG_LEVEL,
        handlers=handlers,
    )

    # Add environment metadata to all logs
    logger = structlog.get_logger()
    logger = logger.bind(
        environment=config.ENVIRONMENT_MODE,
        service="study-abroad-backend",
        version=config.APP_VERSION,
    )

    return logger


# Global logger instance (lazy initialization)
_logger: FilteringBoundLogger | None = None


def get_logger() -> FilteringBoundLogger:
    """
    Get configured logger instance

    Lazy initialization ensures config is loaded first.

    Returns:
        Configured logger
    """
    global _logger
    if _logger is None:
        _logger = configure_logging()
    return _logger


# Export as 'logger' for convenience
logger = get_logger()
