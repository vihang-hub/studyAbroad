"""
Integration tests for Stripe webhook signature verification

Tests security of Stripe webhook endpoint including:
- Valid signature verification
- Invalid signature rejection
- Replay attack prevention
- Malformed payload handling
"""
import pytest
import stripe
import time
import hmac
import hashlib
from fastapi.testclient import TestClient
from src.main import app
from src.config import settings


class TestStripeWebhookSecurity:
    """Test suite for Stripe webhook security"""

    @pytest.fixture
    def client(self):
        """Create test client"""
        return TestClient(app)

    @pytest.fixture
    def webhook_secret(self):
        """Get webhook secret from settings"""
        return settings.STRIPE_WEBHOOK_SECRET

    @pytest.fixture
    def sample_event(self):
        """Sample Stripe event payload"""
        return {
            "id": "evt_test_webhook",
            "type": "checkout.session.completed",
            "data": {
                "object": {
                    "id": "cs_test_123",
                    "payment_status": "paid",
                    "metadata": {
                        "user_id": "user_123",
                        "report_id": "report_456"
                    }
                }
            }
        }

    def generate_signature(
        self,
        payload: str,
        secret: str,
        timestamp: int = None
    ) -> str:
        """
        Generate Stripe webhook signature

        Args:
            payload: JSON payload as string
            secret: Webhook secret
            timestamp: Unix timestamp (defaults to current time)

        Returns:
            Stripe signature header value
        """
        if timestamp is None:
            timestamp = int(time.time())

        # Create signed payload string
        signed_payload = f"{timestamp}.{payload}"

        # Compute HMAC signature
        signature = hmac.new(
            secret.encode('utf-8'),
            signed_payload.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        # Return Stripe signature header format
        return f"t={timestamp},v1={signature}"

    def test_valid_signature_accepted(self, client, webhook_secret, sample_event):
        """
        Test that webhook with valid signature is accepted

        Expected: 200 OK response
        """
        import json

        # Convert event to JSON string
        payload = json.dumps(sample_event)

        # Generate valid signature
        signature = self.generate_signature(payload, webhook_secret)

        # Send webhook request
        response = client.post(
            "/webhooks/stripe",
            content=payload,
            headers={
                "Stripe-Signature": signature,
                "Content-Type": "application/json"
            }
        )

        # Should accept valid signature
        assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"

        # Verify response indicates success
        data = response.json()
        assert "status" in data or "received" in data

    def test_invalid_signature_rejected(self, client, sample_event):
        """
        Test that webhook with invalid signature is rejected

        Expected: 400 Bad Request
        """
        import json

        payload = json.dumps(sample_event)

        # Generate signature with wrong secret
        wrong_secret = "whsec_wrong_secret_123"
        invalid_signature = self.generate_signature(payload, wrong_secret)

        # Send webhook request
        response = client.post(
            "/webhooks/stripe",
            content=payload,
            headers={
                "Stripe-Signature": invalid_signature,
                "Content-Type": "application/json"
            }
        )

        # Should reject invalid signature
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"

        # Verify error message
        data = response.json()
        assert "error" in data or "detail" in data

    def test_missing_signature_rejected(self, client, sample_event):
        """
        Test that webhook without signature is rejected

        Expected: 400 Bad Request
        """
        import json

        payload = json.dumps(sample_event)

        # Send webhook request without signature header
        response = client.post(
            "/webhooks/stripe",
            content=payload,
            headers={
                "Content-Type": "application/json"
            }
        )

        # Should reject missing signature
        assert response.status_code == 400, f"Expected 400, got {response.status_code}"

        data = response.json()
        assert "error" in data or "detail" in data

    def test_malformed_signature_rejected(self, client, sample_event):
        """
        Test that webhook with malformed signature is rejected

        Expected: 400 Bad Request
        """
        import json

        payload = json.dumps(sample_event)

        # Malformed signatures
        malformed_signatures = [
            "invalid",
            "t=,v1=",
            "t=abc,v1=def",
            "v1=signature_only",
            "",
        ]

        for malformed_sig in malformed_signatures:
            response = client.post(
                "/webhooks/stripe",
                content=payload,
                headers={
                    "Stripe-Signature": malformed_sig,
                    "Content-Type": "application/json"
                }
            )

            assert response.status_code == 400, \
                f"Expected 400 for signature '{malformed_sig}', got {response.status_code}"

    def test_replay_attack_prevention(self, client, webhook_secret, sample_event):
        """
        Test that old timestamps are rejected (replay attack prevention)

        Stripe rejects webhooks with timestamps older than 5 minutes.
        Expected: 400 Bad Request
        """
        import json

        payload = json.dumps(sample_event)

        # Generate signature with old timestamp (10 minutes ago)
        old_timestamp = int(time.time()) - 600  # 10 minutes ago
        old_signature = self.generate_signature(payload, webhook_secret, old_timestamp)

        # Send webhook request
        response = client.post(
            "/webhooks/stripe",
            content=payload,
            headers={
                "Stripe-Signature": old_signature,
                "Content-Type": "application/json"
            }
        )

        # Should reject old timestamp
        # Note: This test may fail if the webhook handler doesn't check timestamp
        # Stripe's library handles this automatically
        assert response.status_code in [400, 401], \
            f"Expected 400/401 for old timestamp, got {response.status_code}"

    def test_modified_payload_rejected(self, client, webhook_secret, sample_event):
        """
        Test that modified payload is detected via signature mismatch

        Expected: 400 Bad Request
        """
        import json

        # Generate signature for original payload
        original_payload = json.dumps(sample_event)
        signature = self.generate_signature(original_payload, webhook_secret)

        # Modify payload after signing (tampering attempt)
        modified_event = sample_event.copy()
        modified_event["data"]["object"]["payment_status"] = "unpaid"  # Malicious change
        modified_payload = json.dumps(modified_event)

        # Send modified payload with original signature
        response = client.post(
            "/webhooks/stripe",
            content=modified_payload,
            headers={
                "Stripe-Signature": signature,
                "Content-Type": "application/json"
            }
        )

        # Should reject due to signature mismatch
        assert response.status_code == 400, \
            f"Expected 400 for modified payload, got {response.status_code}"

    def test_multiple_signatures_handling(self, client, webhook_secret, sample_event):
        """
        Test handling of multiple signatures (Stripe sends multiple versions)

        Stripe signature format: t=timestamp,v1=sig1,v1=sig2
        Expected: 200 OK if at least one signature is valid
        """
        import json

        payload = json.dumps(sample_event)
        timestamp = int(time.time())

        # Generate valid signature
        valid_sig = self.generate_signature(payload, webhook_secret, timestamp)

        # Add a second invalid signature
        multi_sig = f"{valid_sig},v1=invalid_signature_abc123"

        # Send webhook request
        response = client.post(
            "/webhooks/stripe",
            content=payload,
            headers={
                "Stripe-Signature": multi_sig,
                "Content-Type": "application/json"
            }
        )

        # Should accept if at least one signature is valid
        # Stripe's library handles this automatically
        assert response.status_code == 200, \
            f"Expected 200 for multi-signature, got {response.status_code}"

    def test_empty_payload_rejected(self, client, webhook_secret):
        """
        Test that empty payload is rejected

        Expected: 400 Bad Request
        """
        payload = ""
        signature = self.generate_signature(payload, webhook_secret)

        response = client.post(
            "/webhooks/stripe",
            content=payload,
            headers={
                "Stripe-Signature": signature,
                "Content-Type": "application/json"
            }
        )

        assert response.status_code in [400, 422], \
            f"Expected 400/422 for empty payload, got {response.status_code}"

    def test_malformed_json_rejected(self, client, webhook_secret):
        """
        Test that malformed JSON is rejected

        Expected: 400 Bad Request
        """
        payload = "{invalid json"
        signature = self.generate_signature(payload, webhook_secret)

        response = client.post(
            "/webhooks/stripe",
            content=payload,
            headers={
                "Stripe-Signature": signature,
                "Content-Type": "application/json"
            }
        )

        assert response.status_code in [400, 422], \
            f"Expected 400/422 for malformed JSON, got {response.status_code}"

    def test_signature_verification_logs_events(self, client, webhook_secret, sample_event, caplog):
        """
        Test that signature verification events are logged

        Expected: Log entries for verification success/failure
        """
        import json
        import logging

        caplog.set_level(logging.INFO)

        # Test valid signature (should log success)
        payload = json.dumps(sample_event)
        valid_signature = self.generate_signature(payload, webhook_secret)

        response = client.post(
            "/webhooks/stripe",
            content=payload,
            headers={
                "Stripe-Signature": valid_signature,
                "Content-Type": "application/json"
            }
        )

        # Check logs for webhook verification
        assert any("webhook" in record.message.lower() for record in caplog.records), \
            "Expected webhook verification to be logged"

        # Test invalid signature (should log failure)
        caplog.clear()
        invalid_signature = self.generate_signature(payload, "wrong_secret")

        response = client.post(
            "/webhooks/stripe",
            content=payload,
            headers={
                "Stripe-Signature": invalid_signature,
                "Content-Type": "application/json"
            }
        )

        # Check logs for verification failure
        assert any(
            "error" in record.message.lower() or "failed" in record.message.lower()
            for record in caplog.records
        ), "Expected signature verification failure to be logged"


class TestStripeWebhookIntegration:
    """Integration tests for full webhook processing flow"""

    @pytest.fixture
    def client(self):
        """Create test client"""
        return TestClient(app)

    def test_checkout_session_completed_flow(self, client, mocker):
        """
        Test complete flow for checkout.session.completed webhook

        Expected: Payment record created, report generation triggered
        """
        # This test requires mocking Stripe SDK
        # Mock stripe.Webhook.construct_event to return valid event
        mock_event = {
            "id": "evt_test_123",
            "type": "checkout.session.completed",
            "data": {
                "object": {
                    "id": "cs_test_123",
                    "payment_status": "paid",
                    "metadata": {
                        "user_id": "test_user_123",
                        "report_id": "test_report_456"
                    }
                }
            }
        }

        mocker.patch(
            "stripe.Webhook.construct_event",
            return_value=mock_event
        )

        # Send webhook
        response = client.post(
            "/webhooks/stripe",
            json=mock_event,
            headers={
                "Stripe-Signature": "t=123,v1=test_signature",
                "Content-Type": "application/json"
            }
        )

        # Should process successfully
        assert response.status_code == 200

    @pytest.mark.skip(reason="Requires live Stripe test environment")
    def test_live_stripe_webhook(self):
        """
        Test with actual Stripe test webhook

        This test is skipped by default. To run:
        1. Set up Stripe CLI: stripe listen --forward-to localhost:8000/webhooks/stripe
        2. Trigger test event: stripe trigger checkout.session.completed
        3. Verify webhook is processed correctly
        """
        pass
