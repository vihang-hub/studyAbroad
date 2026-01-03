"""
Tests for payment service (Stripe integration)
"""
import pytest
from unittest.mock import patch, Mock, MagicMock
from datetime import datetime
from src.api.services.payment_service import (
    create_checkout_session,
    update_payment_status,
    get_payment_by_intent_id,
    verify_webhook_signature,
)
from src.api.models.payment import Payment, PaymentStatus


class TestCreateCheckoutSession:
    """Test suite for Stripe checkout session creation"""

    @pytest.mark.asyncio
    async def test_create_checkout_session_success(
        self, mock_user_id, mock_report_id, sample_uk_query
    ):
        """Test successful creation of Stripe checkout session"""
        with patch("src.api.services.payment_service.stripe.PaymentIntent") as mock_pi, \
             patch("src.api.services.payment_service.get_supabase") as mock_get_supabase:

            # Mock Stripe PaymentIntent
            mock_pi.create.return_value = Mock(
                id="pi_test_12345",
                client_secret="secret_test_12345",
            )

            # Mock Supabase
            mock_supabase = MagicMock()
            mock_supabase.table.return_value = mock_supabase
            mock_supabase.insert.return_value = mock_supabase
            mock_supabase.execute.return_value = Mock(data=[{"id": "payment_12345"}])
            mock_get_supabase.return_value = mock_supabase

            result = await create_checkout_session(
                user_id=mock_user_id,
                report_id=mock_report_id,
                query=sample_uk_query,
            )

            assert result.client_secret == "secret_test_12345"
            assert result.payment_intent_id == "pi_test_12345"
            assert result.amount == 299
            assert result.currency == "gbp"

            mock_pi.create.assert_called_once()
            mock_supabase.table.assert_called_with("payments")
            mock_supabase.insert.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_checkout_session_stripe_error(
        self, mock_user_id, mock_report_id, sample_uk_query
    ):
        """Test Stripe API error handling"""
        import stripe as stripe_lib

        with patch("src.api.services.payment_service.stripe.PaymentIntent") as mock_pi:
            mock_pi.create.side_effect = stripe_lib.error.StripeError("API Error")

            with pytest.raises(Exception) as exc_info:
                await create_checkout_session(
                    user_id=mock_user_id,
                    report_id=mock_report_id,
                    query=sample_uk_query,
                )

            assert "Stripe error" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_create_checkout_session_db_error(
        self, mock_user_id, mock_report_id, sample_uk_query
    ):
        """Test database error during payment record creation"""
        with patch("src.api.services.payment_service.stripe.PaymentIntent") as mock_pi, \
             patch("src.api.services.payment_service.get_supabase") as mock_get_supabase:

            mock_pi.create.return_value = Mock(
                id="pi_test_12345",
                client_secret="secret_test_12345",
            )

            mock_supabase = MagicMock()
            mock_supabase.table.return_value = mock_supabase
            mock_supabase.insert.return_value = mock_supabase
            mock_supabase.execute.side_effect = Exception("Database error")
            mock_get_supabase.return_value = mock_supabase

            with pytest.raises(Exception) as exc_info:
                await create_checkout_session(
                    user_id=mock_user_id,
                    report_id=mock_report_id,
                    query=sample_uk_query,
                )

            assert "Database error" in str(exc_info.value)


class TestUpdatePaymentStatus:
    """Test suite for payment status updates"""

    @pytest.mark.asyncio
    async def test_update_payment_status_success(self, sample_payment_data):
        """Test successful payment status update"""
        with patch("src.api.services.payment_service.get_supabase") as mock_get_supabase:
            mock_supabase = MagicMock()
            mock_supabase.table.return_value = mock_supabase
            mock_supabase.update.return_value = mock_supabase
            mock_supabase.eq.return_value = mock_supabase
            mock_supabase.execute.return_value = Mock(data=[sample_payment_data])
            mock_get_supabase.return_value = mock_supabase

            result = await update_payment_status(
                payment_intent_id="pi_test_12345",
                status=PaymentStatus.SUCCEEDED,
            )

            assert result is not None
            assert result.stripe_payment_intent_id == "pi_test_12345"
            mock_supabase.update.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_payment_status_with_error(self, sample_payment_data):
        """Test payment status update with error message"""
        with patch("src.api.services.payment_service.get_supabase") as mock_get_supabase:
            mock_supabase = MagicMock()
            mock_supabase.table.return_value = mock_supabase
            mock_supabase.update.return_value = mock_supabase
            mock_supabase.eq.return_value = mock_supabase
            mock_supabase.execute.return_value = Mock(data=[sample_payment_data])
            mock_get_supabase.return_value = mock_supabase

            result = await update_payment_status(
                payment_intent_id="pi_test_12345",
                status=PaymentStatus.FAILED,
                error_message="Card declined",
            )

            assert result is not None
            update_data = mock_supabase.update.call_args[0][0]
            assert update_data["error_message"] == "Card declined"

    @pytest.mark.asyncio
    async def test_update_payment_status_refunded(self):
        """Test refunded payment status includes refunded_at timestamp"""
        with patch("src.api.services.payment_service.get_supabase") as mock_get_supabase:
            mock_supabase = MagicMock()
            mock_supabase.table.return_value = mock_supabase
            mock_supabase.update.return_value = mock_supabase
            mock_supabase.eq.return_value = mock_supabase
            mock_supabase.execute.return_value = Mock(data=[])
            mock_get_supabase.return_value = mock_supabase

            await update_payment_status(
                payment_intent_id="pi_test_12345",
                status=PaymentStatus.REFUNDED,
            )

            update_data = mock_supabase.update.call_args[0][0]
            assert "refunded_at" in update_data

    @pytest.mark.asyncio
    async def test_update_payment_status_not_found(self):
        """Test payment status update when payment not found"""
        with patch("src.api.services.payment_service.get_supabase") as mock_get_supabase:
            mock_supabase = MagicMock()
            mock_supabase.table.return_value = mock_supabase
            mock_supabase.update.return_value = mock_supabase
            mock_supabase.eq.return_value = mock_supabase
            mock_supabase.execute.return_value = Mock(data=[])
            mock_get_supabase.return_value = mock_supabase

            result = await update_payment_status(
                payment_intent_id="pi_nonexistent",
                status=PaymentStatus.SUCCEEDED,
            )

            assert result is None


class TestGetPaymentByIntentId:
    """Test suite for retrieving payment by intent ID"""

    @pytest.mark.asyncio
    async def test_get_payment_found(self, sample_payment_data):
        """Test successful payment retrieval"""
        with patch("src.api.services.payment_service.get_supabase") as mock_get_supabase:
            mock_supabase = MagicMock()
            mock_supabase.table.return_value = mock_supabase
            mock_supabase.select.return_value = mock_supabase
            mock_supabase.eq.return_value = mock_supabase
            mock_supabase.execute.return_value = Mock(data=[sample_payment_data])
            mock_get_supabase.return_value = mock_supabase

            result = await get_payment_by_intent_id("pi_test_12345")

            assert result is not None
            assert result.stripe_payment_intent_id == "pi_test_12345"

    @pytest.mark.asyncio
    async def test_get_payment_not_found(self):
        """Test payment retrieval when not found"""
        with patch("src.api.services.payment_service.get_supabase") as mock_get_supabase:
            mock_supabase = MagicMock()
            mock_supabase.table.return_value = mock_supabase
            mock_supabase.select.return_value = mock_supabase
            mock_supabase.eq.return_value = mock_supabase
            mock_supabase.execute.return_value = Mock(data=[])
            mock_get_supabase.return_value = mock_supabase

            result = await get_payment_by_intent_id("pi_nonexistent")

            assert result is None


class TestVerifyWebhookSignature:
    """Test suite for Stripe webhook signature verification"""

    def test_verify_webhook_signature_valid(self):
        """Test successful webhook signature verification"""
        import stripe as stripe_lib

        with patch("src.api.services.payment_service.stripe.Webhook") as mock_webhook:
            mock_event = {"type": "payment_intent.succeeded", "id": "evt_12345"}
            mock_webhook.construct_event.return_value = mock_event

            result = verify_webhook_signature(b"payload", "sig_header")

            assert result == mock_event

    def test_verify_webhook_signature_invalid_payload(self):
        """Test webhook verification with invalid payload"""
        import stripe as stripe_lib

        with patch("src.api.services.payment_service.stripe.Webhook") as mock_webhook:
            mock_webhook.construct_event.side_effect = ValueError("Invalid payload")

            with pytest.raises(Exception) as exc_info:
                verify_webhook_signature(b"invalid", "sig_header")

            assert "Invalid payload" in str(exc_info.value)

    def test_verify_webhook_signature_invalid_signature(self):
        """Test webhook verification with invalid signature"""
        import stripe as stripe_lib

        with patch("src.api.services.payment_service.stripe.Webhook") as mock_webhook:
            mock_webhook.construct_event.side_effect = stripe_lib.error.SignatureVerificationError(
                "Invalid signature", "sig_header"
            )

            with pytest.raises(Exception) as exc_info:
                verify_webhook_signature(b"payload", "invalid_sig")

            assert "Invalid signature" in str(exc_info.value)
