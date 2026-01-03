"""
Log Data Sanitizer

Redacts sensitive data from log entries.
Equivalent to TypeScript sanitizer.ts.
"""

import re
from typing import Any

# Sensitive field patterns to redact
SENSITIVE_PATTERNS = [
    re.compile(r"password", re.IGNORECASE),
    re.compile(r"secret", re.IGNORECASE),
    re.compile(r"token", re.IGNORECASE),
    re.compile(r"api[_-]?key", re.IGNORECASE),
    re.compile(r"authorization", re.IGNORECASE),
    re.compile(r"cookie", re.IGNORECASE),
    re.compile(r"ssn", re.IGNORECASE),
    re.compile(r"credit[_-]?card", re.IGNORECASE),
    re.compile(r"card[_-]?number", re.IGNORECASE),
    re.compile(r"cvv", re.IGNORECASE),
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


def x_sanitize_log_data__mutmut_orig(data: Any) -> Any:
    """
    Sanitize log data by redacting sensitive fields

    Recursively processes dictionaries and lists to find and redact
    fields matching sensitive patterns.

    Args:
        data: Data to sanitize (dict, list, or primitive)

    Returns:
        Sanitized data with sensitive fields redacted
    """
    if data is None or isinstance(data, (str, int, float, bool)):
        return data

    if isinstance(data, list):
        return [sanitize_log_data(item) for item in data]

    if isinstance(data, dict):
        sanitized = {}
        for key, value in data.items():
            # Check if key matches sensitive pattern
            if any(pattern.search(key) for pattern in SENSITIVE_PATTERNS):
                sanitized[key] = "[REDACTED]"
            elif isinstance(value, (dict, list)):
                sanitized[key] = sanitize_log_data(value)
            else:
                sanitized[key] = value
        return sanitized

    # For other types (objects, etc.), return as is
    return data


def x_sanitize_log_data__mutmut_1(data: Any) -> Any:
    """
    Sanitize log data by redacting sensitive fields

    Recursively processes dictionaries and lists to find and redact
    fields matching sensitive patterns.

    Args:
        data: Data to sanitize (dict, list, or primitive)

    Returns:
        Sanitized data with sensitive fields redacted
    """
    if data is None and isinstance(data, (str, int, float, bool)):
        return data

    if isinstance(data, list):
        return [sanitize_log_data(item) for item in data]

    if isinstance(data, dict):
        sanitized = {}
        for key, value in data.items():
            # Check if key matches sensitive pattern
            if any(pattern.search(key) for pattern in SENSITIVE_PATTERNS):
                sanitized[key] = "[REDACTED]"
            elif isinstance(value, (dict, list)):
                sanitized[key] = sanitize_log_data(value)
            else:
                sanitized[key] = value
        return sanitized

    # For other types (objects, etc.), return as is
    return data


def x_sanitize_log_data__mutmut_2(data: Any) -> Any:
    """
    Sanitize log data by redacting sensitive fields

    Recursively processes dictionaries and lists to find and redact
    fields matching sensitive patterns.

    Args:
        data: Data to sanitize (dict, list, or primitive)

    Returns:
        Sanitized data with sensitive fields redacted
    """
    if data is not None or isinstance(data, (str, int, float, bool)):
        return data

    if isinstance(data, list):
        return [sanitize_log_data(item) for item in data]

    if isinstance(data, dict):
        sanitized = {}
        for key, value in data.items():
            # Check if key matches sensitive pattern
            if any(pattern.search(key) for pattern in SENSITIVE_PATTERNS):
                sanitized[key] = "[REDACTED]"
            elif isinstance(value, (dict, list)):
                sanitized[key] = sanitize_log_data(value)
            else:
                sanitized[key] = value
        return sanitized

    # For other types (objects, etc.), return as is
    return data


def x_sanitize_log_data__mutmut_3(data: Any) -> Any:
    """
    Sanitize log data by redacting sensitive fields

    Recursively processes dictionaries and lists to find and redact
    fields matching sensitive patterns.

    Args:
        data: Data to sanitize (dict, list, or primitive)

    Returns:
        Sanitized data with sensitive fields redacted
    """
    if data is None or isinstance(data, (str, int, float, bool)):
        return data

    if isinstance(data, list):
        return [sanitize_log_data(None) for item in data]

    if isinstance(data, dict):
        sanitized = {}
        for key, value in data.items():
            # Check if key matches sensitive pattern
            if any(pattern.search(key) for pattern in SENSITIVE_PATTERNS):
                sanitized[key] = "[REDACTED]"
            elif isinstance(value, (dict, list)):
                sanitized[key] = sanitize_log_data(value)
            else:
                sanitized[key] = value
        return sanitized

    # For other types (objects, etc.), return as is
    return data


def x_sanitize_log_data__mutmut_4(data: Any) -> Any:
    """
    Sanitize log data by redacting sensitive fields

    Recursively processes dictionaries and lists to find and redact
    fields matching sensitive patterns.

    Args:
        data: Data to sanitize (dict, list, or primitive)

    Returns:
        Sanitized data with sensitive fields redacted
    """
    if data is None or isinstance(data, (str, int, float, bool)):
        return data

    if isinstance(data, list):
        return [sanitize_log_data(item) for item in data]

    if isinstance(data, dict):
        sanitized = None
        for key, value in data.items():
            # Check if key matches sensitive pattern
            if any(pattern.search(key) for pattern in SENSITIVE_PATTERNS):
                sanitized[key] = "[REDACTED]"
            elif isinstance(value, (dict, list)):
                sanitized[key] = sanitize_log_data(value)
            else:
                sanitized[key] = value
        return sanitized

    # For other types (objects, etc.), return as is
    return data


def x_sanitize_log_data__mutmut_5(data: Any) -> Any:
    """
    Sanitize log data by redacting sensitive fields

    Recursively processes dictionaries and lists to find and redact
    fields matching sensitive patterns.

    Args:
        data: Data to sanitize (dict, list, or primitive)

    Returns:
        Sanitized data with sensitive fields redacted
    """
    if data is None or isinstance(data, (str, int, float, bool)):
        return data

    if isinstance(data, list):
        return [sanitize_log_data(item) for item in data]

    if isinstance(data, dict):
        sanitized = {}
        for key, value in data.items():
            # Check if key matches sensitive pattern
            if any(None):
                sanitized[key] = "[REDACTED]"
            elif isinstance(value, (dict, list)):
                sanitized[key] = sanitize_log_data(value)
            else:
                sanitized[key] = value
        return sanitized

    # For other types (objects, etc.), return as is
    return data


def x_sanitize_log_data__mutmut_6(data: Any) -> Any:
    """
    Sanitize log data by redacting sensitive fields

    Recursively processes dictionaries and lists to find and redact
    fields matching sensitive patterns.

    Args:
        data: Data to sanitize (dict, list, or primitive)

    Returns:
        Sanitized data with sensitive fields redacted
    """
    if data is None or isinstance(data, (str, int, float, bool)):
        return data

    if isinstance(data, list):
        return [sanitize_log_data(item) for item in data]

    if isinstance(data, dict):
        sanitized = {}
        for key, value in data.items():
            # Check if key matches sensitive pattern
            if any(pattern.search(None) for pattern in SENSITIVE_PATTERNS):
                sanitized[key] = "[REDACTED]"
            elif isinstance(value, (dict, list)):
                sanitized[key] = sanitize_log_data(value)
            else:
                sanitized[key] = value
        return sanitized

    # For other types (objects, etc.), return as is
    return data


def x_sanitize_log_data__mutmut_7(data: Any) -> Any:
    """
    Sanitize log data by redacting sensitive fields

    Recursively processes dictionaries and lists to find and redact
    fields matching sensitive patterns.

    Args:
        data: Data to sanitize (dict, list, or primitive)

    Returns:
        Sanitized data with sensitive fields redacted
    """
    if data is None or isinstance(data, (str, int, float, bool)):
        return data

    if isinstance(data, list):
        return [sanitize_log_data(item) for item in data]

    if isinstance(data, dict):
        sanitized = {}
        for key, value in data.items():
            # Check if key matches sensitive pattern
            if any(pattern.search(key) for pattern in SENSITIVE_PATTERNS):
                sanitized[key] = None
            elif isinstance(value, (dict, list)):
                sanitized[key] = sanitize_log_data(value)
            else:
                sanitized[key] = value
        return sanitized

    # For other types (objects, etc.), return as is
    return data


def x_sanitize_log_data__mutmut_8(data: Any) -> Any:
    """
    Sanitize log data by redacting sensitive fields

    Recursively processes dictionaries and lists to find and redact
    fields matching sensitive patterns.

    Args:
        data: Data to sanitize (dict, list, or primitive)

    Returns:
        Sanitized data with sensitive fields redacted
    """
    if data is None or isinstance(data, (str, int, float, bool)):
        return data

    if isinstance(data, list):
        return [sanitize_log_data(item) for item in data]

    if isinstance(data, dict):
        sanitized = {}
        for key, value in data.items():
            # Check if key matches sensitive pattern
            if any(pattern.search(key) for pattern in SENSITIVE_PATTERNS):
                sanitized[key] = "XX[REDACTED]XX"
            elif isinstance(value, (dict, list)):
                sanitized[key] = sanitize_log_data(value)
            else:
                sanitized[key] = value
        return sanitized

    # For other types (objects, etc.), return as is
    return data


def x_sanitize_log_data__mutmut_9(data: Any) -> Any:
    """
    Sanitize log data by redacting sensitive fields

    Recursively processes dictionaries and lists to find and redact
    fields matching sensitive patterns.

    Args:
        data: Data to sanitize (dict, list, or primitive)

    Returns:
        Sanitized data with sensitive fields redacted
    """
    if data is None or isinstance(data, (str, int, float, bool)):
        return data

    if isinstance(data, list):
        return [sanitize_log_data(item) for item in data]

    if isinstance(data, dict):
        sanitized = {}
        for key, value in data.items():
            # Check if key matches sensitive pattern
            if any(pattern.search(key) for pattern in SENSITIVE_PATTERNS):
                sanitized[key] = "[redacted]"
            elif isinstance(value, (dict, list)):
                sanitized[key] = sanitize_log_data(value)
            else:
                sanitized[key] = value
        return sanitized

    # For other types (objects, etc.), return as is
    return data


def x_sanitize_log_data__mutmut_10(data: Any) -> Any:
    """
    Sanitize log data by redacting sensitive fields

    Recursively processes dictionaries and lists to find and redact
    fields matching sensitive patterns.

    Args:
        data: Data to sanitize (dict, list, or primitive)

    Returns:
        Sanitized data with sensitive fields redacted
    """
    if data is None or isinstance(data, (str, int, float, bool)):
        return data

    if isinstance(data, list):
        return [sanitize_log_data(item) for item in data]

    if isinstance(data, dict):
        sanitized = {}
        for key, value in data.items():
            # Check if key matches sensitive pattern
            if any(pattern.search(key) for pattern in SENSITIVE_PATTERNS):
                sanitized[key] = "[REDACTED]"
            elif isinstance(value, (dict, list)):
                sanitized[key] = None
            else:
                sanitized[key] = value
        return sanitized

    # For other types (objects, etc.), return as is
    return data


def x_sanitize_log_data__mutmut_11(data: Any) -> Any:
    """
    Sanitize log data by redacting sensitive fields

    Recursively processes dictionaries and lists to find and redact
    fields matching sensitive patterns.

    Args:
        data: Data to sanitize (dict, list, or primitive)

    Returns:
        Sanitized data with sensitive fields redacted
    """
    if data is None or isinstance(data, (str, int, float, bool)):
        return data

    if isinstance(data, list):
        return [sanitize_log_data(item) for item in data]

    if isinstance(data, dict):
        sanitized = {}
        for key, value in data.items():
            # Check if key matches sensitive pattern
            if any(pattern.search(key) for pattern in SENSITIVE_PATTERNS):
                sanitized[key] = "[REDACTED]"
            elif isinstance(value, (dict, list)):
                sanitized[key] = sanitize_log_data(None)
            else:
                sanitized[key] = value
        return sanitized

    # For other types (objects, etc.), return as is
    return data


def x_sanitize_log_data__mutmut_12(data: Any) -> Any:
    """
    Sanitize log data by redacting sensitive fields

    Recursively processes dictionaries and lists to find and redact
    fields matching sensitive patterns.

    Args:
        data: Data to sanitize (dict, list, or primitive)

    Returns:
        Sanitized data with sensitive fields redacted
    """
    if data is None or isinstance(data, (str, int, float, bool)):
        return data

    if isinstance(data, list):
        return [sanitize_log_data(item) for item in data]

    if isinstance(data, dict):
        sanitized = {}
        for key, value in data.items():
            # Check if key matches sensitive pattern
            if any(pattern.search(key) for pattern in SENSITIVE_PATTERNS):
                sanitized[key] = "[REDACTED]"
            elif isinstance(value, (dict, list)):
                sanitized[key] = sanitize_log_data(value)
            else:
                sanitized[key] = None
        return sanitized

    # For other types (objects, etc.), return as is
    return data

x_sanitize_log_data__mutmut_mutants : ClassVar[MutantDict] = {
'x_sanitize_log_data__mutmut_1': x_sanitize_log_data__mutmut_1, 
    'x_sanitize_log_data__mutmut_2': x_sanitize_log_data__mutmut_2, 
    'x_sanitize_log_data__mutmut_3': x_sanitize_log_data__mutmut_3, 
    'x_sanitize_log_data__mutmut_4': x_sanitize_log_data__mutmut_4, 
    'x_sanitize_log_data__mutmut_5': x_sanitize_log_data__mutmut_5, 
    'x_sanitize_log_data__mutmut_6': x_sanitize_log_data__mutmut_6, 
    'x_sanitize_log_data__mutmut_7': x_sanitize_log_data__mutmut_7, 
    'x_sanitize_log_data__mutmut_8': x_sanitize_log_data__mutmut_8, 
    'x_sanitize_log_data__mutmut_9': x_sanitize_log_data__mutmut_9, 
    'x_sanitize_log_data__mutmut_10': x_sanitize_log_data__mutmut_10, 
    'x_sanitize_log_data__mutmut_11': x_sanitize_log_data__mutmut_11, 
    'x_sanitize_log_data__mutmut_12': x_sanitize_log_data__mutmut_12
}

def sanitize_log_data(*args, **kwargs):
    result = _mutmut_trampoline(x_sanitize_log_data__mutmut_orig, x_sanitize_log_data__mutmut_mutants, args, kwargs)
    return result 

sanitize_log_data.__signature__ = _mutmut_signature(x_sanitize_log_data__mutmut_orig)
x_sanitize_log_data__mutmut_orig.__name__ = 'x_sanitize_log_data'
