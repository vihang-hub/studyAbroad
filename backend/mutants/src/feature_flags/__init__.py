"""
Feature Flags Module

Environment-based feature flag evaluation.
Equivalent to TypeScript @study-abroad/shared-feature-flags package.

This module provides:
- Feature: Enum of available feature flags
- FeatureFlagEvaluator: Feature flag evaluation logic
- feature_flags: Singleton evaluator instance

Usage:
    from feature_flags import feature_flags, Feature

    if feature_flags.is_enabled(Feature.SUPABASE):
        # Use Supabase
        pass

    feature_flags.require_enabled(Feature.PAYMENTS)  # Raises if disabled
"""

from feature_flags.types import Feature
from feature_flags.evaluator import FeatureFlagEvaluator, feature_flags

__all__ = ["Feature", "FeatureFlagEvaluator", "feature_flags"]
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
