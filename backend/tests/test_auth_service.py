"""
Tests for authentication service (Clerk JWT verification)
"""
import pytest
from unittest.mock import patch, Mock
from fastapi import HTTPException
from src.api.services.auth_service import (
    verify_clerk_token,
    get_current_user_id,
    validate_cron_secret,
)
from fastapi.security import HTTPAuthorizationCredentials


class TestVerifyClerkToken:
    """Test suite for Clerk token verification"""

    def test_verify_valid_token(self):
        """Test verification of valid Clerk JWT token"""
        mock_credentials = Mock(spec=HTTPAuthorizationCredentials)
        mock_credentials.credentials = "valid_token"

        with patch("src.api.services.auth_service.jwt.decode") as mock_decode:
            mock_decode.return_value = {"sub": "user_12345"}

            user_id = verify_clerk_token(mock_credentials)

            assert user_id == "user_12345"
            mock_decode.assert_called_once()

    def test_verify_token_missing_subject(self):
        """Test verification fails when token missing subject (sub)"""
        mock_credentials = Mock(spec=HTTPAuthorizationCredentials)
        mock_credentials.credentials = "invalid_token"

        with patch("src.api.services.auth_service.jwt.decode") as mock_decode:
            mock_decode.return_value = {}  # Missing 'sub'

            with pytest.raises(HTTPException) as exc_info:
                verify_clerk_token(mock_credentials)

            assert exc_info.value.status_code == 401
            assert "missing subject" in exc_info.value.detail.lower()

    def test_verify_expired_token(self):
        """Test verification fails for expired tokens"""
        import jwt as pyjwt

        mock_credentials = Mock(spec=HTTPAuthorizationCredentials)
        mock_credentials.credentials = "expired_token"

        with patch("src.api.services.auth_service.jwt.decode") as mock_decode:
            mock_decode.side_effect = pyjwt.ExpiredSignatureError()

            with pytest.raises(HTTPException) as exc_info:
                verify_clerk_token(mock_credentials)

            assert exc_info.value.status_code == 401
            assert "expired" in exc_info.value.detail.lower()

    def test_verify_invalid_token_format(self):
        """Test verification fails for malformed tokens"""
        import jwt as pyjwt

        mock_credentials = Mock(spec=HTTPAuthorizationCredentials)
        mock_credentials.credentials = "malformed_token"

        with patch("src.api.services.auth_service.jwt.decode") as mock_decode:
            mock_decode.side_effect = pyjwt.InvalidTokenError("Invalid token")

            with pytest.raises(HTTPException) as exc_info:
                verify_clerk_token(mock_credentials)

            assert exc_info.value.status_code == 401
            assert "invalid token" in exc_info.value.detail.lower()


class TestGetCurrentUserId:
    """Test suite for get_current_user_id dependency"""

    @pytest.mark.asyncio
    async def test_get_current_user_id_success(self):
        """Test successful user ID extraction"""
        mock_credentials = Mock(spec=HTTPAuthorizationCredentials)
        mock_credentials.credentials = "valid_token"

        with patch("src.api.services.auth_service.verify_clerk_token") as mock_verify:
            mock_verify.return_value = "user_67890"

            user_id = await get_current_user_id(mock_credentials)

            assert user_id == "user_67890"
            mock_verify.assert_called_once_with(mock_credentials)

    @pytest.mark.asyncio
    async def test_get_current_user_id_failure(self):
        """Test user ID extraction failure"""
        mock_credentials = Mock(spec=HTTPAuthorizationCredentials)
        mock_credentials.credentials = "invalid_token"

        with patch("src.api.services.auth_service.verify_clerk_token") as mock_verify:
            mock_verify.side_effect = HTTPException(status_code=401, detail="Invalid token")

            with pytest.raises(HTTPException) as exc_info:
                await get_current_user_id(mock_credentials)

            assert exc_info.value.status_code == 401


class TestValidateCronSecret:
    """Test suite for cron secret validation"""

    def test_validate_cron_secret_valid(self):
        """Test validation with non-empty cron secret"""
        # Current implementation just checks for non-empty string
        result = validate_cron_secret("valid_secret_12345")
        assert result is True

    def test_validate_cron_secret_any_nonempty_string(self):
        """Test validation with any non-empty secret returns True"""
        # Current implementation accepts any non-empty string (dev mode)
        result = validate_cron_secret("any_string")
        assert result is True

    def test_validate_cron_secret_missing(self):
        """Test validation with missing cron secret"""
        result = validate_cron_secret(None)
        assert result is False

    def test_validate_cron_secret_empty(self):
        """Test validation with empty cron secret"""
        result = validate_cron_secret("")
        assert result is False
