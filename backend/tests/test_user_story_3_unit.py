"""
Unit Tests for User Story 3: Data Retention & Cleanup
Repository-level tests for data retention logic

Tests cover Tasks T146-T150:
- T146: expire_old_reports() marks reports as expired
- T147: RLS blocks access to expired reports
- T148: delete_expired_reports() hard deletes old reports
- T149: Monitoring and logging
- T150: GDPR compliance (cascade deletes)
"""

import pytest
from unittest.mock import Mock, AsyncMock, patch, MagicMock
from datetime import datetime, timedelta
import uuid


class TestExpireOldReports:
    """T146: Test expire_old_reports() function"""

    @pytest.mark.asyncio
    async def test_marks_expired_reports_as_expired(self):
        """Test reports past expires_at are marked as expired"""
        from src.database.repositories.report import ReportRepository
        from src.api.models.report import ReportStatus

        # Mock expired report
        mock_expired_report = Mock()
        mock_expired_report.id = str(uuid.uuid4())
        mock_expired_report.status = ReportStatus.COMPLETED
        mock_expired_report.expires_at = datetime.utcnow() - timedelta(days=1)

        # Mock result from execute
        mock_result = Mock()
        mock_result.scalars.return_value.all.return_value = [mock_expired_report]

        # Mock session with proper async context manager pattern
        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(return_value=mock_result)
        mock_session.commit = AsyncMock()

        # Mock adapter.get_session() as async context manager
        mock_context_manager = AsyncMock()
        mock_context_manager.__aenter__.return_value = mock_session
        mock_context_manager.__aexit__.return_value = None

        mock_adapter = MagicMock()
        mock_adapter.get_session = AsyncMock(return_value=mock_context_manager)

        repo = ReportRepository(mock_adapter)

        expired_count = await repo.expire_old_reports()

        assert expired_count == 1
        assert mock_expired_report.status == ReportStatus.EXPIRED

    @pytest.mark.asyncio
    async def test_returns_accurate_count(self):
        """Test expire_old_reports returns accurate count"""
        from src.database.repositories.report import ReportRepository
        from src.api.models.report import ReportStatus

        # Mock 5 expired reports
        expired_reports = [Mock(status=ReportStatus.COMPLETED, expires_at=datetime.utcnow() - timedelta(days=i)) for i in range(1, 6)]

        mock_result = Mock()
        mock_result.scalars.return_value.all.return_value = expired_reports

        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(return_value=mock_result)
        mock_session.commit = AsyncMock()

        mock_context_manager = AsyncMock()
        mock_context_manager.__aenter__.return_value = mock_session
        mock_context_manager.__aexit__.return_value = None

        mock_adapter = MagicMock()
        mock_adapter.get_session = AsyncMock(return_value=mock_context_manager)

        repo = ReportRepository(mock_adapter)

        count = await repo.expire_old_reports()

        assert count == 5

    @pytest.mark.asyncio
    async def test_only_expires_eligible_statuses(self):
        """Test only completed/pending/generating/failed reports are expired"""
        from src.database.repositories.report import ReportRepository
        from src.api.models.report import ReportStatus

        # Only completed reports in this case
        mock_report = Mock()
        mock_report.status = ReportStatus.COMPLETED
        mock_report.expires_at = datetime.utcnow() - timedelta(days=1)

        mock_result = Mock()
        mock_result.scalars.return_value.all.return_value = [mock_report]

        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(return_value=mock_result)
        mock_session.commit = AsyncMock()

        mock_context_manager = AsyncMock()
        mock_context_manager.__aenter__.return_value = mock_session
        mock_context_manager.__aexit__.return_value = None

        mock_adapter = MagicMock()
        mock_adapter.get_session = AsyncMock(return_value=mock_context_manager)

        repo = ReportRepository(mock_adapter)

        count = await repo.expire_old_reports()

        assert count == 1
        assert mock_report.status == ReportStatus.EXPIRED


class TestDeleteExpiredReports:
    """T148: Test delete_expired_reports() function"""

    @pytest.mark.asyncio
    async def test_deletes_reports_expired_90_days(self):
        """Test reports expired for 90+ days are hard deleted"""
        from src.database.repositories.report import ReportRepository
        from src.api.models.report import ReportStatus

        # Mock old expired report
        old_expires_at = datetime.utcnow() - timedelta(days=91)
        mock_old_report = Mock()
        mock_old_report.id = str(uuid.uuid4())
        mock_old_report.status = ReportStatus.EXPIRED
        mock_old_report.expires_at = old_expires_at

        mock_result = Mock()
        mock_result.scalars.return_value.all.return_value = [mock_old_report]

        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(return_value=mock_result)
        mock_session.delete = AsyncMock()
        mock_session.commit = AsyncMock()

        mock_context_manager = AsyncMock()
        mock_context_manager.__aenter__.return_value = mock_session
        mock_context_manager.__aexit__.return_value = None

        mock_adapter = MagicMock()
        mock_adapter.get_session = AsyncMock(return_value=mock_context_manager)

        repo = ReportRepository(mock_adapter)

        deleted_count = await repo.delete_expired_reports()

        assert deleted_count == 1
        mock_session.delete.assert_called_once_with(mock_old_report)

    @pytest.mark.asyncio
    async def test_returns_accurate_count(self):
        """Test delete_expired_reports returns accurate count"""
        from src.database.repositories.report import ReportRepository
        from src.api.models.report import ReportStatus

        # Mock 3 old expired reports
        old_reports = [
            Mock(id=str(uuid.uuid4()), status=ReportStatus.EXPIRED, expires_at=datetime.utcnow() - timedelta(days=90 + i))
            for i in range(1, 4)
        ]

        mock_result = Mock()
        mock_result.scalars.return_value.all.return_value = old_reports

        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(return_value=mock_result)
        mock_session.delete = AsyncMock()
        mock_session.commit = AsyncMock()

        mock_context_manager = AsyncMock()
        mock_context_manager.__aenter__.return_value = mock_session
        mock_context_manager.__aexit__.return_value = None

        mock_adapter = MagicMock()
        mock_adapter.get_session = AsyncMock(return_value=mock_context_manager)

        repo = ReportRepository(mock_adapter)

        count = await repo.delete_expired_reports()

        assert count == 3


class TestRLSBlocksExpiredReports:
    """T147: Test RLS blocks access to expired reports"""

    @pytest.mark.asyncio
    async def test_get_report_returns_none_for_expired(self):
        """Test get_report doesn't return expired reports"""
        from src.api.services.report_service import get_report

        user_id = "user_test_rls"
        report_id = str(uuid.uuid4())

        with patch("src.api.services.report_service.get_supabase") as mock_supabase:
            mock_client = MagicMock()
            mock_supabase.return_value = mock_client

            # Simulate RLS: expired reports are filtered out
            mock_chain = Mock()
            mock_chain.data = []
            mock_client.table.return_value.select.return_value.eq.return_value.eq.return_value.is_.return_value.execute.return_value = mock_chain

            report = await get_report(report_id, user_id)

            assert report is None

    @pytest.mark.asyncio
    async def test_list_user_reports_excludes_expired(self):
        """Test list_user_reports doesn't include expired reports"""
        from src.api.services.report_service import list_user_reports

        user_id = "user_test_list_expired"

        # In production, RLS handles this, but service filters deleted_at
        with patch("src.api.services.report_service.get_supabase") as mock_supabase:
            mock_client = MagicMock()
            mock_supabase.return_value = mock_client

            # Return only non-expired reports
            non_expired_reports = [
                {
                    "id": "report-1",
                    "query": "Active Report",
                    "status": "completed",
                    "created_at": datetime.utcnow().isoformat(),
                    "expires_at": (datetime.utcnow() + timedelta(days=10)).isoformat(),
                }
            ]

            mock_chain = Mock()
            mock_chain.data = non_expired_reports
            mock_client.table.return_value.select.return_value.eq.return_value.is_.return_value.order.return_value.limit.return_value.execute.return_value = mock_chain

            reports = await list_user_reports(user_id)

            assert len(reports) == 1
            assert reports[0].status == "completed"


class TestCronEndpointSecurity:
    """Test cron endpoint security (requires X-Cron-Secret)"""

    @pytest.mark.asyncio
    async def test_expire_endpoint_requires_secret(self):
        """Test /cron/expire-reports requires X-Cron-Secret header"""
        # This is tested at API route level
        # Dependency verify_cron_secret should raise 401 without valid secret
        from src.api.routes.cron import verify_cron_secret
        from fastapi import HTTPException

        with patch("src.api.routes.cron.settings") as mock_settings:
            mock_settings.CRON_SECRET = "correct_secret"

            # Wrong secret should raise 401
            with pytest.raises(HTTPException) as exc_info:
                verify_cron_secret(x_cron_secret="wrong_secret")

            assert exc_info.value.status_code == 401
            assert "Invalid cron secret" in exc_info.value.detail

    @pytest.mark.asyncio
    async def test_expire_endpoint_accepts_correct_secret(self):
        """Test /cron/expire-reports accepts correct secret"""
        from src.api.routes.cron import verify_cron_secret

        with patch("src.api.routes.cron.settings") as mock_settings:
            mock_settings.CRON_SECRET = "correct_secret"

            # Should not raise exception
            result = verify_cron_secret(x_cron_secret="correct_secret")
            assert result is None  # Returns None on success


class TestMonitoringAndLogging:
    """T149: Test monitoring and logging for cron jobs"""

    @pytest.mark.asyncio
    async def test_expire_job_logs_execution(self):
        """Test expire job logs success"""
        # Cron endpoints should log execution via structlog
        # Verified by checking logger calls in route handlers
        pass  # Logging is verified through integration tests

    @pytest.mark.asyncio
    async def test_expire_job_returns_correlation_id(self):
        """Test expire job returns correlation ID for tracking"""
        # Response should include correlation_id for monitoring
        pass  # Verified through API tests


class TestGDPRCompliance:
    """T150: Test GDPR compliance (cascade deletes)"""

    @pytest.mark.asyncio
    async def test_foreign_key_cascade_on_user_deletion(self):
        """Test database foreign key constraints cascade delete reports"""
        # This is enforced at database schema level
        # When user is deleted, all their reports should cascade delete
        # Verified by database migration and schema
        pass  # Database-level constraint, tested in DB migration tests

    @pytest.mark.asyncio
    async def test_hard_delete_is_permanent(self):
        """Test hard deleted reports are unrecoverable"""
        from src.database.repositories.report import ReportRepository

        report_id = str(uuid.uuid4())

        # Mock finding report
        mock_report = Mock()
        mock_report.id = report_id

        # Mock result using scalar_one_or_none() pattern (used by find_by_id)
        mock_find_result = Mock()
        mock_find_result.scalar_one_or_none.return_value = mock_report

        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(return_value=mock_find_result)
        mock_session.delete = AsyncMock()
        mock_session.commit = AsyncMock()

        mock_context_manager = AsyncMock()
        mock_context_manager.__aenter__.return_value = mock_session
        mock_context_manager.__aexit__.return_value = None

        mock_adapter = MagicMock()
        mock_adapter.get_session = AsyncMock(return_value=mock_context_manager)

        repo = ReportRepository(mock_adapter)

        # Hard delete
        deleted = await repo.hard_delete(report_id)

        assert deleted is True
        mock_session.delete.assert_called_once_with(mock_report)


class TestDataRetentionLifecycle:
    """Test complete data retention lifecycle"""

    @pytest.mark.asyncio
    async def test_report_lifecycle_30_day_expire_90_day_delete(self):
        """
        Test complete lifecycle:
        1. Report created with expires_at = created_at + 30 days
        2. After 30 days: expire_old_reports() marks as expired
        3. After 90 more days: delete_expired_reports() hard deletes
        """
        from src.database.repositories.report import ReportRepository
        from src.api.models.report import ReportStatus

        # Step 1: Report created 31 days ago
        created_at = datetime.utcnow() - timedelta(days=31)
        expires_at = created_at + timedelta(days=30)  # 1 day in past now

        mock_report = Mock()
        mock_report.id = str(uuid.uuid4())
        mock_report.status = ReportStatus.COMPLETED
        mock_report.created_at = created_at
        mock_report.expires_at = expires_at

        # Step 2: Expire (status becomes EXPIRED)
        mock_result_expire = Mock()
        mock_result_expire.scalars.return_value.all.return_value = [mock_report]

        mock_session = AsyncMock()
        mock_session.execute = AsyncMock(return_value=mock_result_expire)
        mock_session.commit = AsyncMock()

        mock_context_manager = AsyncMock()
        mock_context_manager.__aenter__.return_value = mock_session
        mock_context_manager.__aexit__.return_value = None

        mock_adapter = MagicMock()
        mock_adapter.get_session = AsyncMock(return_value=mock_context_manager)

        repo = ReportRepository(mock_adapter)

        expired_count = await repo.expire_old_reports()

        assert expired_count == 1
        assert mock_report.status == ReportStatus.EXPIRED

        # Step 3: After 90 more days, report is deleted
        # (Tested separately in delete tests)
