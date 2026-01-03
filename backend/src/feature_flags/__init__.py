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
