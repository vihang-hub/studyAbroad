"""
Environment Configuration Presets

Predefined configuration values for dev/test/production environments.
Equivalent to TypeScript presets.ts.
"""

# Development preset
DEV_PRESET: dict[str, any] = {
    "ENVIRONMENT_MODE": "dev",
    "ENABLE_SUPABASE": False,
    "ENABLE_PAYMENTS": False,
    "LOG_LEVEL": "DEBUG",
    "LOG_PRETTY_PRINT": True,
    "DATABASE_URL": "postgresql://studyabroad:studyabroad_dev@localhost:5432/studyabroad_dev",
}

# Test preset
TEST_PRESET: dict[str, any] = {
    "ENVIRONMENT_MODE": "test",
    "ENABLE_SUPABASE": True,
    "ENABLE_PAYMENTS": False,
    "LOG_LEVEL": "DEBUG",
    "LOG_PRETTY_PRINT": False,
}

# Production preset
PRODUCTION_PRESET: dict[str, any] = {
    "ENVIRONMENT_MODE": "production",
    "ENABLE_SUPABASE": True,
    "ENABLE_PAYMENTS": True,
    "LOG_LEVEL": "ERROR",
    "LOG_PRETTY_PRINT": False,
    "LOG_CONSOLE_ENABLED": False,
}
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
