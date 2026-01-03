"""
Correlation ID Management

Context-based correlation ID tracking for request tracing.
Equivalent to TypeScript correlation.ts using contextvars.
"""

import uuid
from contextvars import ContextVar
from typing import Optional

# Context variable for correlation ID
_correlation_id_var: ContextVar[Optional[str]] = ContextVar("correlation_id", default=None)


def get_correlation_id() -> str:
    """
    Get current correlation ID

    Returns:
        Current correlation ID or generates new one
    """
    correlation_id = _correlation_id_var.get()
    if correlation_id is None:
        correlation_id = str(uuid.uuid4())
        _correlation_id_var.set(correlation_id)
    return correlation_id


def set_correlation_id(correlation_id: str) -> None:
    """
    Set correlation ID for current context

    Args:
        correlation_id: Correlation ID to set
    """
    _correlation_id_var.set(correlation_id)


def clear_correlation_id() -> None:
    """Clear correlation ID from current context"""
    _correlation_id_var.set(None)


class CorrelationContext:
    """
    Context manager for correlation ID

    Usage:
        with CorrelationContext():
            logger.info("Request started")
            # All logs in this context will have same correlation_id

        with CorrelationContext(correlation_id="custom-id"):
            logger.info("Custom correlation ID")
    """

    def __init__(self, correlation_id: Optional[str] = None):
        """
        Initialize correlation context

        Args:
            correlation_id: Optional correlation ID (generates new one if not provided)
        """
        self.correlation_id = correlation_id or str(uuid.uuid4())
        self.previous_id: Optional[str] = None

    def __enter__(self):
        """Enter context and set correlation ID"""
        self.previous_id = _correlation_id_var.get()
        _correlation_id_var.set(self.correlation_id)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context and restore previous correlation ID"""
        _correlation_id_var.set(self.previous_id)
