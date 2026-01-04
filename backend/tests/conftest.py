"""
pytest configuration and fixtures for backend tests
"""
import pytest
import os
from typing import Generator
from fastapi.testclient import TestClient
from unittest.mock import Mock, MagicMock
from src.main import app


@pytest.fixture(scope='function', autouse=True)
def clean_environment() -> Generator[None, None, None]:
    """
    Clean environment variables before and after each test

    This ensures tests don't interfere with each other through
    shared environment state.
    """
    # Store original environment
    original_env = dict(os.environ)

    # Clear test-related env vars
    test_vars = [
        'ENVIRONMENT_MODE',
        'ENABLE_SUPABASE',
        'ENABLE_PAYMENTS',
        'DATABASE_URL',
        'SUPABASE_URL',
        'SUPABASE_ANON_KEY',
        'SUPABASE_SERVICE_ROLE_KEY',
        'CLERK_PUBLISHABLE_KEY',
        'CLERK_SECRET_KEY',
        'GEMINI_API_KEY',
        'STRIPE_PUBLISHABLE_KEY',
        'STRIPE_SECRET_KEY',
        'STRIPE_WEBHOOK_SECRET',
        'LOG_LEVEL',
    ]

    for var in test_vars:
        os.environ.pop(var, None)

    yield

    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def dev_env_config():
    """Development environment configuration fixture"""
    return {
        'ENVIRONMENT_MODE': 'dev',
        'ENABLE_SUPABASE': False,
        'ENABLE_PAYMENTS': False,
        'DATABASE_URL': 'postgresql://localhost:5432/studyabroad_test',
        'CLERK_PUBLISHABLE_KEY': 'pk_test_dev',
        'CLERK_SECRET_KEY': 'sk_test_dev',
        'GEMINI_API_KEY': 'test_gemini_key',
        'LOG_LEVEL': 'DEBUG',
    }


@pytest.fixture
def test_env_config():
    """Test environment configuration fixture"""
    return {
        'ENVIRONMENT_MODE': 'test',
        'ENABLE_SUPABASE': True,
        'ENABLE_PAYMENTS': False,
        'DATABASE_URL': 'postgresql://localhost:5432/studyabroad_test',
        'SUPABASE_URL': 'https://test.supabase.co',
        'SUPABASE_ANON_KEY': 'test_anon_key',
        'SUPABASE_SERVICE_ROLE_KEY': 'test_service_role_key',
        'CLERK_PUBLISHABLE_KEY': 'pk_test_test',
        'CLERK_SECRET_KEY': 'sk_test_test',
        'GEMINI_API_KEY': 'test_gemini_key',
        'LOG_LEVEL': 'DEBUG',
    }


@pytest.fixture
def production_env_config():
    """Production environment configuration fixture"""
    return {
        'ENVIRONMENT_MODE': 'production',
        'ENABLE_SUPABASE': True,
        'ENABLE_PAYMENTS': True,
        'DATABASE_URL': 'postgresql://localhost:5432/studyabroad_test',
        'SUPABASE_URL': 'https://prod.supabase.co',
        'SUPABASE_ANON_KEY': 'prod_anon_key',
        'SUPABASE_SERVICE_ROLE_KEY': 'prod_service_role_key',
        'CLERK_PUBLISHABLE_KEY': 'pk_live_prod',
        'CLERK_SECRET_KEY': 'sk_live_prod',
        'GEMINI_API_KEY': 'prod_gemini_key',
        'STRIPE_PUBLISHABLE_KEY': 'pk_live_prod',
        'STRIPE_SECRET_KEY': 'sk_live_prod',
        'STRIPE_WEBHOOK_SECRET': 'whsec_prod',
        'LOG_LEVEL': 'ERROR',
    }


@pytest.fixture
def client() -> Generator:
    """
    Create a FastAPI test client
    """
    with TestClient(app) as c:
        yield c


@pytest.fixture
def mock_supabase():
    """
    Mock Supabase client for testing
    """
    mock = MagicMock()
    mock.table.return_value = mock
    mock.insert.return_value = mock
    mock.update.return_value = mock
    mock.select.return_value = mock
    mock.eq.return_value = mock
    mock.is_.return_value = mock
    mock.order.return_value = mock
    mock.limit.return_value = mock
    mock.execute.return_value = Mock(data=[])
    return mock


@pytest.fixture
def mock_stripe():
    """
    Mock Stripe client for testing
    """
    mock = MagicMock()
    return mock


@pytest.fixture
def mock_clerk_token():
    """
    Mock Clerk JWT token for testing
    """
    return "mock_clerk_token_12345"


@pytest.fixture
def mock_user_id():
    """
    Mock user ID for testing
    """
    return "user_test_12345"


@pytest.fixture
def mock_report_id():
    """
    Mock report ID for testing
    """
    return "report_test_12345"


@pytest.fixture
def sample_report_data():
    """
    Sample report data for testing
    """
    return {
        "id": "report_test_12345",
        "user_id": "user_test_12345",
        "query": "Studying Computer Science in UK universities",
        "status": "pending",
        "content": None,
        "error": None,
        "expires_at": "2025-01-28T12:00:00Z",
        "created_at": "2024-12-29T12:00:00Z",
        "updated_at": "2024-12-29T12:00:00Z",
        "deleted_at": None,
    }


@pytest.fixture
def sample_payment_data():
    """
    Sample payment data for testing
    """
    return {
        "id": "payment_test_12345",
        "user_id": "user_test_12345",
        "report_id": "report_test_12345",
        "stripe_payment_intent_id": "pi_test_12345",
        "amount": 299,
        "currency": "gbp",
        "status": "pending",
        "created_at": "2024-12-29T12:00:00Z",
        "updated_at": "2024-12-29T12:00:00Z",
    }


@pytest.fixture
def sample_uk_query():
    """
    Sample UK-specific query for testing
    """
    return "What are the best UK universities for Computer Science?"


@pytest.fixture
def sample_non_uk_query():
    """
    Sample non-UK query for testing (should be rejected)
    """
    return "What are the best universities in USA for Computer Science?"


@pytest.fixture
def test_client():
    """
    Fixture for FastAPI TestClient
    """
    return TestClient(app)


@pytest.fixture
def mock_clerk_user():
    """
    Mock authenticated Clerk user data
    """
    return {
        "id": "user_test_clerk_123",
        "email": "test@example.com",
        "email_addresses": [{"email_address": "test@example.com"}],
        "external_accounts": [],
        "created_at": 1704067200000,  # 2024-01-01
    }


@pytest.fixture
def mock_gemini():
    """
    Mock Gemini AI client for testing report generation
    """
    mock = MagicMock()
    mock.generate_content = MagicMock()
    return mock


@pytest.fixture
def mock_db_adapter():
    """
    Mock DatabaseAdapter for testing
    """
    mock = MagicMock()
    return mock


@pytest.fixture
def set_cron_secret():
    """
    Set CRON_SECRET environment variable for testing
    """
    os.environ['CRON_SECRET'] = 'test_cron_secret'
    yield 'test_cron_secret'
    os.environ.pop('CRON_SECRET', None)


@pytest.fixture
def authenticated_client(mock_user_id) -> Generator:
    """
    Create a FastAPI test client with mocked authentication.

    This overrides the get_current_user_id dependency to return a mock user ID
    without requiring actual JWT verification.
    """
    # Use same import path as the routes to ensure it's the same function object
    from api.services.auth_service import get_current_user_id

    async def override_get_current_user_id():
        return mock_user_id

    app.dependency_overrides[get_current_user_id] = override_get_current_user_id

    with TestClient(app) as c:
        yield c

    # Clean up the override
    app.dependency_overrides.pop(get_current_user_id, None)


@pytest.fixture
def payment_enabled_client() -> Generator:
    """
    Create a test client with payments feature flag enabled.

    This overrides the get_feature_flags dependency to return a mock
    FeatureFlagEvaluator that always returns True for is_enabled().
    """
    from dependencies import get_feature_flags
    from feature_flags.evaluator import FeatureFlagEvaluator

    mock_feature_flags = MagicMock(spec=FeatureFlagEvaluator)
    mock_feature_flags.is_enabled.return_value = True

    def override_get_feature_flags():
        return mock_feature_flags

    app.dependency_overrides[get_feature_flags] = override_get_feature_flags

    with TestClient(app) as c:
        yield c

    # Clean up the override
    app.dependency_overrides.pop(get_feature_flags, None)
