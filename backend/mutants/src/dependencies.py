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


def x_get_db__mutmut_orig(request: Request) -> DatabaseAdapter:
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


def x_get_db__mutmut_1(request: Request) -> DatabaseAdapter:
    """
    Get database adapter from application state

    Args:
        request: FastAPI request object

    Returns:
        Database adapter instance

    Raises:
        RuntimeError: If database not initialized
    """
    if hasattr(request.app.state, "db"):
        raise RuntimeError(
            "Database not initialized. Ensure lifespan context manager is configured."
        )

    return request.app.state.db


def x_get_db__mutmut_2(request: Request) -> DatabaseAdapter:
    """
    Get database adapter from application state

    Args:
        request: FastAPI request object

    Returns:
        Database adapter instance

    Raises:
        RuntimeError: If database not initialized
    """
    if not hasattr(None, "db"):
        raise RuntimeError(
            "Database not initialized. Ensure lifespan context manager is configured."
        )

    return request.app.state.db


def x_get_db__mutmut_3(request: Request) -> DatabaseAdapter:
    """
    Get database adapter from application state

    Args:
        request: FastAPI request object

    Returns:
        Database adapter instance

    Raises:
        RuntimeError: If database not initialized
    """
    if not hasattr(request.app.state, None):
        raise RuntimeError(
            "Database not initialized. Ensure lifespan context manager is configured."
        )

    return request.app.state.db


def x_get_db__mutmut_4(request: Request) -> DatabaseAdapter:
    """
    Get database adapter from application state

    Args:
        request: FastAPI request object

    Returns:
        Database adapter instance

    Raises:
        RuntimeError: If database not initialized
    """
    if not hasattr("db"):
        raise RuntimeError(
            "Database not initialized. Ensure lifespan context manager is configured."
        )

    return request.app.state.db


def x_get_db__mutmut_5(request: Request) -> DatabaseAdapter:
    """
    Get database adapter from application state

    Args:
        request: FastAPI request object

    Returns:
        Database adapter instance

    Raises:
        RuntimeError: If database not initialized
    """
    if not hasattr(request.app.state, ):
        raise RuntimeError(
            "Database not initialized. Ensure lifespan context manager is configured."
        )

    return request.app.state.db


def x_get_db__mutmut_6(request: Request) -> DatabaseAdapter:
    """
    Get database adapter from application state

    Args:
        request: FastAPI request object

    Returns:
        Database adapter instance

    Raises:
        RuntimeError: If database not initialized
    """
    if not hasattr(request.app.state, "XXdbXX"):
        raise RuntimeError(
            "Database not initialized. Ensure lifespan context manager is configured."
        )

    return request.app.state.db


def x_get_db__mutmut_7(request: Request) -> DatabaseAdapter:
    """
    Get database adapter from application state

    Args:
        request: FastAPI request object

    Returns:
        Database adapter instance

    Raises:
        RuntimeError: If database not initialized
    """
    if not hasattr(request.app.state, "DB"):
        raise RuntimeError(
            "Database not initialized. Ensure lifespan context manager is configured."
        )

    return request.app.state.db


def x_get_db__mutmut_8(request: Request) -> DatabaseAdapter:
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
            None
        )

    return request.app.state.db


def x_get_db__mutmut_9(request: Request) -> DatabaseAdapter:
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
            "XXDatabase not initialized. Ensure lifespan context manager is configured.XX"
        )

    return request.app.state.db


def x_get_db__mutmut_10(request: Request) -> DatabaseAdapter:
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
            "database not initialized. ensure lifespan context manager is configured."
        )

    return request.app.state.db


def x_get_db__mutmut_11(request: Request) -> DatabaseAdapter:
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
            "DATABASE NOT INITIALIZED. ENSURE LIFESPAN CONTEXT MANAGER IS CONFIGURED."
        )

    return request.app.state.db

x_get_db__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_db__mutmut_1': x_get_db__mutmut_1, 
    'x_get_db__mutmut_2': x_get_db__mutmut_2, 
    'x_get_db__mutmut_3': x_get_db__mutmut_3, 
    'x_get_db__mutmut_4': x_get_db__mutmut_4, 
    'x_get_db__mutmut_5': x_get_db__mutmut_5, 
    'x_get_db__mutmut_6': x_get_db__mutmut_6, 
    'x_get_db__mutmut_7': x_get_db__mutmut_7, 
    'x_get_db__mutmut_8': x_get_db__mutmut_8, 
    'x_get_db__mutmut_9': x_get_db__mutmut_9, 
    'x_get_db__mutmut_10': x_get_db__mutmut_10, 
    'x_get_db__mutmut_11': x_get_db__mutmut_11
}

def get_db(*args, **kwargs):
    result = _mutmut_trampoline(x_get_db__mutmut_orig, x_get_db__mutmut_mutants, args, kwargs)
    return result 

get_db.__signature__ = _mutmut_signature(x_get_db__mutmut_orig)
x_get_db__mutmut_orig.__name__ = 'x_get_db'


def x_get_db_session__mutmut_orig(request: Request) -> Generator:
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


def x_get_db_session__mutmut_1(request: Request) -> Generator:
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
    db = None

    try:
        # For async operations, we return the adapter directly
        # Repository pattern handles transaction management
        yield db
    finally:
        # Cleanup if needed (adapter manages its own connection pool)
        pass


def x_get_db_session__mutmut_2(request: Request) -> Generator:
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
    db = get_db(None)

    try:
        # For async operations, we return the adapter directly
        # Repository pattern handles transaction management
        yield db
    finally:
        # Cleanup if needed (adapter manages its own connection pool)
        pass

x_get_db_session__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_db_session__mutmut_1': x_get_db_session__mutmut_1, 
    'x_get_db_session__mutmut_2': x_get_db_session__mutmut_2
}

def get_db_session(*args, **kwargs):
    result = _mutmut_trampoline(x_get_db_session__mutmut_orig, x_get_db_session__mutmut_mutants, args, kwargs)
    return result 

get_db_session.__signature__ = _mutmut_signature(x_get_db_session__mutmut_orig)
x_get_db_session__mutmut_orig.__name__ = 'x_get_db_session'


def x_get_correlation_id__mutmut_orig(request: Request) -> str:
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


def x_get_correlation_id__mutmut_1(request: Request) -> str:
    """
    Get correlation ID from request

    Args:
        request: FastAPI request object

    Returns:
        Correlation ID from request headers or context
    """
    from logging_lib.correlation import get_correlation_id as get_ctx_correlation_id

    # Try to get from request headers first
    correlation_id = None

    # Fallback to context variable
    if not correlation_id:
        correlation_id = get_ctx_correlation_id()

    return correlation_id


def x_get_correlation_id__mutmut_2(request: Request) -> str:
    """
    Get correlation ID from request

    Args:
        request: FastAPI request object

    Returns:
        Correlation ID from request headers or context
    """
    from logging_lib.correlation import get_correlation_id as get_ctx_correlation_id

    # Try to get from request headers first
    correlation_id = request.headers.get(None)

    # Fallback to context variable
    if not correlation_id:
        correlation_id = get_ctx_correlation_id()

    return correlation_id


def x_get_correlation_id__mutmut_3(request: Request) -> str:
    """
    Get correlation ID from request

    Args:
        request: FastAPI request object

    Returns:
        Correlation ID from request headers or context
    """
    from logging_lib.correlation import get_correlation_id as get_ctx_correlation_id

    # Try to get from request headers first
    correlation_id = request.headers.get("XXX-Correlation-IDXX")

    # Fallback to context variable
    if not correlation_id:
        correlation_id = get_ctx_correlation_id()

    return correlation_id


def x_get_correlation_id__mutmut_4(request: Request) -> str:
    """
    Get correlation ID from request

    Args:
        request: FastAPI request object

    Returns:
        Correlation ID from request headers or context
    """
    from logging_lib.correlation import get_correlation_id as get_ctx_correlation_id

    # Try to get from request headers first
    correlation_id = request.headers.get("x-correlation-id")

    # Fallback to context variable
    if not correlation_id:
        correlation_id = get_ctx_correlation_id()

    return correlation_id


def x_get_correlation_id__mutmut_5(request: Request) -> str:
    """
    Get correlation ID from request

    Args:
        request: FastAPI request object

    Returns:
        Correlation ID from request headers or context
    """
    from logging_lib.correlation import get_correlation_id as get_ctx_correlation_id

    # Try to get from request headers first
    correlation_id = request.headers.get("X-CORRELATION-ID")

    # Fallback to context variable
    if not correlation_id:
        correlation_id = get_ctx_correlation_id()

    return correlation_id


def x_get_correlation_id__mutmut_6(request: Request) -> str:
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
    if correlation_id:
        correlation_id = get_ctx_correlation_id()

    return correlation_id


def x_get_correlation_id__mutmut_7(request: Request) -> str:
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
        correlation_id = None

    return correlation_id

x_get_correlation_id__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_correlation_id__mutmut_1': x_get_correlation_id__mutmut_1, 
    'x_get_correlation_id__mutmut_2': x_get_correlation_id__mutmut_2, 
    'x_get_correlation_id__mutmut_3': x_get_correlation_id__mutmut_3, 
    'x_get_correlation_id__mutmut_4': x_get_correlation_id__mutmut_4, 
    'x_get_correlation_id__mutmut_5': x_get_correlation_id__mutmut_5, 
    'x_get_correlation_id__mutmut_6': x_get_correlation_id__mutmut_6, 
    'x_get_correlation_id__mutmut_7': x_get_correlation_id__mutmut_7
}

def get_correlation_id(*args, **kwargs):
    result = _mutmut_trampoline(x_get_correlation_id__mutmut_orig, x_get_correlation_id__mutmut_mutants, args, kwargs)
    return result 

get_correlation_id.__signature__ = _mutmut_signature(x_get_correlation_id__mutmut_orig)
x_get_correlation_id__mutmut_orig.__name__ = 'x_get_correlation_id'


def x_get_request_logger__mutmut_orig(request: Request) -> structlog.BoundLogger:
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


def x_get_request_logger__mutmut_1(request: Request) -> structlog.BoundLogger:
    """
    Get logger bound to current request context

    Args:
        request: FastAPI request object

    Returns:
        Logger with request context (correlation_id, method, path)
    """
    logger = None
    correlation_id = get_correlation_id(request)

    return logger.bind(
        correlation_id=correlation_id,
        method=request.method,
        path=request.url.path,
    )


def x_get_request_logger__mutmut_2(request: Request) -> structlog.BoundLogger:
    """
    Get logger bound to current request context

    Args:
        request: FastAPI request object

    Returns:
        Logger with request context (correlation_id, method, path)
    """
    logger = get_logger()
    correlation_id = None

    return logger.bind(
        correlation_id=correlation_id,
        method=request.method,
        path=request.url.path,
    )


def x_get_request_logger__mutmut_3(request: Request) -> structlog.BoundLogger:
    """
    Get logger bound to current request context

    Args:
        request: FastAPI request object

    Returns:
        Logger with request context (correlation_id, method, path)
    """
    logger = get_logger()
    correlation_id = get_correlation_id(None)

    return logger.bind(
        correlation_id=correlation_id,
        method=request.method,
        path=request.url.path,
    )


def x_get_request_logger__mutmut_4(request: Request) -> structlog.BoundLogger:
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
        correlation_id=None,
        method=request.method,
        path=request.url.path,
    )


def x_get_request_logger__mutmut_5(request: Request) -> structlog.BoundLogger:
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
        method=None,
        path=request.url.path,
    )


def x_get_request_logger__mutmut_6(request: Request) -> structlog.BoundLogger:
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
        path=None,
    )


def x_get_request_logger__mutmut_7(request: Request) -> structlog.BoundLogger:
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
        method=request.method,
        path=request.url.path,
    )


def x_get_request_logger__mutmut_8(request: Request) -> structlog.BoundLogger:
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
        path=request.url.path,
    )


def x_get_request_logger__mutmut_9(request: Request) -> structlog.BoundLogger:
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
        )

x_get_request_logger__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_request_logger__mutmut_1': x_get_request_logger__mutmut_1, 
    'x_get_request_logger__mutmut_2': x_get_request_logger__mutmut_2, 
    'x_get_request_logger__mutmut_3': x_get_request_logger__mutmut_3, 
    'x_get_request_logger__mutmut_4': x_get_request_logger__mutmut_4, 
    'x_get_request_logger__mutmut_5': x_get_request_logger__mutmut_5, 
    'x_get_request_logger__mutmut_6': x_get_request_logger__mutmut_6, 
    'x_get_request_logger__mutmut_7': x_get_request_logger__mutmut_7, 
    'x_get_request_logger__mutmut_8': x_get_request_logger__mutmut_8, 
    'x_get_request_logger__mutmut_9': x_get_request_logger__mutmut_9
}

def get_request_logger(*args, **kwargs):
    result = _mutmut_trampoline(x_get_request_logger__mutmut_orig, x_get_request_logger__mutmut_mutants, args, kwargs)
    return result 

get_request_logger.__signature__ = _mutmut_signature(x_get_request_logger__mutmut_orig)
x_get_request_logger__mutmut_orig.__name__ = 'x_get_request_logger'
