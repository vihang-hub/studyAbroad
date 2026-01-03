"""
Tests for Configuration Loader

Tests singleton pattern and configuration loading.
"""

import pytest
import os
from config.loader import ConfigLoader


class TestConfigLoader:
    """Test configuration loader"""

    def setup_method(self):
        """Reset loader before each test"""
        ConfigLoader.reset()

    def teardown_method(self):
        """Reset loader after each test"""
        ConfigLoader.reset()

    def test_singleton_pattern(self):
        """Loader returns same instance on multiple calls"""
        # Set minimal required env vars
        os.environ['ENVIRONMENT_MODE'] = 'dev'
        os.environ['DATABASE_URL'] = 'postgresql://localhost/test'
        os.environ['CLERK_PUBLISHABLE_KEY'] = 'test_key'
        os.environ['CLERK_SECRET_KEY'] = 'test_secret'
        os.environ['GEMINI_API_KEY'] = 'test_api_key'

        config1 = ConfigLoader.load()
        config2 = ConfigLoader.load()

        assert config1 is config2

    def test_is_loaded(self):
        """is_loaded() returns correct status"""
        assert ConfigLoader.is_loaded() is False

        os.environ['ENVIRONMENT_MODE'] = 'dev'
        os.environ['DATABASE_URL'] = 'postgresql://localhost/test'
        os.environ['CLERK_PUBLISHABLE_KEY'] = 'test_key'
        os.environ['CLERK_SECRET_KEY'] = 'test_secret'
        os.environ['GEMINI_API_KEY'] = 'test_api_key'

        ConfigLoader.load()
        assert ConfigLoader.is_loaded() is True

    def test_get_before_load_raises(self):
        """get() before load() raises error"""
        with pytest.raises(ValueError, match='Configuration not loaded'):
            ConfigLoader.get('ENVIRONMENT_MODE')

    def test_get_after_load(self):
        """get() returns configuration value after load()"""
        os.environ['ENVIRONMENT_MODE'] = 'dev'
        os.environ['DATABASE_URL'] = 'postgresql://localhost/test'
        os.environ['CLERK_PUBLISHABLE_KEY'] = 'test_key'
        os.environ['CLERK_SECRET_KEY'] = 'test_secret'
        os.environ['GEMINI_API_KEY'] = 'test_api_key'

        ConfigLoader.load()
        assert ConfigLoader.get('ENVIRONMENT_MODE') == 'dev'

    def test_reload_clears_instance(self):
        """reload() clears cached instance"""
        os.environ['ENVIRONMENT_MODE'] = 'dev'
        os.environ['DATABASE_URL'] = 'postgresql://localhost/test'
        os.environ['CLERK_PUBLISHABLE_KEY'] = 'test_key'
        os.environ['CLERK_SECRET_KEY'] = 'test_secret'
        os.environ['GEMINI_API_KEY'] = 'test_api_key'

        config1 = ConfigLoader.load()
        ConfigLoader.reload()
        assert ConfigLoader.is_loaded() is False

        config2 = ConfigLoader.load()
        # After reload, new instance is created
        assert config1 is not config2

    def test_reset_alias_for_reload(self):
        """reset() is alias for reload()"""
        os.environ['ENVIRONMENT_MODE'] = 'dev'
        os.environ['DATABASE_URL'] = 'postgresql://localhost/test'
        os.environ['CLERK_PUBLISHABLE_KEY'] = 'test_key'
        os.environ['CLERK_SECRET_KEY'] = 'test_secret'
        os.environ['GEMINI_API_KEY'] = 'test_api_key'

        ConfigLoader.load()
        assert ConfigLoader.is_loaded() is True

        ConfigLoader.reset()
        assert ConfigLoader.is_loaded() is False
