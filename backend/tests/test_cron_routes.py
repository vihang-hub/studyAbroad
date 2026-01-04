"""
Tests for Cron Routes

Tests the scheduled job endpoints for data retention and cleanup.
"""
import pytest
from typing import Generator
from unittest.mock import patch, MagicMock, AsyncMock
from fastapi.testclient import TestClient
from src.main import app


@pytest.fixture
def cron_authenticated_client() -> Generator:
    """
    Create a test client with cron secret verification bypassed.
    Uses dependency override to skip cron secret validation.
    """
    from src.api.routes.cron import verify_cron_secret

    def override_verify_cron_secret():
        return None  # Bypass verification

    app.dependency_overrides[verify_cron_secret] = override_verify_cron_secret

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.pop(verify_cron_secret, None)


class TestCronSecretVerification:
    """Test suite for cron secret verification"""

    def test_expire_reports_missing_secret_header(self, client):
        """Test POST /cron/expire-reports requires X-Cron-Secret header"""
        response = client.post("/cron/expire-reports")
        assert response.status_code == 422  # Missing required header

    def test_expire_reports_invalid_secret(self, client):
        """Test POST /cron/expire-reports rejects invalid secret"""
        with patch("src.api.routes.cron.settings") as mock_settings:
            mock_settings.CRON_SECRET = "correct_secret"

            response = client.post(
                "/cron/expire-reports",
                headers={"X-Cron-Secret": "wrong_secret"},
            )
            assert response.status_code == 401
            assert "Invalid cron secret" in response.json()["detail"]

    def test_delete_expired_reports_missing_secret_header(self, client):
        """Test POST /cron/delete-expired-reports requires X-Cron-Secret header"""
        response = client.post("/cron/delete-expired-reports")
        assert response.status_code == 422  # Missing required header

    def test_delete_expired_reports_invalid_secret(self, client):
        """Test POST /cron/delete-expired-reports rejects invalid secret"""
        with patch("src.api.routes.cron.settings") as mock_settings:
            mock_settings.CRON_SECRET = "correct_secret"

            response = client.post(
                "/cron/delete-expired-reports",
                headers={"X-Cron-Secret": "wrong_secret"},
            )
            assert response.status_code == 401


class TestExpireReportsEndpoint:
    """Test suite for /cron/expire-reports endpoint"""

    def test_expire_reports_success(self, cron_authenticated_client):
        """Test POST /cron/expire-reports with valid secret and successful expiry"""
        with patch("src.api.routes.cron.ReportRepository") as mock_repo_class:
            mock_repo = MagicMock()
            mock_repo.expire_old_reports = AsyncMock(return_value=5)
            mock_repo_class.return_value = mock_repo

            response = cron_authenticated_client.post(
                "/cron/expire-reports",
                headers={"X-Cron-Secret": "test_secret"},
            )

            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["expired_count"] == 5
            assert "correlation_id" in data

    def test_expire_reports_zero_expired(self, cron_authenticated_client):
        """Test POST /cron/expire-reports when no reports need expiry"""
        with patch("src.api.routes.cron.ReportRepository") as mock_repo_class:
            mock_repo = MagicMock()
            mock_repo.expire_old_reports = AsyncMock(return_value=0)
            mock_repo_class.return_value = mock_repo

            response = cron_authenticated_client.post(
                "/cron/expire-reports",
                headers={"X-Cron-Secret": "test_secret"},
            )

            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["expired_count"] == 0

    def test_expire_reports_database_error(self, cron_authenticated_client):
        """Test POST /cron/expire-reports handles database errors"""
        with patch("src.api.routes.cron.ReportRepository") as mock_repo_class:
            mock_repo = MagicMock()
            mock_repo.expire_old_reports = AsyncMock(side_effect=Exception("Database connection error"))
            mock_repo_class.return_value = mock_repo

            response = cron_authenticated_client.post(
                "/cron/expire-reports",
                headers={"X-Cron-Secret": "test_secret"},
            )

            assert response.status_code == 500
            assert "Failed to expire reports" in response.json()["detail"]


class TestDeleteExpiredReportsEndpoint:
    """Test suite for /cron/delete-expired-reports endpoint"""

    def test_delete_expired_reports_success(self, cron_authenticated_client):
        """Test POST /cron/delete-expired-reports with valid secret and successful deletion"""
        with patch("src.api.routes.cron.ReportRepository") as mock_repo_class:
            mock_repo = MagicMock()
            mock_repo.delete_expired_reports = AsyncMock(return_value=3)
            mock_repo_class.return_value = mock_repo

            response = cron_authenticated_client.post(
                "/cron/delete-expired-reports",
                headers={"X-Cron-Secret": "test_secret"},
            )

            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["deleted_count"] == 3
            assert "correlation_id" in data

    def test_delete_expired_reports_zero_deleted(self, cron_authenticated_client):
        """Test POST /cron/delete-expired-reports when no reports need deletion"""
        with patch("src.api.routes.cron.ReportRepository") as mock_repo_class:
            mock_repo = MagicMock()
            mock_repo.delete_expired_reports = AsyncMock(return_value=0)
            mock_repo_class.return_value = mock_repo

            response = cron_authenticated_client.post(
                "/cron/delete-expired-reports",
                headers={"X-Cron-Secret": "test_secret"},
            )

            assert response.status_code == 200
            data = response.json()
            assert data["success"] is True
            assert data["deleted_count"] == 0

    def test_delete_expired_reports_database_error(self, cron_authenticated_client):
        """Test POST /cron/delete-expired-reports handles database errors"""
        with patch("src.api.routes.cron.ReportRepository") as mock_repo_class:
            mock_repo = MagicMock()
            mock_repo.delete_expired_reports = AsyncMock(side_effect=Exception("Database connection error"))
            mock_repo_class.return_value = mock_repo

            response = cron_authenticated_client.post(
                "/cron/delete-expired-reports",
                headers={"X-Cron-Secret": "test_secret"},
            )

            assert response.status_code == 500
            assert "Failed to delete expired reports" in response.json()["detail"]
