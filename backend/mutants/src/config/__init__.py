"""
Configuration Module

Environment-based configuration management with Pydantic validation.
Equivalent to TypeScript @study-abroad/shared-config package.

This module provides:
- EnvironmentConfig: Pydantic model for all configuration
- ConfigLoader: Singleton configuration loader
- Environment presets for dev/test/production

Usage:
    from config import config_loader

    config = config_loader.load()
    print(config.ENVIRONMENT_MODE)
"""

from config.environment import EnvironmentConfig, EnvironmentMode, LogLevel
from config.loader import ConfigLoader, config_loader
from config.presets import DEV_PRESET, TEST_PRESET, PRODUCTION_PRESET

# Backward compatibility: Create a settings object for old code
settings = config_loader.load()

__all__ = [
    "EnvironmentConfig",
    "EnvironmentMode",
    "LogLevel",
    "ConfigLoader",
    "config_loader",
    "DEV_PRESET",
    "TEST_PRESET",
    "PRODUCTION_PRESET",
    "settings",  # Backward compatibility
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
