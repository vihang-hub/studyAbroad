"""
Integration tests for API endpoints
"""
import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
from src.main import app
from src.api.models.report import ReportStatus


class TestHealthEndpoint:
    """Test suite for health check endpoint"""

    def test_health_check(self, client):
        """Test GET /health returns 200"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestRootEndpoint:
    """Test suite for root endpoint"""

    def test_root_endpoint(self, client):
        """Test GET / returns API information"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data


class TestReportsEndpoints:
    """Test suite for /reports endpoints"""

    def test_initiate_report_unauthorized(self, client):
        """Test POST /reports/initiate requires authentication"""
        response = client.post(
            "/reports/initiate", json={"query": "Test query about UK universities"}
        )
        assert response.status_code == 401  # Missing authorization

    def test_initiate_report_success(self, authenticated_client, sample_uk_query):
        """Test POST /reports/initiate with valid auth"""
        with patch("src.api.routes.reports.create_report") as mock_create, \
             patch("src.api.routes.reports.create_checkout_session") as mock_checkout:

            from src.api.models.report import CreateReportResponse
            from src.api.models.payment import CreateCheckoutResponse

            mock_create.return_value = CreateReportResponse(
                report_id="report_12345",
                status=ReportStatus.PENDING,
                estimated_completion_seconds=60,
            )

            mock_checkout.return_value = CreateCheckoutResponse(
                client_secret="secret_12345",
                payment_intent_id="pi_12345",
                amount=299,
                currency="gbp",
            )

            response = authenticated_client.post(
                "/reports/initiate",
                json={"query": sample_uk_query},
            )

            assert response.status_code == 200
            data = response.json()
            assert "report_id" in data
            assert "client_secret" in data
            assert "payment_intent_id" in data

    def test_initiate_report_invalid_query(self, authenticated_client, sample_non_uk_query):
        """Test POST /reports/initiate rejects non-UK queries"""
        with patch("src.api.routes.reports.create_report") as mock_create:
            mock_create.side_effect = ValueError("Query must be UK-related")

            response = authenticated_client.post(
                "/reports/initiate",
                json={"query": sample_non_uk_query},
            )

            assert response.status_code == 400

    def test_get_report_by_id_unauthorized(self, client, mock_report_id):
        """Test GET /reports/{id} requires authentication"""
        response = client.get(f"/reports/{mock_report_id}")
        assert response.status_code == 401

    def test_get_report_by_id_success(self, authenticated_client, mock_report_id, sample_report_data):
        """Test GET /reports/{id} with valid auth"""
        with patch("src.api.routes.reports.get_report") as mock_get:
            from src.api.models.report import Report

            mock_get.return_value = Report(**sample_report_data)

            response = authenticated_client.get(f"/reports/{mock_report_id}")

            assert response.status_code == 200
            data = response.json()
            assert data["id"] == mock_report_id

    def test_get_report_by_id_not_found(self, authenticated_client, mock_report_id):
        """Test GET /reports/{id} returns 404 when not found"""
        with patch("src.api.routes.reports.get_report") as mock_get:
            mock_get.return_value = None

            response = authenticated_client.get(f"/reports/{mock_report_id}")

            assert response.status_code == 404

    def test_list_reports_unauthorized(self, client):
        """Test GET /reports requires authentication"""
        response = client.get("/reports")
        assert response.status_code == 401

    def test_list_reports_success(self, authenticated_client):
        """Test GET /reports returns user's reports"""
        with patch("src.api.routes.reports.list_user_reports") as mock_list:
            from src.api.models.report import ReportListItem
            from datetime import datetime

            mock_list.return_value = [
                ReportListItem(
                    id="report_1",
                    query="Query 1",
                    status=ReportStatus.COMPLETED,
                    created_at=datetime.utcnow(),
                    expires_at=datetime.utcnow(),
                ),
                ReportListItem(
                    id="report_2",
                    query="Query 2",
                    status=ReportStatus.PENDING,
                    created_at=datetime.utcnow(),
                    expires_at=datetime.utcnow(),
                ),
            ]

            response = authenticated_client.get("/reports")

            assert response.status_code == 200
            data = response.json()
            assert len(data) == 2

    def test_delete_report_unauthorized(self, client, mock_report_id):
        """Test DELETE /reports/{id} requires authentication"""
        response = client.delete(f"/reports/{mock_report_id}")
        assert response.status_code == 401

    def test_delete_report_success(self, authenticated_client, mock_report_id):
        """Test DELETE /reports/{id} with valid auth"""
        with patch("src.api.routes.reports.soft_delete_report") as mock_delete:
            mock_delete.return_value = True

            response = authenticated_client.delete(f"/reports/{mock_report_id}")

            assert response.status_code == 200
            data = response.json()
            assert "deleted successfully" in data["message"].lower()

    def test_delete_report_not_found(self, authenticated_client, mock_report_id):
        """Test DELETE /reports/{id} returns 404 when not found"""
        with patch("src.api.routes.reports.soft_delete_report") as mock_delete:
            mock_delete.return_value = False

            response = authenticated_client.delete(f"/reports/{mock_report_id}")

            assert response.status_code == 404


class TestWebhookEndpoints:
    """Test suite for /webhooks endpoints"""

    def test_stripe_webhook_missing_signature(self, payment_enabled_client):
        """Test POST /webhooks/stripe requires signature header"""
        response = payment_enabled_client.post("/webhooks/stripe", content=b"test payload")

        assert response.status_code == 400

    def test_stripe_webhook_invalid_signature(self, payment_enabled_client):
        """Test POST /webhooks/stripe validates signature"""
        with patch("src.api.routes.webhooks.verify_webhook_signature") as mock_verify:
            mock_verify.side_effect = Exception("Invalid signature")

            response = payment_enabled_client.post(
                "/webhooks/stripe",
                content=b"test payload",
                headers={"stripe-signature": "invalid_sig"},
            )

            assert response.status_code == 400

    def test_stripe_webhook_payment_succeeded(self, payment_enabled_client, sample_payment_data):
        """Test POST /webhooks/stripe handles payment_intent.succeeded"""
        with patch("src.api.routes.webhooks.verify_webhook_signature") as mock_verify, \
             patch("src.api.routes.webhooks.update_payment_status") as mock_update, \
             patch("src.api.routes.webhooks.trigger_report_generation") as mock_trigger:

            from api.models.payment import Payment

            mock_verify.return_value = {
                "type": "payment_intent.succeeded",
                "id": "evt_12345",
                "data": {"object": {"id": "pi_12345"}},
            }

            mock_update.return_value = Payment(**sample_payment_data)

            response = payment_enabled_client.post(
                "/webhooks/stripe",
                content=b"test payload",
                headers={"stripe-signature": "valid_sig"},
            )

            assert response.status_code == 200
            mock_trigger.assert_called_once()

    def test_stripe_webhook_payment_failed(self, payment_enabled_client):
        """Test POST /webhooks/stripe handles payment_intent.payment_failed"""
        with patch("src.api.routes.webhooks.verify_webhook_signature") as mock_verify, \
             patch("src.api.routes.webhooks.update_payment_status") as mock_update:

            mock_verify.return_value = {
                "type": "payment_intent.payment_failed",
                "id": "evt_12345",
                "data": {
                    "object": {
                        "id": "pi_12345",
                        "last_payment_error": {"message": "Card declined"},
                    }
                },
            }

            response = payment_enabled_client.post(
                "/webhooks/stripe",
                content=b"test payload",
                headers={"stripe-signature": "valid_sig"},
            )

            assert response.status_code == 200
            mock_update.assert_called_once()

    def test_stripe_webhook_charge_refunded(self, payment_enabled_client):
        """Test POST /webhooks/stripe handles charge.refunded"""
        with patch("src.api.routes.webhooks.verify_webhook_signature") as mock_verify, \
             patch("src.api.routes.webhooks.update_payment_status") as mock_update:

            mock_verify.return_value = {
                "type": "charge.refunded",
                "id": "evt_12345",
                "data": {"object": {"payment_intent": "pi_12345"}},
            }

            response = payment_enabled_client.post(
                "/webhooks/stripe",
                content=b"test payload",
                headers={"stripe-signature": "valid_sig"},
            )

            assert response.status_code == 200
            mock_update.assert_called_once()

    def test_stripe_webhook_unknown_event(self, payment_enabled_client):
        """Test POST /webhooks/stripe ignores unknown events"""
        with patch("src.api.routes.webhooks.verify_webhook_signature") as mock_verify:
            mock_verify.return_value = {
                "type": "unknown.event",
                "id": "evt_12345",
                "data": {"object": {}},
            }

            response = payment_enabled_client.post(
                "/webhooks/stripe",
                content=b"test payload",
                headers={"stripe-signature": "valid_sig"},
            )

            assert response.status_code == 200
