"""
Feature Flag Types

Enum definitions for feature flags.
Equivalent to TypeScript flags.ts.
"""

from enum import Enum


class Feature(str, Enum):
    """
    Feature Flag Enum

    Defines all available feature flags in the system.
    """

    SUPABASE = "ENABLE_SUPABASE"
    PAYMENTS = "ENABLE_PAYMENTS"
    RATE_LIMITING = "ENABLE_RATE_LIMITING"
    OBSERVABILITY = "ENABLE_OBSERVABILITY"

    def __str__(self) -> str:
        return self.value
