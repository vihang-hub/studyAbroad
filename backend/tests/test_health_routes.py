"""
Tests for Health Check Routes

Tests for comprehensive health check endpoint and helper functions.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient

from src.main import app
from src.api.routes.health import (
    check_database_health,
    check_ai_health,
    check_payments_health,
    ServiceStatus,
)


class TestCheckDatabaseHealth:
    """Test suite for check_database_health function"""

    @pytest.mark.asyncio
    async def test_database_healthy(self):
        """Test database health check returns up when connected"""
        mock_db = MagicMock()

        result = await check_database_health(mock_db)

        assert result.status == "up"
        assert result.message == "Database connected"
        assert result.response_time_ms is not None



class TestCheckAIHealth:
    """Test suite for check_ai_health function"""

    @pytest.mark.asyncio
    async def test_ai_healthy(self):
        """Test AI health check returns up when configured"""
        mock_config = MagicMock()
        mock_config.GEMINI_API_KEY = "test-api-key"

        result = await check_ai_health(mock_config)

        assert result.status == "up"
        assert result.message == "Gemini API configured"

    @pytest.mark.asyncio
    async def test_ai_no_api_key(self):
        """Test AI health check returns down when API key not configured"""
        mock_config = MagicMock()
        mock_config.GEMINI_API_KEY = None

        result = await check_ai_health(mock_config)

        assert result.status == "down"
        assert "not configured" in result.message

    @pytest.mark.asyncio
    async def test_ai_empty_api_key(self):
        """Test AI health check returns down when API key is empty"""
        mock_config = MagicMock()
        mock_config.GEMINI_API_KEY = ""

        result = await check_ai_health(mock_config)

        assert result.status == "down"
        assert "not configured" in result.message

    @pytest.mark.asyncio
    async def test_ai_error(self):
        """Test AI health check returns down on error"""
        mock_config = MagicMock()
        # Make GEMINI_API_KEY access raise an exception
        type(mock_config).GEMINI_API_KEY = property(lambda s: (_ for _ in ()).throw(Exception("Config error")))

        result = await check_ai_health(mock_config)

        assert result.status == "down"
        assert "error" in result.message.lower()


class TestCheckPaymentsHealth:
    """Test suite for check_payments_health function"""

    @pytest.mark.asyncio
    async def test_payments_healthy(self):
        """Test payments health check returns up when configured"""
        mock_config = MagicMock()
        mock_config.STRIPE_SECRET_KEY = "sk_test_123"
        mock_config.STRIPE_PUBLISHABLE_KEY = "pk_test_123"

        mock_feature_flags = MagicMock()
        mock_feature_flags.is_enabled.return_value = True

        result = await check_payments_health(mock_config, mock_feature_flags)

        assert result.status == "up"
        assert result.message == "Stripe configured"

    @pytest.mark.asyncio
    async def test_payments_disabled(self):
        """Test payments health check returns disabled when feature flag off"""
        mock_config = MagicMock()
        mock_feature_flags = MagicMock()
        mock_feature_flags.is_enabled.return_value = False

        result = await check_payments_health(mock_config, mock_feature_flags)

        assert result.status == "disabled"
        assert "disabled" in result.message.lower()

    @pytest.mark.asyncio
    async def test_payments_no_secret_key(self):
        """Test payments health check returns down when Stripe secret key not configured"""
        mock_config = MagicMock()
        mock_config.STRIPE_SECRET_KEY = None
        mock_config.STRIPE_PUBLISHABLE_KEY = "pk_test_123"

        mock_feature_flags = MagicMock()
        mock_feature_flags.is_enabled.return_value = True

        result = await check_payments_health(mock_config, mock_feature_flags)

        assert result.status == "down"
        assert "not configured" in result.message

    @pytest.mark.asyncio
    async def test_payments_no_publishable_key(self):
        """Test payments health check returns down when Stripe publishable key not configured"""
        mock_config = MagicMock()
        mock_config.STRIPE_SECRET_KEY = "sk_test_123"
        mock_config.STRIPE_PUBLISHABLE_KEY = None

        mock_feature_flags = MagicMock()
        mock_feature_flags.is_enabled.return_value = True

        result = await check_payments_health(mock_config, mock_feature_flags)

        assert result.status == "down"
        assert "not configured" in result.message

    @pytest.mark.asyncio
    async def test_payments_error(self):
        """Test payments health check returns down on error"""
        mock_config = MagicMock()
        mock_feature_flags = MagicMock()
        mock_feature_flags.is_enabled.side_effect = Exception("Feature flag error")

        result = await check_payments_health(mock_config, mock_feature_flags)

        assert result.status == "down"
        assert "error" in result.message.lower()


class TestHealthEndpoint:
    """Test suite for /health endpoint"""

    def test_health_endpoint_healthy(self, client):
        """Test health endpoint returns healthy status when all services up"""
        with patch("src.api.routes.health.get_db") as mock_get_db, \
             patch("src.api.routes.health.check_database_health") as mock_db_health, \
             patch("src.api.routes.health.check_ai_health") as mock_ai_health, \
             patch("src.api.routes.health.check_payments_health") as mock_payments_health:

            mock_db = MagicMock()
            mock_get_db.return_value = mock_db

            mock_db_health.return_value = ServiceStatus(status="up", message="OK")
            mock_ai_health.return_value = ServiceStatus(status="up", message="OK")
            mock_payments_health.return_value = ServiceStatus(status="up", message="OK")

            response = client.get("/health")

            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert "timestamp" in data
            assert "version" in data
            assert "services" in data

    def test_health_endpoint_degraded_payments_down(self, client):
        """Test health endpoint returns degraded when payments down but others up"""
        with patch("src.api.routes.health.get_db") as mock_get_db, \
             patch("src.api.routes.health.check_database_health") as mock_db_health, \
             patch("src.api.routes.health.check_ai_health") as mock_ai_health, \
             patch("src.api.routes.health.check_payments_health") as mock_payments_health:

            mock_db = MagicMock()
            mock_get_db.return_value = mock_db

            mock_db_health.return_value = ServiceStatus(status="up", message="OK")
            mock_ai_health.return_value = ServiceStatus(status="up", message="OK")
            mock_payments_health.return_value = ServiceStatus(status="down", message="Not configured")

            response = client.get("/health")

            assert response.status_code == 200
            data = response.json()
            # Payments is not critical, so it should be degraded, not unhealthy
            assert data["status"] == "degraded"

    def test_health_endpoint_unhealthy_database_down(self, client):
        """Test health endpoint returns unhealthy when database down"""
        with patch("src.api.routes.health.get_db") as mock_get_db, \
             patch("src.api.routes.health.check_database_health") as mock_db_health, \
             patch("src.api.routes.health.check_ai_health") as mock_ai_health, \
             patch("src.api.routes.health.check_payments_health") as mock_payments_health:

            mock_db = MagicMock()
            mock_get_db.return_value = mock_db

            mock_db_health.return_value = ServiceStatus(status="down", message="Connection refused")
            mock_ai_health.return_value = ServiceStatus(status="up", message="OK")
            mock_payments_health.return_value = ServiceStatus(status="up", message="OK")

            response = client.get("/health")

            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "unhealthy"

    def test_health_endpoint_unhealthy_ai_down(self, client):
        """Test health endpoint returns unhealthy when AI service down"""
        with patch("src.api.routes.health.get_db") as mock_get_db, \
             patch("src.api.routes.health.check_database_health") as mock_db_health, \
             patch("src.api.routes.health.check_ai_health") as mock_ai_health, \
             patch("src.api.routes.health.check_payments_health") as mock_payments_health:

            mock_db = MagicMock()
            mock_get_db.return_value = mock_db

            mock_db_health.return_value = ServiceStatus(status="up", message="OK")
            mock_ai_health.return_value = ServiceStatus(status="down", message="API key not configured")
            mock_payments_health.return_value = ServiceStatus(status="up", message="OK")

            response = client.get("/health")

            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "unhealthy"

    def test_health_endpoint_database_not_initialized(self, client):
        """Test health endpoint handles database not initialized"""
        with patch("src.api.routes.health.get_db") as mock_get_db, \
             patch("src.api.routes.health.check_ai_health") as mock_ai_health, \
             patch("src.api.routes.health.check_payments_health") as mock_payments_health:

            mock_get_db.side_effect = Exception("Database not initialized")

            mock_ai_health.return_value = ServiceStatus(status="up", message="OK")
            mock_payments_health.return_value = ServiceStatus(status="up", message="OK")

            response = client.get("/health")

            assert response.status_code == 200
            data = response.json()
            assert data["services"]["database"]["status"] == "down"
            assert "not initialized" in data["services"]["database"]["message"].lower()

    def test_health_endpoint_healthy_with_disabled_payments(self, client):
        """Test health endpoint returns healthy when payments disabled"""
        with patch("src.api.routes.health.get_db") as mock_get_db, \
             patch("src.api.routes.health.check_database_health") as mock_db_health, \
             patch("src.api.routes.health.check_ai_health") as mock_ai_health, \
             patch("src.api.routes.health.check_payments_health") as mock_payments_health:

            mock_db = MagicMock()
            mock_get_db.return_value = mock_db

            mock_db_health.return_value = ServiceStatus(status="up", message="OK")
            mock_ai_health.return_value = ServiceStatus(status="up", message="OK")
            mock_payments_health.return_value = ServiceStatus(status="disabled", message="Payments disabled")

            response = client.get("/health")

            assert response.status_code == 200
            data = response.json()
            # Disabled services don't affect overall health
            assert data["status"] == "healthy"
