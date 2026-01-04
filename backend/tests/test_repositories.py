"""
Unit Tests for Database Repositories

Tests for PaymentRepository, UserRepository, and ReportRepository.
These tests mock the database adapter to test repository logic in isolation.
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime, timedelta
import uuid

from database.repositories.payment import PaymentRepository
from database.repositories.user import UserRepository
from database.repositories.report import ReportRepository
from database.models.payment import Payment
from database.models.user import User
from database.models.report import Report, ReportStatus


def create_mock_adapter():
    """Create a mock database adapter with async session context manager"""
    adapter = MagicMock()
    session = AsyncMock()

    # Create async context manager for get_session
    async_cm = AsyncMock()
    async_cm.__aenter__.return_value = session
    async_cm.__aexit__.return_value = None

    # get_session returns an awaitable that returns the async context manager
    adapter.get_session = AsyncMock(return_value=async_cm)

    return adapter, session


class TestPaymentRepository:
    """Test suite for PaymentRepository"""

    @pytest.mark.asyncio
    async def test_init(self):
        """Test repository initialization"""
        adapter, _ = create_mock_adapter()
        repo = PaymentRepository(adapter)
        assert repo.adapter == adapter

    @pytest.mark.asyncio
    async def test_find_by_id_found(self):
        """Test find_by_id returns payment when found"""
        adapter, session = create_mock_adapter()
        repo = PaymentRepository(adapter)

        mock_payment = MagicMock(spec=Payment)
        mock_payment.payment_id = "pay_123"

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_payment
        session.execute = AsyncMock(return_value=mock_result)

        result = await repo.find_by_id("pay_123")

        assert result == mock_payment
        session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_find_by_id_not_found(self):
        """Test find_by_id returns None when not found"""
        adapter, session = create_mock_adapter()
        repo = PaymentRepository(adapter)

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        session.execute = AsyncMock(return_value=mock_result)

        result = await repo.find_by_id("nonexistent")

        assert result is None

    @pytest.mark.asyncio
    async def test_find_by_stripe_session_id(self):
        """Test find_by_stripe_session_id returns payment"""
        adapter, session = create_mock_adapter()
        repo = PaymentRepository(adapter)

        mock_payment = MagicMock(spec=Payment)
        mock_payment.stripe_checkout_session_id = "cs_123"

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_payment
        session.execute = AsyncMock(return_value=mock_result)

        result = await repo.find_by_stripe_session_id("cs_123")

        assert result == mock_payment

    @pytest.mark.asyncio
    async def test_find_by_stripe_payment_intent_id(self):
        """Test find_by_stripe_payment_intent_id returns payment"""
        adapter, session = create_mock_adapter()
        repo = PaymentRepository(adapter)

        mock_payment = MagicMock(spec=Payment)
        mock_payment.stripe_payment_intent_id = "pi_123"

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_payment
        session.execute = AsyncMock(return_value=mock_result)

        result = await repo.find_by_stripe_payment_intent_id("pi_123")

        assert result == mock_payment

    @pytest.mark.asyncio
    async def test_find_by_user(self):
        """Test find_by_user returns list of payments"""
        adapter, session = create_mock_adapter()
        repo = PaymentRepository(adapter)

        mock_payments = [MagicMock(spec=Payment), MagicMock(spec=Payment)]

        mock_scalars = MagicMock()
        mock_scalars.all.return_value = mock_payments
        mock_result = MagicMock()
        mock_result.scalars.return_value = mock_scalars
        session.execute = AsyncMock(return_value=mock_result)

        result = await repo.find_by_user("user_123", skip=0, limit=10)

        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_find_all(self):
        """Test find_all returns list of payments"""
        adapter, session = create_mock_adapter()
        repo = PaymentRepository(adapter)

        mock_payments = [MagicMock(spec=Payment)]

        mock_scalars = MagicMock()
        mock_scalars.all.return_value = mock_payments
        mock_result = MagicMock()
        mock_result.scalars.return_value = mock_scalars
        session.execute = AsyncMock(return_value=mock_result)

        result = await repo.find_all(skip=0, limit=100)

        assert len(result) == 1

    @pytest.mark.asyncio
    async def test_create(self):
        """Test create adds and returns payment"""
        adapter, session = create_mock_adapter()
        repo = PaymentRepository(adapter)

        payment_data = {
            "user_id": uuid.uuid4(),
            "stripe_checkout_session_id": "cs_test_123",
            "stripe_payment_intent_id": "pi_123",
        }

        session.add = MagicMock()
        session.commit = AsyncMock()
        session.refresh = AsyncMock()

        result = await repo.create(payment_data)

        assert result is not None
        session.add.assert_called_once()
        session.commit.assert_called_once()
        session.refresh.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_found(self):
        """Test update modifies and returns payment"""
        adapter, session = create_mock_adapter()
        repo = PaymentRepository(adapter)

        mock_payment = MagicMock(spec=Payment)
        mock_payment.status = "pending"

        # Mock find_by_id to return the payment
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_payment
        session.execute = AsyncMock(return_value=mock_result)
        session.add = MagicMock()
        session.commit = AsyncMock()
        session.refresh = AsyncMock()

        result = await repo.update("pay_123", {"status": "succeeded"})

        assert result is not None
        session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_not_found(self):
        """Test update returns None when payment not found"""
        adapter, session = create_mock_adapter()
        repo = PaymentRepository(adapter)

        # Mock find_by_id to return None
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        session.execute = AsyncMock(return_value=mock_result)

        result = await repo.update("nonexistent", {"status": "succeeded"})

        assert result is None

    @pytest.mark.asyncio
    async def test_soft_delete_returns_none(self):
        """Test soft_delete returns None (not implemented for payments)"""
        adapter, _ = create_mock_adapter()
        repo = PaymentRepository(adapter)

        result = await repo.soft_delete("pay_123")

        assert result is None

    @pytest.mark.asyncio
    async def test_hard_delete_returns_false(self):
        """Test hard_delete returns False (not allowed for payments)"""
        adapter, _ = create_mock_adapter()
        repo = PaymentRepository(adapter)

        result = await repo.hard_delete("pay_123")

        assert result is False

    @pytest.mark.asyncio
    async def test_restore_returns_none(self):
        """Test restore returns None (not implemented for payments)"""
        adapter, _ = create_mock_adapter()
        repo = PaymentRepository(adapter)

        result = await repo.restore("pay_123")

        assert result is None


class TestUserRepository:
    """Test suite for UserRepository"""

    @pytest.mark.asyncio
    async def test_init(self):
        """Test repository initialization"""
        adapter, _ = create_mock_adapter()
        repo = UserRepository(adapter)
        assert repo.adapter == adapter

    @pytest.mark.asyncio
    async def test_find_by_id_found(self):
        """Test find_by_id returns user when found"""
        adapter, session = create_mock_adapter()
        repo = UserRepository(adapter)

        mock_user = MagicMock(spec=User)
        mock_user.user_id = "user_123"

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_user
        session.execute = AsyncMock(return_value=mock_result)

        result = await repo.find_by_id("user_123")

        assert result == mock_user

    @pytest.mark.asyncio
    async def test_find_by_id_not_found(self):
        """Test find_by_id returns None when not found"""
        adapter, session = create_mock_adapter()
        repo = UserRepository(adapter)

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        session.execute = AsyncMock(return_value=mock_result)

        result = await repo.find_by_id("nonexistent")

        assert result is None

    @pytest.mark.asyncio
    async def test_find_by_clerk_id(self):
        """Test find_by_clerk_id returns user"""
        adapter, session = create_mock_adapter()
        repo = UserRepository(adapter)

        mock_user = MagicMock(spec=User)
        mock_user.clerk_user_id = "clerk_123"

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_user
        session.execute = AsyncMock(return_value=mock_result)

        result = await repo.find_by_clerk_id("clerk_123")

        assert result == mock_user

    @pytest.mark.asyncio
    async def test_find_by_email(self):
        """Test find_by_email returns user"""
        adapter, session = create_mock_adapter()
        repo = UserRepository(adapter)

        mock_user = MagicMock(spec=User)
        mock_user.email = "test@example.com"

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_user
        session.execute = AsyncMock(return_value=mock_result)

        result = await repo.find_by_email("test@example.com")

        assert result == mock_user

    @pytest.mark.asyncio
    async def test_find_all(self):
        """Test find_all returns list of users"""
        adapter, session = create_mock_adapter()
        repo = UserRepository(adapter)

        mock_users = [MagicMock(spec=User), MagicMock(spec=User)]

        mock_scalars = MagicMock()
        mock_scalars.all.return_value = mock_users
        mock_result = MagicMock()
        mock_result.scalars.return_value = mock_scalars
        session.execute = AsyncMock(return_value=mock_result)

        result = await repo.find_all(skip=0, limit=100)

        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_create(self):
        """Test create adds and returns user"""
        adapter, session = create_mock_adapter()
        repo = UserRepository(adapter)

        user_data = {
            "user_id": str(uuid.uuid4()),
            "clerk_user_id": "clerk_123",
            "email": "test@example.com",
        }

        session.add = MagicMock()
        session.commit = AsyncMock()
        session.refresh = AsyncMock()

        result = await repo.create(user_data)

        assert result is not None
        session.add.assert_called_once()
        session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_found(self):
        """Test update modifies and returns user"""
        adapter, session = create_mock_adapter()
        repo = UserRepository(adapter)

        mock_user = MagicMock(spec=User)
        mock_user.email = "old@example.com"

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_user
        session.execute = AsyncMock(return_value=mock_result)
        session.add = MagicMock()
        session.commit = AsyncMock()
        session.refresh = AsyncMock()

        result = await repo.update("user_123", {"email": "new@example.com"})

        assert result is not None
        session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_not_found(self):
        """Test update returns None when user not found"""
        adapter, session = create_mock_adapter()
        repo = UserRepository(adapter)

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        session.execute = AsyncMock(return_value=mock_result)

        result = await repo.update("nonexistent", {"email": "new@example.com"})

        assert result is None

    @pytest.mark.asyncio
    async def test_soft_delete_returns_none(self):
        """Test soft_delete returns None (not implemented for users)"""
        adapter, _ = create_mock_adapter()
        repo = UserRepository(adapter)

        result = await repo.soft_delete("user_123")

        assert result is None

    @pytest.mark.asyncio
    async def test_hard_delete_found(self):
        """Test hard_delete removes user and returns True"""
        adapter, session = create_mock_adapter()
        repo = UserRepository(adapter)

        mock_user = MagicMock(spec=User)

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_user
        session.execute = AsyncMock(return_value=mock_result)
        session.delete = AsyncMock()
        session.commit = AsyncMock()

        result = await repo.hard_delete("user_123")

        assert result is True
        session.delete.assert_called_once_with(mock_user)
        session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_hard_delete_not_found(self):
        """Test hard_delete returns False when user not found"""
        adapter, session = create_mock_adapter()
        repo = UserRepository(adapter)

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        session.execute = AsyncMock(return_value=mock_result)

        result = await repo.hard_delete("nonexistent")

        assert result is False

    @pytest.mark.asyncio
    async def test_restore_returns_none(self):
        """Test restore returns None (not implemented for users)"""
        adapter, _ = create_mock_adapter()
        repo = UserRepository(adapter)

        result = await repo.restore("user_123")

        assert result is None


class TestReportRepository:
    """Test suite for ReportRepository"""

    @pytest.mark.asyncio
    async def test_init(self):
        """Test repository initialization"""
        adapter, _ = create_mock_adapter()
        repo = ReportRepository(adapter)
        assert repo.adapter == adapter

    @pytest.mark.asyncio
    async def test_find_by_id_found(self):
        """Test find_by_id returns report when found"""
        adapter, session = create_mock_adapter()
        repo = ReportRepository(adapter)

        mock_report = MagicMock(spec=Report)
        mock_report.report_id = "report_123"
        mock_report.status = ReportStatus.COMPLETED

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_report
        session.execute = AsyncMock(return_value=mock_result)

        result = await repo.find_by_id("report_123")

        assert result == mock_report

    @pytest.mark.asyncio
    async def test_find_by_id_not_found(self):
        """Test find_by_id returns None when not found"""
        adapter, session = create_mock_adapter()
        repo = ReportRepository(adapter)

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        session.execute = AsyncMock(return_value=mock_result)

        result = await repo.find_by_id("nonexistent")

        assert result is None

    @pytest.mark.asyncio
    async def test_find_by_id_include_deleted(self):
        """Test find_by_id with include_deleted=True returns expired reports"""
        adapter, session = create_mock_adapter()
        repo = ReportRepository(adapter)

        mock_report = MagicMock(spec=Report)
        mock_report.status = ReportStatus.EXPIRED

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_report
        session.execute = AsyncMock(return_value=mock_result)

        result = await repo.find_by_id("report_123", include_deleted=True)

        assert result == mock_report

    @pytest.mark.asyncio
    async def test_find_by_user(self):
        """Test find_by_user returns list of reports"""
        adapter, session = create_mock_adapter()
        repo = ReportRepository(adapter)

        mock_reports = [MagicMock(spec=Report), MagicMock(spec=Report)]

        mock_scalars = MagicMock()
        mock_scalars.all.return_value = mock_reports
        mock_result = MagicMock()
        mock_result.scalars.return_value = mock_scalars
        session.execute = AsyncMock(return_value=mock_result)

        result = await repo.find_by_user("user_123", skip=0, limit=10)

        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_find_by_user_include_deleted(self):
        """Test find_by_user with include_deleted=True returns all reports"""
        adapter, session = create_mock_adapter()
        repo = ReportRepository(adapter)

        mock_reports = [MagicMock(spec=Report)]

        mock_scalars = MagicMock()
        mock_scalars.all.return_value = mock_reports
        mock_result = MagicMock()
        mock_result.scalars.return_value = mock_scalars
        session.execute = AsyncMock(return_value=mock_result)

        result = await repo.find_by_user("user_123", include_deleted=True)

        assert len(result) == 1

    @pytest.mark.asyncio
    async def test_find_all(self):
        """Test find_all returns list of reports"""
        adapter, session = create_mock_adapter()
        repo = ReportRepository(adapter)

        mock_reports = [MagicMock(spec=Report)]

        mock_scalars = MagicMock()
        mock_scalars.all.return_value = mock_reports
        mock_result = MagicMock()
        mock_result.scalars.return_value = mock_scalars
        session.execute = AsyncMock(return_value=mock_result)

        result = await repo.find_all(skip=0, limit=100)

        assert len(result) == 1

    @pytest.mark.asyncio
    async def test_find_all_include_deleted(self):
        """Test find_all with include_deleted=True returns all reports"""
        adapter, session = create_mock_adapter()
        repo = ReportRepository(adapter)

        mock_reports = [MagicMock(spec=Report), MagicMock(spec=Report)]

        mock_scalars = MagicMock()
        mock_scalars.all.return_value = mock_reports
        mock_result = MagicMock()
        mock_result.scalars.return_value = mock_scalars
        session.execute = AsyncMock(return_value=mock_result)

        result = await repo.find_all(include_deleted=True)

        assert len(result) == 2

    @pytest.mark.asyncio
    async def test_create(self):
        """Test create adds and returns report"""
        adapter, session = create_mock_adapter()
        repo = ReportRepository(adapter)

        report_data = {
            "user_id": uuid.uuid4(),
            "subject": "Computer Science",
            "country": "UK",
            "status": ReportStatus.PENDING,
        }

        session.add = MagicMock()
        session.commit = AsyncMock()
        session.refresh = AsyncMock()

        result = await repo.create(report_data)

        assert result is not None
        session.add.assert_called_once()
        session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_found(self):
        """Test update modifies and returns report"""
        adapter, session = create_mock_adapter()
        repo = ReportRepository(adapter)

        mock_report = MagicMock(spec=Report)
        mock_report.status = ReportStatus.PENDING

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_report
        session.execute = AsyncMock(return_value=mock_result)
        session.add = MagicMock()
        session.commit = AsyncMock()
        session.refresh = AsyncMock()

        result = await repo.update("report_123", {"status": ReportStatus.COMPLETED})

        assert result is not None
        session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_update_not_found(self):
        """Test update returns None when report not found"""
        adapter, session = create_mock_adapter()
        repo = ReportRepository(adapter)

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        session.execute = AsyncMock(return_value=mock_result)

        result = await repo.update("nonexistent", {"status": ReportStatus.COMPLETED})

        assert result is None

    @pytest.mark.asyncio
    async def test_soft_delete(self):
        """Test soft_delete sets status to EXPIRED"""
        adapter, session = create_mock_adapter()
        repo = ReportRepository(adapter)

        mock_report = MagicMock(spec=Report)
        mock_report.status = ReportStatus.COMPLETED

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_report
        session.execute = AsyncMock(return_value=mock_result)
        session.add = MagicMock()
        session.commit = AsyncMock()
        session.refresh = AsyncMock()

        result = await repo.soft_delete("report_123")

        assert result is not None

    @pytest.mark.asyncio
    async def test_hard_delete_found(self):
        """Test hard_delete removes report and returns True"""
        adapter, session = create_mock_adapter()
        repo = ReportRepository(adapter)

        mock_report = MagicMock(spec=Report)

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_report
        session.execute = AsyncMock(return_value=mock_result)
        session.delete = AsyncMock()
        session.commit = AsyncMock()

        result = await repo.hard_delete("report_123")

        assert result is True
        session.delete.assert_called_once()
        session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_hard_delete_not_found(self):
        """Test hard_delete returns False when report not found"""
        adapter, session = create_mock_adapter()
        repo = ReportRepository(adapter)

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        session.execute = AsyncMock(return_value=mock_result)

        result = await repo.hard_delete("nonexistent")

        assert result is False

    @pytest.mark.asyncio
    async def test_restore_expired_report(self):
        """Test restore sets expired report status back to COMPLETED"""
        adapter, session = create_mock_adapter()
        repo = ReportRepository(adapter)

        mock_report = MagicMock(spec=Report)
        mock_report.status = ReportStatus.EXPIRED

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_report
        session.execute = AsyncMock(return_value=mock_result)
        session.add = MagicMock()
        session.commit = AsyncMock()
        session.refresh = AsyncMock()

        result = await repo.restore("report_123")

        assert result is not None

    @pytest.mark.asyncio
    async def test_restore_non_expired_report(self):
        """Test restore returns None for non-expired report"""
        adapter, session = create_mock_adapter()
        repo = ReportRepository(adapter)

        mock_report = MagicMock(spec=Report)
        mock_report.status = ReportStatus.COMPLETED  # Not expired

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = mock_report
        session.execute = AsyncMock(return_value=mock_result)

        result = await repo.restore("report_123")

        assert result is None

    @pytest.mark.asyncio
    async def test_restore_not_found(self):
        """Test restore returns None when report not found"""
        adapter, session = create_mock_adapter()
        repo = ReportRepository(adapter)

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        session.execute = AsyncMock(return_value=mock_result)

        result = await repo.restore("nonexistent")

        assert result is None

    @pytest.mark.asyncio
    async def test_expire_old_reports(self):
        """Test expire_old_reports marks old reports as expired"""
        adapter, session = create_mock_adapter()
        repo = ReportRepository(adapter)

        # Create mock reports that are past expiry
        mock_reports = [
            MagicMock(spec=Report),
            MagicMock(spec=Report),
        ]
        for report in mock_reports:
            report.status = ReportStatus.COMPLETED

        mock_scalars = MagicMock()
        mock_scalars.all.return_value = mock_reports
        mock_result = MagicMock()
        mock_result.scalars.return_value = mock_scalars
        session.execute = AsyncMock(return_value=mock_result)
        session.commit = AsyncMock()

        count = await repo.expire_old_reports()

        assert count == 2
        for report in mock_reports:
            assert report.status == ReportStatus.EXPIRED
        session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_expire_old_reports_none_to_expire(self):
        """Test expire_old_reports returns 0 when no reports need expiring"""
        adapter, session = create_mock_adapter()
        repo = ReportRepository(adapter)

        mock_scalars = MagicMock()
        mock_scalars.all.return_value = []
        mock_result = MagicMock()
        mock_result.scalars.return_value = mock_scalars
        session.execute = AsyncMock(return_value=mock_result)
        session.commit = AsyncMock()

        count = await repo.expire_old_reports()

        assert count == 0

    @pytest.mark.asyncio
    async def test_delete_expired_reports(self):
        """Test delete_expired_reports permanently deletes old expired reports"""
        adapter, session = create_mock_adapter()
        repo = ReportRepository(adapter)

        mock_reports = [
            MagicMock(spec=Report),
            MagicMock(spec=Report),
            MagicMock(spec=Report),
        ]

        mock_scalars = MagicMock()
        mock_scalars.all.return_value = mock_reports
        mock_result = MagicMock()
        mock_result.scalars.return_value = mock_scalars
        session.execute = AsyncMock(return_value=mock_result)
        session.delete = AsyncMock()
        session.commit = AsyncMock()

        count = await repo.delete_expired_reports()

        assert count == 3
        assert session.delete.call_count == 3
        session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_delete_expired_reports_none_to_delete(self):
        """Test delete_expired_reports returns 0 when no reports need deletion"""
        adapter, session = create_mock_adapter()
        repo = ReportRepository(adapter)

        mock_scalars = MagicMock()
        mock_scalars.all.return_value = []
        mock_result = MagicMock()
        mock_result.scalars.return_value = mock_scalars
        session.execute = AsyncMock(return_value=mock_result)
        session.commit = AsyncMock()

        count = await repo.delete_expired_reports()

        assert count == 0
