"""
Structured Logger Configuration

Configures structlog with rotation, retention, and correlation ID support.
Equivalent to TypeScript logger.ts.
"""

import os
import logging
from datetime import datetime
import structlog
from structlog.types import FilteringBoundLogger

from logging_lib.correlation import get_correlation_id
from logging_lib.sanitizer import sanitize_log_data
from logging_lib.rotation import DateSequenceRotatingHandler
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


def x_add_correlation_id__mutmut_orig(logger, method_name, event_dict):
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


def x_add_correlation_id__mutmut_1(logger, method_name, event_dict):
    """
    Processor to add correlation ID to log entries

    Args:
        logger: Logger instance
        method_name: Log method name
        event_dict: Event dictionary

    Returns:
        Updated event dictionary with correlation_id
    """
    event_dict["correlation_id"] = None
    return event_dict


def x_add_correlation_id__mutmut_2(logger, method_name, event_dict):
    """
    Processor to add correlation ID to log entries

    Args:
        logger: Logger instance
        method_name: Log method name
        event_dict: Event dictionary

    Returns:
        Updated event dictionary with correlation_id
    """
    event_dict["XXcorrelation_idXX"] = get_correlation_id()
    return event_dict


def x_add_correlation_id__mutmut_3(logger, method_name, event_dict):
    """
    Processor to add correlation ID to log entries

    Args:
        logger: Logger instance
        method_name: Log method name
        event_dict: Event dictionary

    Returns:
        Updated event dictionary with correlation_id
    """
    event_dict["CORRELATION_ID"] = get_correlation_id()
    return event_dict

x_add_correlation_id__mutmut_mutants : ClassVar[MutantDict] = {
'x_add_correlation_id__mutmut_1': x_add_correlation_id__mutmut_1, 
    'x_add_correlation_id__mutmut_2': x_add_correlation_id__mutmut_2, 
    'x_add_correlation_id__mutmut_3': x_add_correlation_id__mutmut_3
}

def add_correlation_id(*args, **kwargs):
    result = _mutmut_trampoline(x_add_correlation_id__mutmut_orig, x_add_correlation_id__mutmut_mutants, args, kwargs)
    return result 

add_correlation_id.__signature__ = _mutmut_signature(x_add_correlation_id__mutmut_orig)
x_add_correlation_id__mutmut_orig.__name__ = 'x_add_correlation_id'


def x_sanitize_processor__mutmut_orig(logger, method_name, event_dict):
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


def x_sanitize_processor__mutmut_1(logger, method_name, event_dict):
    """
    Processor to sanitize sensitive data from log entries

    Args:
        logger: Logger instance
        method_name: Log method name
        event_dict: Event dictionary

    Returns:
        Sanitized event dictionary
    """
    return sanitize_log_data(None)

x_sanitize_processor__mutmut_mutants : ClassVar[MutantDict] = {
'x_sanitize_processor__mutmut_1': x_sanitize_processor__mutmut_1
}

def sanitize_processor(*args, **kwargs):
    result = _mutmut_trampoline(x_sanitize_processor__mutmut_orig, x_sanitize_processor__mutmut_mutants, args, kwargs)
    return result 

sanitize_processor.__signature__ = _mutmut_signature(x_sanitize_processor__mutmut_orig)
x_sanitize_processor__mutmut_orig.__name__ = 'x_sanitize_processor'


def x_configure_logging__mutmut_orig() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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


def x_configure_logging__mutmut_1() -> FilteringBoundLogger:
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

    config = None

    # Ensure log directory exists
    os.makedirs(config.LOG_DIR, exist_ok=True)

    # Create handlers
    handlers = []

    # Console handler
    if config.LOG_CONSOLE_ENABLED:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(config.LOG_LEVEL)
        handlers.append(console_handler)

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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


def x_configure_logging__mutmut_2() -> FilteringBoundLogger:
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
    os.makedirs(None, exist_ok=True)

    # Create handlers
    handlers = []

    # Console handler
    if config.LOG_CONSOLE_ENABLED:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(config.LOG_LEVEL)
        handlers.append(console_handler)

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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


def x_configure_logging__mutmut_3() -> FilteringBoundLogger:
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
    os.makedirs(config.LOG_DIR, exist_ok=None)

    # Create handlers
    handlers = []

    # Console handler
    if config.LOG_CONSOLE_ENABLED:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(config.LOG_LEVEL)
        handlers.append(console_handler)

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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


def x_configure_logging__mutmut_4() -> FilteringBoundLogger:
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
    os.makedirs(exist_ok=True)

    # Create handlers
    handlers = []

    # Console handler
    if config.LOG_CONSOLE_ENABLED:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(config.LOG_LEVEL)
        handlers.append(console_handler)

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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


def x_configure_logging__mutmut_5() -> FilteringBoundLogger:
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
    os.makedirs(config.LOG_DIR, )

    # Create handlers
    handlers = []

    # Console handler
    if config.LOG_CONSOLE_ENABLED:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(config.LOG_LEVEL)
        handlers.append(console_handler)

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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


def x_configure_logging__mutmut_6() -> FilteringBoundLogger:
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
    os.makedirs(config.LOG_DIR, exist_ok=False)

    # Create handlers
    handlers = []

    # Console handler
    if config.LOG_CONSOLE_ENABLED:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(config.LOG_LEVEL)
        handlers.append(console_handler)

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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


def x_configure_logging__mutmut_7() -> FilteringBoundLogger:
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
    handlers = None

    # Console handler
    if config.LOG_CONSOLE_ENABLED:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(config.LOG_LEVEL)
        handlers.append(console_handler)

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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


def x_configure_logging__mutmut_8() -> FilteringBoundLogger:
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
        console_handler = None
        console_handler.setLevel(config.LOG_LEVEL)
        handlers.append(console_handler)

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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


def x_configure_logging__mutmut_9() -> FilteringBoundLogger:
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
        console_handler.setLevel(None)
        handlers.append(console_handler)

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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


def x_configure_logging__mutmut_10() -> FilteringBoundLogger:
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
        handlers.append(None)

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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


def x_configure_logging__mutmut_11() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = None
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


def x_configure_logging__mutmut_12() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=None,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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


def x_configure_logging__mutmut_13() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=None,
        retention_days=config.LOG_RETENTION_DAYS,
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


def x_configure_logging__mutmut_14() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=None,
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


def x_configure_logging__mutmut_15() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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


def x_configure_logging__mutmut_16() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        retention_days=config.LOG_RETENTION_DAYS,
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


def x_configure_logging__mutmut_17() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
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


def x_configure_logging__mutmut_18() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 / 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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


def x_configure_logging__mutmut_19() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB / 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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


def x_configure_logging__mutmut_20() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1025 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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


def x_configure_logging__mutmut_21() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1025,
        retention_days=config.LOG_RETENTION_DAYS,
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


def x_configure_logging__mutmut_22() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
    )
    file_handler.setLevel(None)
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


def x_configure_logging__mutmut_23() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
    )
    file_handler.setLevel(config.LOG_LEVEL)
    handlers.append(None)

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


def x_configure_logging__mutmut_24() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
    )
    file_handler.setLevel(config.LOG_LEVEL)
    handlers.append(file_handler)

    # Configure structlog processors
    processors = None

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


def x_configure_logging__mutmut_25() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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
        structlog.processors.TimeStamper(fmt=None),
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


def x_configure_logging__mutmut_26() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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
        structlog.processors.TimeStamper(fmt="XXisoXX"),
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


def x_configure_logging__mutmut_27() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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
        structlog.processors.TimeStamper(fmt="ISO"),
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


def x_configure_logging__mutmut_28() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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
        processors.append(None)
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


def x_configure_logging__mutmut_29() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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
        processors.append(None)

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


def x_configure_logging__mutmut_30() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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
        processors=None,
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


def x_configure_logging__mutmut_31() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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
        wrapper_class=None,
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


def x_configure_logging__mutmut_32() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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
        context_class=None,
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


def x_configure_logging__mutmut_33() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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
        logger_factory=None,
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


def x_configure_logging__mutmut_34() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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
        cache_logger_on_first_use=None,
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


def x_configure_logging__mutmut_35() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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


def x_configure_logging__mutmut_36() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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


def x_configure_logging__mutmut_37() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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


def x_configure_logging__mutmut_38() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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


def x_configure_logging__mutmut_39() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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


def x_configure_logging__mutmut_40() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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
        wrapper_class=structlog.make_filtering_bound_logger(None),
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


def x_configure_logging__mutmut_41() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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
        wrapper_class=structlog.make_filtering_bound_logger(logging.getLevelName(None)),
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


def x_configure_logging__mutmut_42() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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
        cache_logger_on_first_use=False,
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


def x_configure_logging__mutmut_43() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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
        format=None,
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


def x_configure_logging__mutmut_44() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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
        level=None,
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


def x_configure_logging__mutmut_45() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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
        handlers=None,
    )

    # Add environment metadata to all logs
    logger = structlog.get_logger()
    logger = logger.bind(
        environment=config.ENVIRONMENT_MODE,
        service="study-abroad-backend",
        version=config.APP_VERSION,
    )

    return logger


def x_configure_logging__mutmut_46() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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


def x_configure_logging__mutmut_47() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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


def x_configure_logging__mutmut_48() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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
        )

    # Add environment metadata to all logs
    logger = structlog.get_logger()
    logger = logger.bind(
        environment=config.ENVIRONMENT_MODE,
        service="study-abroad-backend",
        version=config.APP_VERSION,
    )

    return logger


def x_configure_logging__mutmut_49() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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
        format="XX%(message)sXX",
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


def x_configure_logging__mutmut_50() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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
        format="%(MESSAGE)S",
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


def x_configure_logging__mutmut_51() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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
    logger = None
    logger = logger.bind(
        environment=config.ENVIRONMENT_MODE,
        service="study-abroad-backend",
        version=config.APP_VERSION,
    )

    return logger


def x_configure_logging__mutmut_52() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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
    logger = None

    return logger


def x_configure_logging__mutmut_53() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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
        environment=None,
        service="study-abroad-backend",
        version=config.APP_VERSION,
    )

    return logger


def x_configure_logging__mutmut_54() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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
        service=None,
        version=config.APP_VERSION,
    )

    return logger


def x_configure_logging__mutmut_55() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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
        version=None,
    )

    return logger


def x_configure_logging__mutmut_56() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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
        service="study-abroad-backend",
        version=config.APP_VERSION,
    )

    return logger


def x_configure_logging__mutmut_57() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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
        version=config.APP_VERSION,
    )

    return logger


def x_configure_logging__mutmut_58() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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
        )

    return logger


def x_configure_logging__mutmut_59() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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
        service="XXstudy-abroad-backendXX",
        version=config.APP_VERSION,
    )

    return logger


def x_configure_logging__mutmut_60() -> FilteringBoundLogger:
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

    # File handler with hybrid rotation (size OR time-based, date-sequence naming)
    # T050a: Configure structlog with date-sequence file rotation
    file_handler = DateSequenceRotatingHandler(
        log_dir=config.LOG_DIR,
        max_bytes=config.LOG_MAX_SIZE_MB * 1024 * 1024,
        retention_days=config.LOG_RETENTION_DAYS,
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
        service="STUDY-ABROAD-BACKEND",
        version=config.APP_VERSION,
    )

    return logger

x_configure_logging__mutmut_mutants : ClassVar[MutantDict] = {
'x_configure_logging__mutmut_1': x_configure_logging__mutmut_1, 
    'x_configure_logging__mutmut_2': x_configure_logging__mutmut_2, 
    'x_configure_logging__mutmut_3': x_configure_logging__mutmut_3, 
    'x_configure_logging__mutmut_4': x_configure_logging__mutmut_4, 
    'x_configure_logging__mutmut_5': x_configure_logging__mutmut_5, 
    'x_configure_logging__mutmut_6': x_configure_logging__mutmut_6, 
    'x_configure_logging__mutmut_7': x_configure_logging__mutmut_7, 
    'x_configure_logging__mutmut_8': x_configure_logging__mutmut_8, 
    'x_configure_logging__mutmut_9': x_configure_logging__mutmut_9, 
    'x_configure_logging__mutmut_10': x_configure_logging__mutmut_10, 
    'x_configure_logging__mutmut_11': x_configure_logging__mutmut_11, 
    'x_configure_logging__mutmut_12': x_configure_logging__mutmut_12, 
    'x_configure_logging__mutmut_13': x_configure_logging__mutmut_13, 
    'x_configure_logging__mutmut_14': x_configure_logging__mutmut_14, 
    'x_configure_logging__mutmut_15': x_configure_logging__mutmut_15, 
    'x_configure_logging__mutmut_16': x_configure_logging__mutmut_16, 
    'x_configure_logging__mutmut_17': x_configure_logging__mutmut_17, 
    'x_configure_logging__mutmut_18': x_configure_logging__mutmut_18, 
    'x_configure_logging__mutmut_19': x_configure_logging__mutmut_19, 
    'x_configure_logging__mutmut_20': x_configure_logging__mutmut_20, 
    'x_configure_logging__mutmut_21': x_configure_logging__mutmut_21, 
    'x_configure_logging__mutmut_22': x_configure_logging__mutmut_22, 
    'x_configure_logging__mutmut_23': x_configure_logging__mutmut_23, 
    'x_configure_logging__mutmut_24': x_configure_logging__mutmut_24, 
    'x_configure_logging__mutmut_25': x_configure_logging__mutmut_25, 
    'x_configure_logging__mutmut_26': x_configure_logging__mutmut_26, 
    'x_configure_logging__mutmut_27': x_configure_logging__mutmut_27, 
    'x_configure_logging__mutmut_28': x_configure_logging__mutmut_28, 
    'x_configure_logging__mutmut_29': x_configure_logging__mutmut_29, 
    'x_configure_logging__mutmut_30': x_configure_logging__mutmut_30, 
    'x_configure_logging__mutmut_31': x_configure_logging__mutmut_31, 
    'x_configure_logging__mutmut_32': x_configure_logging__mutmut_32, 
    'x_configure_logging__mutmut_33': x_configure_logging__mutmut_33, 
    'x_configure_logging__mutmut_34': x_configure_logging__mutmut_34, 
    'x_configure_logging__mutmut_35': x_configure_logging__mutmut_35, 
    'x_configure_logging__mutmut_36': x_configure_logging__mutmut_36, 
    'x_configure_logging__mutmut_37': x_configure_logging__mutmut_37, 
    'x_configure_logging__mutmut_38': x_configure_logging__mutmut_38, 
    'x_configure_logging__mutmut_39': x_configure_logging__mutmut_39, 
    'x_configure_logging__mutmut_40': x_configure_logging__mutmut_40, 
    'x_configure_logging__mutmut_41': x_configure_logging__mutmut_41, 
    'x_configure_logging__mutmut_42': x_configure_logging__mutmut_42, 
    'x_configure_logging__mutmut_43': x_configure_logging__mutmut_43, 
    'x_configure_logging__mutmut_44': x_configure_logging__mutmut_44, 
    'x_configure_logging__mutmut_45': x_configure_logging__mutmut_45, 
    'x_configure_logging__mutmut_46': x_configure_logging__mutmut_46, 
    'x_configure_logging__mutmut_47': x_configure_logging__mutmut_47, 
    'x_configure_logging__mutmut_48': x_configure_logging__mutmut_48, 
    'x_configure_logging__mutmut_49': x_configure_logging__mutmut_49, 
    'x_configure_logging__mutmut_50': x_configure_logging__mutmut_50, 
    'x_configure_logging__mutmut_51': x_configure_logging__mutmut_51, 
    'x_configure_logging__mutmut_52': x_configure_logging__mutmut_52, 
    'x_configure_logging__mutmut_53': x_configure_logging__mutmut_53, 
    'x_configure_logging__mutmut_54': x_configure_logging__mutmut_54, 
    'x_configure_logging__mutmut_55': x_configure_logging__mutmut_55, 
    'x_configure_logging__mutmut_56': x_configure_logging__mutmut_56, 
    'x_configure_logging__mutmut_57': x_configure_logging__mutmut_57, 
    'x_configure_logging__mutmut_58': x_configure_logging__mutmut_58, 
    'x_configure_logging__mutmut_59': x_configure_logging__mutmut_59, 
    'x_configure_logging__mutmut_60': x_configure_logging__mutmut_60
}

def configure_logging(*args, **kwargs):
    result = _mutmut_trampoline(x_configure_logging__mutmut_orig, x_configure_logging__mutmut_mutants, args, kwargs)
    return result 

configure_logging.__signature__ = _mutmut_signature(x_configure_logging__mutmut_orig)
x_configure_logging__mutmut_orig.__name__ = 'x_configure_logging'


# Global logger instance (lazy initialization)
_logger: FilteringBoundLogger | None = None


def x_get_logger__mutmut_orig() -> FilteringBoundLogger:
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


def x_get_logger__mutmut_1() -> FilteringBoundLogger:
    """
    Get configured logger instance

    Lazy initialization ensures config is loaded first.

    Returns:
        Configured logger
    """
    global _logger
    if _logger is not None:
        _logger = configure_logging()
    return _logger


def x_get_logger__mutmut_2() -> FilteringBoundLogger:
    """
    Get configured logger instance

    Lazy initialization ensures config is loaded first.

    Returns:
        Configured logger
    """
    global _logger
    if _logger is None:
        _logger = None
    return _logger

x_get_logger__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_logger__mutmut_1': x_get_logger__mutmut_1, 
    'x_get_logger__mutmut_2': x_get_logger__mutmut_2
}

def get_logger(*args, **kwargs):
    result = _mutmut_trampoline(x_get_logger__mutmut_orig, x_get_logger__mutmut_mutants, args, kwargs)
    return result 

get_logger.__signature__ = _mutmut_signature(x_get_logger__mutmut_orig)
x_get_logger__mutmut_orig.__name__ = 'x_get_logger'


# Export as 'logger' for convenience
logger = get_logger()
