"""
Tests for User Pydantic models
"""
import pytest
from datetime import datetime
from pydantic import ValidationError
from src.api.models.user import User, UserCreate, UserProfile


class TestUserModel:
    """Test suite for User model"""

    def test_user_model_valid(self):
        """Test User model with valid data"""
        user_data = {
            "id": "user_123",
            "clerk_user_id": "clerk_456",
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "profile_image_url": "https://example.com/image.jpg",
            "auth_provider": "clerk",
            "email_verified": True,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }

        user = User(**user_data)

        assert user.id == "user_123"
        assert user.clerk_user_id == "clerk_456"
        assert user.email == "test@example.com"
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.profile_image_url == "https://example.com/image.jpg"
        assert user.auth_provider == "clerk"
        assert user.email_verified is True
        assert user.deleted_at is None

    def test_user_model_minimal(self):
        """Test User model with minimal required fields"""
        user_data = {
            "id": "user_123",
            "clerk_user_id": "clerk_456",
            "email": "test@example.com",
            "auth_provider": "clerk",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }

        user = User(**user_data)

        assert user.id == "user_123"
        assert user.first_name is None
        assert user.last_name is None
        assert user.profile_image_url is None
        assert user.email_verified is False
        assert user.deleted_at is None

    def test_user_model_with_deleted_at(self):
        """Test User model with soft delete timestamp"""
        deleted_time = datetime.utcnow()
        user_data = {
            "id": "user_123",
            "clerk_user_id": "clerk_456",
            "email": "test@example.com",
            "auth_provider": "clerk",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "deleted_at": deleted_time,
        }

        user = User(**user_data)

        assert user.deleted_at == deleted_time

    def test_user_model_invalid_email(self):
        """Test User model rejects invalid email"""
        user_data = {
            "id": "user_123",
            "clerk_user_id": "clerk_456",
            "email": "invalid_email",  # Invalid email format
            "auth_provider": "clerk",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
        }

        with pytest.raises(ValidationError) as exc_info:
            User(**user_data)

        assert "email" in str(exc_info.value).lower()

    def test_user_model_from_attributes(self):
        """Test User model can be created from ORM attributes"""
        # This tests the Config.from_attributes = True setting
        class MockORM:
            id = "user_123"
            clerk_user_id = "clerk_456"
            email = "test@example.com"
            first_name = "John"
            last_name = "Doe"
            profile_image_url = None
            auth_provider = "clerk"
            email_verified = True
            created_at = datetime.utcnow()
            updated_at = datetime.utcnow()
            deleted_at = None

        user = User.model_validate(MockORM())

        assert user.id == "user_123"
        assert user.email == "test@example.com"


class TestUserCreateModel:
    """Test suite for UserCreate model"""

    def test_user_create_valid(self):
        """Test UserCreate model with valid data"""
        user_data = {
            "clerk_user_id": "clerk_456",
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "Doe",
            "profile_image_url": "https://example.com/image.jpg",
            "auth_provider": "clerk",
            "email_verified": True,
        }

        user_create = UserCreate(**user_data)

        assert user_create.clerk_user_id == "clerk_456"
        assert user_create.email == "test@example.com"
        assert user_create.first_name == "John"
        assert user_create.auth_provider == "clerk"

    def test_user_create_minimal(self):
        """Test UserCreate model with minimal required fields"""
        user_data = {
            "clerk_user_id": "clerk_456",
            "email": "test@example.com",
            "auth_provider": "clerk",
        }

        user_create = UserCreate(**user_data)

        assert user_create.clerk_user_id == "clerk_456"
        assert user_create.email == "test@example.com"
        assert user_create.first_name is None
        assert user_create.last_name is None
        assert user_create.profile_image_url is None
        assert user_create.email_verified is False

    def test_user_create_invalid_email(self):
        """Test UserCreate model rejects invalid email"""
        user_data = {
            "clerk_user_id": "clerk_456",
            "email": "invalid_email",
            "auth_provider": "clerk",
        }

        with pytest.raises(ValidationError) as exc_info:
            UserCreate(**user_data)

        assert "email" in str(exc_info.value).lower()

    def test_user_create_missing_required_fields(self):
        """Test UserCreate model requires essential fields"""
        user_data = {
            "clerk_user_id": "clerk_456",
            # Missing email and auth_provider
        }

        with pytest.raises(ValidationError) as exc_info:
            UserCreate(**user_data)

        error_str = str(exc_info.value)
        assert "email" in error_str.lower() or "field required" in error_str.lower()


class TestUserProfileModel:
    """Test suite for UserProfile model"""

    def test_user_profile_valid(self):
        """Test UserProfile model with valid data"""
        profile_data = {
            "user_id": "user_123",
            "display_name": "John Doe",
            "email": "test@example.com",
            "avatar_url": "https://example.com/avatar.jpg",
            "is_subscribed": True,
        }

        profile = UserProfile(**profile_data)

        assert profile.user_id == "user_123"
        assert profile.display_name == "John Doe"
        assert profile.email == "test@example.com"
        assert profile.avatar_url == "https://example.com/avatar.jpg"
        assert profile.is_subscribed is True

    def test_user_profile_minimal(self):
        """Test UserProfile model with minimal required fields"""
        profile_data = {
            "user_id": "user_123",
            "display_name": "John Doe",
            "email": "test@example.com",
        }

        profile = UserProfile(**profile_data)

        assert profile.user_id == "user_123"
        assert profile.display_name == "John Doe"
        assert profile.avatar_url is None
        assert profile.is_subscribed is False

    def test_user_profile_invalid_email(self):
        """Test UserProfile model rejects invalid email"""
        profile_data = {
            "user_id": "user_123",
            "display_name": "John Doe",
            "email": "invalid_email",
        }

        with pytest.raises(ValidationError) as exc_info:
            UserProfile(**profile_data)

        assert "email" in str(exc_info.value).lower()

    def test_user_profile_missing_required_fields(self):
        """Test UserProfile model requires essential fields"""
        profile_data = {
            "user_id": "user_123",
            # Missing display_name and email
        }

        with pytest.raises(ValidationError) as exc_info:
            UserProfile(**profile_data)

        error_str = str(exc_info.value)
        assert "field required" in error_str.lower()
