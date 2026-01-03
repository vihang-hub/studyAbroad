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
