"""
Tests for Feature Flag Evaluator

Tests feature flag evaluation logic.
"""

import pytest
import os
from config.loader import ConfigLoader
from feature_flags import FeatureFlagEvaluator, Feature


class TestFeatureFlagEvaluator:
    """Test feature flag evaluator"""

    def setup_method(self):
        """Reset config before each test"""
        ConfigLoader.reset()

    def teardown_method(self):
        """Reset config after each test"""
        ConfigLoader.reset()

    def _setup_env(self, enable_supabase=False, enable_payments=False):
        """Helper to setup environment"""
        os.environ['ENVIRONMENT_MODE'] = 'dev' if not enable_supabase else 'test'
        os.environ['ENABLE_SUPABASE'] = str(enable_supabase).lower()
        os.environ['ENABLE_PAYMENTS'] = str(enable_payments).lower()
        os.environ['DATABASE_URL'] = 'postgresql://localhost/test'
        os.environ['CLERK_PUBLISHABLE_KEY'] = 'test_key'
        os.environ['CLERK_SECRET_KEY'] = 'test_secret'
        os.environ['GEMINI_API_KEY'] = 'test_api_key'

        if enable_supabase:
            os.environ['SUPABASE_URL'] = 'https://test.supabase.co'
            os.environ['SUPABASE_ANON_KEY'] = 'test_anon_key'

    def test_is_enabled_returns_true_when_enabled(self):
        """is_enabled() returns True for enabled feature"""
        self._setup_env(enable_supabase=True)
        evaluator = FeatureFlagEvaluator()

        assert evaluator.is_enabled(Feature.SUPABASE) is True

    def test_is_enabled_returns_false_when_disabled(self):
        """is_enabled() returns False for disabled feature"""
        self._setup_env(enable_supabase=False)
        evaluator = FeatureFlagEvaluator()

        assert evaluator.is_enabled(Feature.SUPABASE) is False

    def test_require_enabled_succeeds_when_enabled(self):
        """require_enabled() succeeds for enabled feature"""
        self._setup_env(enable_supabase=True)
        evaluator = FeatureFlagEvaluator()

        # Should not raise
        evaluator.require_enabled(Feature.SUPABASE)

    def test_require_enabled_raises_when_disabled(self):
        """require_enabled() raises for disabled feature"""
        self._setup_env(enable_supabase=False)
        evaluator = FeatureFlagEvaluator()

        with pytest.raises(ValueError, match='Feature ENABLE_SUPABASE is required'):
            evaluator.require_enabled(Feature.SUPABASE)

    def test_get_all_flags(self):
        """get_all_flags() returns all feature flags"""
        self._setup_env(enable_supabase=True, enable_payments=False)
        evaluator = FeatureFlagEvaluator()

        flags = evaluator.get_all_flags()

        assert flags[Feature.SUPABASE.value] is True
        assert flags[Feature.PAYMENTS.value] is False
        assert Feature.RATE_LIMITING.value in flags
        assert Feature.OBSERVABILITY.value in flags

    def test_multiple_features_independent(self):
        """Multiple features can have different states"""
        self._setup_env(enable_supabase=True, enable_payments=False)
        evaluator = FeatureFlagEvaluator()

        assert evaluator.is_enabled(Feature.SUPABASE) is True
        assert evaluator.is_enabled(Feature.PAYMENTS) is False
