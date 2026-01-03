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


def sanitize_log_data(data: Any) -> Any:
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
