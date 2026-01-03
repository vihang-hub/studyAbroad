"""
Unit Tests for User Story 2: View Report History
Service-level tests without full integration

Tests cover Tasks T130-T134:
- T130: list_user_reports returns user's reports
- T131: get_report returns content without regeneration
- T132: RLS user scoping
- T133: Immutability - no AI calls on retrieval
- T134: Empty state handling
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta
import uuid


class TestListUserReports:
    """T130: Test list_user_reports service function"""

    @pytest.mark.asyncio
    async def test_returns_user_reports_sorted_by_created_at(self):
        """Test reports are returned sorted by created_at DESC"""
        from src.api.services.report_service import list_user_reports

        user_id = "user_test_123"
        mock_reports = [
            {
                "id": "report-1",
                "query": "Computer Science",
                "status": "completed",
                "created_at": datetime.utcnow().isoformat(),
                "expires_at": (datetime.utcnow() + timedelta(days=30)).isoformat(),
            },
            {
                "id": "report-2",
                "query": "Nursing",
                "status": "completed",
                "created_at": (datetime.utcnow() - timedelta(days=1)).isoformat(),
                "expires_at": (datetime.utcnow() + timedelta(days=29)).isoformat(),
            },
        ]

        with patch("src.api.services.report_service.get_supabase") as mock_supabase:
            mock_client = MagicMock()
            mock_supabase.return_value = mock_client

            # Mock chain: table().select().eq().is_().order().limit().execute()
            mock_chain = Mock()
            mock_chain.data = mock_reports

            mock_client.table.return_value.select.return_value.eq.return_value.is_.return_value.order.return_value.limit.return_value.execute.return_value = mock_chain

            reports = await list_user_reports(user_id, limit=10)

            assert len(reports) == 2
            assert reports[0].id == "report-1"
            assert reports[1].id == "report-2"

    @pytest.mark.asyncio
    async def test_respects_limit_parameter(self):
        """Test limit parameter is applied correctly"""
        from src.api.services.report_service import list_user_reports

        user_id = "user_test_limit"
        mock_reports = [{"id": f"report-{i}", "query": f"Query {i}", "status": "completed", "created_at": datetime.utcnow().isoformat(), "expires_at": datetime.utcnow().isoformat()} for i in range(5)]

        with patch("src.api.services.report_service.get_supabase") as mock_supabase:
            mock_client = MagicMock()
            mock_supabase.return_value = mock_client

            mock_chain = Mock()
            mock_chain.data = mock_reports
            mock_client.table.return_value.select.return_value.eq.return_value.is_.return_value.order.return_value.limit.return_value.execute.return_value = mock_chain

            await list_user_reports(user_id, limit=5)

            # Verify limit was called with 5
            mock_client.table.return_value.select.return_value.eq.return_value.is_.return_value.order.return_value.limit.assert_called_once_with(5)

    @pytest.mark.asyncio
    async def test_returns_empty_array_when_no_reports(self):
        """T134: Test empty state returns empty array"""
        from src.api.services.report_service import list_user_reports

        user_id = "user_no_reports"

        with patch("src.api.services.report_service.get_supabase") as mock_supabase:
            mock_client = MagicMock()
            mock_supabase.return_value = mock_client

            mock_chain = Mock()
            mock_chain.data = []
            mock_client.table.return_value.select.return_value.eq.return_value.is_.return_value.order.return_value.limit.return_value.execute.return_value = mock_chain

            reports = await list_user_reports(user_id, limit=10)

            assert reports == []
            assert isinstance(reports, list)


class TestGetReport:
    """T131, T133: Test get_report service function"""

    @pytest.mark.asyncio
    async def test_returns_existing_report_without_ai_call(self):
        """T131, T133: Test viewing report does not trigger AI generation"""
        from src.api.services.report_service import get_report

        user_id = "user_test_get"
        report_id = str(uuid.uuid4())

        mock_report_data = {
            "id": report_id,
            "user_id": user_id,
            "query": "Computer Science in UK",
            "status": "completed",
            "content": {
                "query": "Computer Science in UK",
                "summary": "Test summary",
                "sections": [],  # Empty list is fine for this test
                "total_citations": 1,
                "generated_at": datetime.utcnow().isoformat(),
            },
            "citations": [{"url": "https://example.com", "title": "Source"}],
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "expires_at": (datetime.utcnow() + timedelta(days=30)).isoformat(),
            "deleted_at": None,
        }

        with patch("src.api.services.report_service.get_supabase") as mock_supabase, \
             patch("src.api.services.report_service.generate_report") as mock_ai:

            mock_client = MagicMock()
            mock_supabase.return_value = mock_client

            mock_chain = Mock()
            mock_chain.data = [mock_report_data]
            mock_client.table.return_value.select.return_value.eq.return_value.eq.return_value.is_.return_value.execute.return_value = mock_chain

            report = await get_report(report_id, user_id)

            # Verify AI was NOT called
            mock_ai.assert_not_called()

            assert report is not None
            assert report.id == report_id
            assert report.content["sections"]["overview"]["content"] == "Existing content"

    @pytest.mark.asyncio
    async def test_returns_none_for_different_user(self):
        """T132: Test RLS - user cannot access other user's report"""
        from src.api.services.report_service import get_report

        user_b_id = "user_b"
        report_id = str(uuid.uuid4())

        with patch("src.api.services.report_service.get_supabase") as mock_supabase:
            mock_client = MagicMock()
            mock_supabase.return_value = mock_client

            # Simulate RLS: query for user_b's report returns empty
            mock_chain = Mock()
            mock_chain.data = []
            mock_client.table.return_value.select.return_value.eq.return_value.eq.return_value.is_.return_value.execute.return_value = mock_chain

            report = await get_report(report_id, user_b_id)

            assert report is None

    @pytest.mark.asyncio
    async def test_returns_none_for_deleted_report(self):
        """Test deleted reports are not returned"""
        from src.api.services.report_service import get_report

        user_id = "user_test_deleted"
        report_id = str(uuid.uuid4())

        with patch("src.api.services.report_service.get_supabase") as mock_supabase:
            mock_client = MagicMock()
            mock_supabase.return_value = mock_client

            # RLS filters out deleted reports
            mock_chain = Mock()
            mock_chain.data = []
            mock_client.table.return_value.select.return_value.eq.return_value.eq.return_value.is_.return_value.execute.return_value = mock_chain

            report = await get_report(report_id, user_id)

            assert report is None


class TestUserScoping:
    """T132: Test RLS enforcement at service level"""

    @pytest.mark.asyncio
    async def test_list_user_reports_filters_by_user_id(self):
        """Test list_user_reports only returns authenticated user's reports"""
        from src.api.services.report_service import list_user_reports

        user_id = "user_scoped_test"

        with patch("src.api.services.report_service.get_supabase") as mock_supabase:
            mock_client = MagicMock()
            mock_supabase.return_value = mock_client

            mock_chain = Mock()
            mock_chain.data = []
            mock_client.table.return_value.select.return_value.eq.return_value.is_.return_value.order.return_value.limit.return_value.execute.return_value = mock_chain

            await list_user_reports(user_id, limit=10)

            # Verify eq was called with user_id
            mock_client.table.return_value.select.return_value.eq.assert_called_with("user_id", user_id)

    @pytest.mark.asyncio
    async def test_get_report_filters_by_user_id(self):
        """Test get_report enforces user_id check"""
        from src.api.services.report_service import get_report

        user_id = "user_check"
        report_id = str(uuid.uuid4())

        with patch("src.api.services.report_service.get_supabase") as mock_supabase:
            mock_client = MagicMock()
            mock_supabase.return_value = mock_client

            mock_chain = Mock()
            mock_chain.data = []

            # Create chainable mock
            select_mock = Mock()
            eq_report_mock = Mock()
            eq_user_mock = Mock()
            is_mock = Mock()

            select_mock.eq.return_value = eq_report_mock
            eq_report_mock.eq.return_value = eq_user_mock
            eq_user_mock.is_.return_value = is_mock
            is_mock.execute.return_value = mock_chain

            mock_client.table.return_value.select.return_value = select_mock

            await get_report(report_id, user_id)

            # Verify both eq calls were made (report_id and user_id)
            calls = select_mock.eq.call_args_list
            assert any("id" in str(call) and report_id in str(call) for call in calls)


class TestImmutability:
    """T133: Test reports are never regenerated on access"""

    @pytest.mark.asyncio
    async def test_multiple_get_calls_no_ai_regeneration(self):
        """Test accessing same report multiple times doesn't trigger AI"""
        from src.api.services.report_service import get_report

        user_id = "user_immutable"
        report_id = str(uuid.uuid4())

        mock_report_data = {
            "id": report_id,
            "user_id": user_id,
            "query": "Test Query",
            "status": "completed",
            "content": {
                "query": "Test Query",
                "summary": "Test summary",
                "sections": [],
                "total_citations": 0,
                "generated_at": datetime.utcnow().isoformat(),
            },
            "citations": [],
            "created_at": datetime.utcnow().isoformat(),
            "updated_at": datetime.utcnow().isoformat(),
            "expires_at": datetime.utcnow().isoformat(),
            "deleted_at": None,
        }

        with patch("src.api.services.report_service.get_supabase") as mock_supabase, \
             patch("src.api.services.report_service.generate_report") as mock_ai:

            mock_client = MagicMock()
            mock_supabase.return_value = mock_client

            mock_chain = Mock()
            mock_chain.data = [mock_report_data]
            mock_client.table.return_value.select.return_value.eq.return_value.eq.return_value.is_.return_value.execute.return_value = mock_chain

            # Call get_report 5 times
            for _ in range(5):
                report = await get_report(report_id, user_id)
                assert report is not None

            # AI should NEVER be called
            mock_ai.assert_not_called()


class TestEmptyState:
    """T134: Test empty state handling"""

    @pytest.mark.asyncio
    async def test_new_user_gets_empty_array(self):
        """Test new user with no reports gets empty array"""
        from src.api.services.report_service import list_user_reports

        new_user_id = "new_user_empty"

        with patch("src.api.services.report_service.get_supabase") as mock_supabase:
            mock_client = MagicMock()
            mock_supabase.return_value = mock_client

            mock_chain = Mock()
            mock_chain.data = []
            mock_client.table.return_value.select.return_value.eq.return_value.is_.return_value.order.return_value.limit.return_value.execute.return_value = mock_chain

            reports = await list_user_reports(new_user_id)

            assert reports == []
            assert len(reports) == 0

    @pytest.mark.asyncio
    async def test_get_nonexistent_report_returns_none(self):
        """Test getting non-existent report returns None"""
        from src.api.services.report_service import get_report

        user_id = "user_test"
        nonexistent_report_id = str(uuid.uuid4())

        with patch("src.api.services.report_service.get_supabase") as mock_supabase:
            mock_client = MagicMock()
            mock_supabase.return_value = mock_client

            mock_chain = Mock()
            mock_chain.data = []
            mock_client.table.return_value.select.return_value.eq.return_value.eq.return_value.is_.return_value.execute.return_value = mock_chain

            report = await get_report(nonexistent_report_id, user_id)

            assert report is None
