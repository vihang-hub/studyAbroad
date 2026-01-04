"""
Tests for Environment Configuration

Tests Pydantic validation rules and environment-specific requirements.
"""

import os
import pytest
from pydantic import ValidationError
from config.environment import EnvironmentConfig


@pytest.fixture
def clean_env(monkeypatch):
    """Clear environment variables that might interfere with tests

    Note: Since Pydantic BaseSettings reads from .env file, we also need
    to prevent file-based loading by removing the env_file path temporarily.
    """
    # Clear environment variables
    env_vars_to_clear = [
        'SUPABASE_URL', 'SUPABASE_ANON_KEY', 'SUPABASE_SERVICE_ROLE_KEY',
        'LOG_LEVEL', 'ENVIRONMENT_MODE', 'STRIPE_PUBLISHABLE_KEY',
        'STRIPE_SECRET_KEY', 'STRIPE_WEBHOOK_SECRET', 'STRIPE_PRICE_ID',
    ]
    for var in env_vars_to_clear:
        monkeypatch.delenv(var, raising=False)

    # Patch the model_config to disable BOTH env and dotenv loading
    @classmethod
    def no_external_settings(cls, settings_cls, init_settings, env_settings, dotenv_settings, file_secret_settings):
        # Only use init_settings (values passed directly to constructor)
        return (init_settings,)

    monkeypatch.setattr(EnvironmentConfig, 'settings_customise_sources', no_external_settings)
    yield


class TestEnvironmentConfig:
    """Test environment configuration validation"""

    def test_dev_mode_requirements(self):
        """Dev mode must disable Supabase and payments"""
        config_data = {
            'ENVIRONMENT_MODE': 'dev',
            'ENABLE_SUPABASE': False,
            'ENABLE_PAYMENTS': False,
            'DATABASE_URL': 'postgresql://localhost/test',
            'CLERK_PUBLISHABLE_KEY': 'test_key',
            'CLERK_SECRET_KEY': 'test_secret',
            'GEMINI_API_KEY': 'test_api_key',
        }

        config = EnvironmentConfig(**config_data)
        assert config.ENVIRONMENT_MODE == 'dev'
        assert config.ENABLE_SUPABASE is False
        assert config.ENABLE_PAYMENTS is False

    def test_dev_mode_rejects_supabase_enabled(self):
        """Dev mode fails if Supabase is enabled"""
        config_data = {
            'ENVIRONMENT_MODE': 'dev',
            'ENABLE_SUPABASE': True,  # Invalid for dev mode
            'ENABLE_PAYMENTS': False,
            'DATABASE_URL': 'postgresql://localhost/test',
            'CLERK_PUBLISHABLE_KEY': 'test_key',
            'CLERK_SECRET_KEY': 'test_secret',
            'GEMINI_API_KEY': 'test_api_key',
        }

        with pytest.raises(ValidationError) as exc_info:
            EnvironmentConfig(**config_data)

        assert 'Dev mode requires ENABLE_SUPABASE=false' in str(exc_info.value)

    def test_production_mode_requirements(self):
        """Production mode must enable Supabase and payments"""
        config_data = {
            'ENVIRONMENT_MODE': 'production',
            'ENABLE_SUPABASE': True,
            'ENABLE_PAYMENTS': True,
            'DATABASE_URL': 'postgresql://localhost/test',
            'SUPABASE_URL': 'https://test.supabase.co',
            'SUPABASE_ANON_KEY': 'test_anon_key',
            'CLERK_PUBLISHABLE_KEY': 'test_key',
            'CLERK_SECRET_KEY': 'test_secret',
            'GEMINI_API_KEY': 'test_api_key',
            'STRIPE_PUBLISHABLE_KEY': 'pk_test_xxx',
            'STRIPE_SECRET_KEY': 'sk_test_xxx',
            'STRIPE_WEBHOOK_SECRET': 'whsec_xxx',
        }

        config = EnvironmentConfig(**config_data)
        assert config.ENVIRONMENT_MODE == 'production'
        assert config.ENABLE_SUPABASE is True
        assert config.ENABLE_PAYMENTS is True

    def test_production_mode_rejects_disabled_payments(self):
        """Production mode fails if payments disabled"""
        config_data = {
            'ENVIRONMENT_MODE': 'production',
            'ENABLE_SUPABASE': True,
            'ENABLE_PAYMENTS': False,  # Invalid for production
            'DATABASE_URL': 'postgresql://localhost/test',
            'SUPABASE_URL': 'https://test.supabase.co',
            'SUPABASE_ANON_KEY': 'test_anon_key',
            'CLERK_PUBLISHABLE_KEY': 'test_key',
            'CLERK_SECRET_KEY': 'test_secret',
            'GEMINI_API_KEY': 'test_api_key',
        }

        with pytest.raises(ValidationError) as exc_info:
            EnvironmentConfig(**config_data)

        assert 'Production mode requires' in str(exc_info.value)

    def test_test_mode_requirements(self):
        """Test mode must enable Supabase but disable payments"""
        config_data = {
            'ENVIRONMENT_MODE': 'test',
            'ENABLE_SUPABASE': True,
            'ENABLE_PAYMENTS': False,
            'DATABASE_URL': 'postgresql://localhost/test',
            'SUPABASE_URL': 'https://test.supabase.co',
            'SUPABASE_ANON_KEY': 'test_anon_key',
            'CLERK_PUBLISHABLE_KEY': 'test_key',
            'CLERK_SECRET_KEY': 'test_secret',
            'GEMINI_API_KEY': 'test_api_key',
        }

        config = EnvironmentConfig(**config_data)
        assert config.ENVIRONMENT_MODE == 'test'
        assert config.ENABLE_SUPABASE is True
        assert config.ENABLE_PAYMENTS is False

    def test_supabase_requires_credentials(self, clean_env):
        """Enabling Supabase requires URL and anon key"""
        config_data = {
            'ENVIRONMENT_MODE': 'test',
            'ENABLE_SUPABASE': True,
            'ENABLE_PAYMENTS': False,
            'DATABASE_URL': 'postgresql://localhost/test',
            # Missing SUPABASE_URL and SUPABASE_ANON_KEY
            'CLERK_PUBLISHABLE_KEY': 'test_key',
            'CLERK_SECRET_KEY': 'test_secret',
            'GEMINI_API_KEY': 'test_api_key',
        }

        with pytest.raises(ValidationError) as exc_info:
            EnvironmentConfig(**config_data)

        assert 'SUPABASE_URL and SUPABASE_ANON_KEY are required' in str(exc_info.value)

    def test_payments_requires_stripe_credentials(self):
        """Enabling payments requires Stripe keys"""
        config_data = {
            'ENVIRONMENT_MODE': 'production',
            'ENABLE_SUPABASE': True,
            'ENABLE_PAYMENTS': True,
            'DATABASE_URL': 'postgresql://localhost/test',
            'SUPABASE_URL': 'https://test.supabase.co',
            'SUPABASE_ANON_KEY': 'test_anon_key',
            # Missing Stripe keys
            'CLERK_PUBLISHABLE_KEY': 'test_key',
            'CLERK_SECRET_KEY': 'test_secret',
            'GEMINI_API_KEY': 'test_api_key',
        }

        with pytest.raises(ValidationError) as exc_info:
            EnvironmentConfig(**config_data)

        assert 'STRIPE' in str(exc_info.value)

    def test_log_level_defaults_to_debug_for_dev(self):
        """Dev mode defaults LOG_LEVEL to DEBUG if not set"""
        config_data = {
            'ENVIRONMENT_MODE': 'dev',
            'ENABLE_SUPABASE': False,
            'ENABLE_PAYMENTS': False,
            'DATABASE_URL': 'postgresql://localhost/test',
            'CLERK_PUBLISHABLE_KEY': 'test_key',
            'CLERK_SECRET_KEY': 'test_secret',
            'GEMINI_API_KEY': 'test_api_key',
            # LOG_LEVEL not set
        }

        config = EnvironmentConfig(**config_data)
        assert config.LOG_LEVEL == 'DEBUG'

    def test_log_level_defaults_to_error_for_production(self, clean_env):
        """Production mode defaults LOG_LEVEL to ERROR if not set"""
        config_data = {
            'ENVIRONMENT_MODE': 'production',
            'ENABLE_SUPABASE': True,
            'ENABLE_PAYMENTS': True,
            'DATABASE_URL': 'postgresql://localhost/test',
            'SUPABASE_URL': 'https://test.supabase.co',
            'SUPABASE_ANON_KEY': 'test_anon_key',
            'CLERK_PUBLISHABLE_KEY': 'test_key',
            'CLERK_SECRET_KEY': 'test_secret',
            'GEMINI_API_KEY': 'test_api_key',
            'STRIPE_PUBLISHABLE_KEY': 'pk_test_xxx',
            'STRIPE_SECRET_KEY': 'sk_test_xxx',
            'STRIPE_WEBHOOK_SECRET': 'whsec_xxx',
            # LOG_LEVEL not set
        }

        config = EnvironmentConfig(**config_data)
        assert config.LOG_LEVEL == 'ERROR'

    def test_payment_amount_must_be_299(self):
        """Payment amount must be exactly £2.99"""
        config_data = {
            'ENVIRONMENT_MODE': 'dev',
            'ENABLE_SUPABASE': False,
            'ENABLE_PAYMENTS': False,
            'DATABASE_URL': 'postgresql://localhost/test',
            'CLERK_PUBLISHABLE_KEY': 'test_key',
            'CLERK_SECRET_KEY': 'test_secret',
            'GEMINI_API_KEY': 'test_api_key',
            'PAYMENT_AMOUNT': 3.99,  # Invalid
        }

        with pytest.raises(ValidationError):
            EnvironmentConfig(**config_data)
