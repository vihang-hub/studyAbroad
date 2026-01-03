"""
Tests for report service (report lifecycle management)
"""
import pytest
from unittest.mock import patch, Mock, MagicMock
from datetime import datetime, timedelta
from src.api.services.report_service import (
    create_report,
    trigger_report_generation,
    get_report,
    list_user_reports,
    soft_delete_report,
)
from src.api.models.report import Report, ReportStatus, CreateReportResponse, ReportListItem


class TestCreateReport:
    """Test suite for report creation"""

    @pytest.mark.asyncio
    async def test_create_report_success(self, mock_user_id, sample_uk_query):
        """Test successful report creation"""
        with patch("src.api.services.report_service.get_supabase") as mock_get_supabase, \
             patch("src.api.services.report_service.settings") as mock_settings:

            mock_settings.REPORT_EXPIRY_DAYS = 30

            mock_supabase = MagicMock()
            mock_supabase.table.return_value = mock_supabase
            mock_supabase.insert.return_value = mock_supabase
            mock_supabase.execute.return_value = Mock(data=[{"id": "report_12345"}])
            mock_get_supabase.return_value = mock_supabase

            result = await create_report(mock_user_id, sample_uk_query)

            assert isinstance(result, CreateReportResponse)
            assert result.report_id is not None
            assert result.status == ReportStatus.PENDING
            assert result.estimated_completion_seconds == 60

            mock_supabase.table.assert_called_with("reports")
            mock_supabase.insert.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_report_sets_expiry(self, mock_user_id, sample_uk_query):
        """Test report creation sets 30-day expiry"""
        with patch("src.api.services.report_service.get_supabase") as mock_get_supabase, \
             patch("src.api.services.report_service.settings") as mock_settings:

            mock_settings.REPORT_EXPIRY_DAYS = 30

            mock_supabase = MagicMock()
            mock_supabase.table.return_value = mock_supabase
            mock_supabase.insert.return_value = mock_supabase
            mock_supabase.execute.return_value = Mock(data=[{"id": "report_12345"}])
            mock_get_supabase.return_value = mock_supabase

            await create_report(mock_user_id, sample_uk_query)

            insert_data = mock_supabase.insert.call_args[0][0]
            assert "expires_at" in insert_data

            # Verify expiry is approximately 30 days from now
            expires_at = datetime.fromisoformat(insert_data["expires_at"])
            expected_expiry = datetime.utcnow() + timedelta(days=30)
            # Allow 1 minute tolerance
            assert abs((expires_at - expected_expiry).total_seconds()) < 60


class TestTriggerReportGeneration:
    """Test suite for triggering report generation"""

    @pytest.mark.asyncio
    async def test_trigger_report_generation_success(self, mock_report_id, sample_report_data):
        """Test successful report generation trigger"""
        with patch("src.api.services.report_service.get_supabase") as mock_get_supabase, \
             patch("src.api.services.report_service.generate_report") as mock_generate:

            # Mock report content
            from src.api.models.report import ReportContent
            mock_content = Mock(spec=ReportContent)
            mock_content.dict.return_value = {"query": "test", "sections": []}
            mock_generate.return_value = mock_content

            # Mock Supabase
            mock_supabase = MagicMock()
            mock_supabase.table.return_value = mock_supabase
            mock_supabase.select.return_value = mock_supabase
            mock_supabase.update.return_value = mock_supabase
            mock_supabase.eq.return_value = mock_supabase
            mock_supabase.execute.return_value = Mock(data=[sample_report_data])
            mock_get_supabase.return_value = mock_supabase

            await trigger_report_generation(mock_report_id)

            # Verify status updates: pending -> generating -> completed
            update_calls = [call[0][0] for call in mock_supabase.update.call_args_list]
            assert any(
                call.get("status") == ReportStatus.GENERATING.value for call in update_calls
            )
            assert any(call.get("status") == ReportStatus.COMPLETED.value for call in update_calls)

    @pytest.mark.asyncio
    async def test_trigger_report_generation_not_found(self, mock_report_id):
        """Test report generation fails when report not found"""
        with patch("src.api.services.report_service.get_supabase") as mock_get_supabase:
            mock_supabase = MagicMock()
            mock_supabase.table.return_value = mock_supabase
            mock_supabase.select.return_value = mock_supabase
            mock_supabase.eq.return_value = mock_supabase
            mock_supabase.execute.return_value = Mock(data=[])
            mock_get_supabase.return_value = mock_supabase

            with pytest.raises(Exception) as exc_info:
                await trigger_report_generation(mock_report_id)

            assert "not found" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_trigger_report_generation_ai_failure(self, mock_report_id, sample_report_data):
        """Test report generation handles AI failures"""
        with patch("src.api.services.report_service.get_supabase") as mock_get_supabase, \
             patch("src.api.services.report_service.generate_report") as mock_generate:

            mock_generate.side_effect = Exception("AI generation failed")

            mock_supabase = MagicMock()
            mock_supabase.table.return_value = mock_supabase
            mock_supabase.select.return_value = mock_supabase
            mock_supabase.update.return_value = mock_supabase
            mock_supabase.eq.return_value = mock_supabase
            mock_supabase.execute.return_value = Mock(data=[sample_report_data])
            mock_get_supabase.return_value = mock_supabase

            with pytest.raises(Exception):
                await trigger_report_generation(mock_report_id)

            # Verify status set to FAILED
            update_calls = [call[0][0] for call in mock_supabase.update.call_args_list]
            assert any(call.get("status") == ReportStatus.FAILED.value for call in update_calls)


class TestGetReport:
    """Test suite for retrieving reports"""

    @pytest.mark.asyncio
    async def test_get_report_success(self, mock_report_id, mock_user_id, sample_report_data):
        """Test successful report retrieval"""
        with patch("src.api.services.report_service.get_supabase") as mock_get_supabase:
            mock_supabase = MagicMock()
            mock_supabase.table.return_value = mock_supabase
            mock_supabase.select.return_value = mock_supabase
            mock_supabase.eq.return_value = mock_supabase
            mock_supabase.is_.return_value = mock_supabase
            mock_supabase.execute.return_value = Mock(data=[sample_report_data])
            mock_get_supabase.return_value = mock_supabase

            result = await get_report(mock_report_id, mock_user_id)

            assert result is not None
            assert isinstance(result, Report)
            assert result.id == mock_report_id

    @pytest.mark.asyncio
    async def test_get_report_not_found(self, mock_report_id, mock_user_id):
        """Test report retrieval when not found"""
        with patch("src.api.services.report_service.get_supabase") as mock_get_supabase:
            mock_supabase = MagicMock()
            mock_supabase.table.return_value = mock_supabase
            mock_supabase.select.return_value = mock_supabase
            mock_supabase.eq.return_value = mock_supabase
            mock_supabase.is_.return_value = mock_supabase
            mock_supabase.execute.return_value = Mock(data=[])
            mock_get_supabase.return_value = mock_supabase

            result = await get_report(mock_report_id, mock_user_id)

            assert result is None

    @pytest.mark.asyncio
    async def test_get_report_ownership_check(self, mock_report_id, sample_report_data):
        """Test report retrieval enforces user ownership"""
        with patch("src.api.services.report_service.get_supabase") as mock_get_supabase:
            mock_supabase = MagicMock()
            mock_supabase.table.return_value = mock_supabase
            mock_supabase.select.return_value = mock_supabase
            mock_supabase.eq.return_value = mock_supabase
            mock_supabase.is_.return_value = mock_supabase
            mock_get_supabase.return_value = mock_supabase

            # Try to get report with different user ID
            await get_report(mock_report_id, "different_user_id")

            # Verify query filters by user_id
            eq_calls = mock_supabase.eq.call_args_list
            assert any(
                call[0][0] == "user_id" and call[0][1] == "different_user_id" for call in eq_calls
            )


class TestListUserReports:
    """Test suite for listing user reports"""

    @pytest.mark.asyncio
    async def test_list_user_reports_success(self, mock_user_id):
        """Test successful report listing"""
        mock_reports = [
            {
                "id": f"report_{i}",
                "query": f"Query {i}",
                "status": "completed",
                "created_at": "2024-12-29T12:00:00Z",
                "expires_at": "2025-01-28T12:00:00Z",
            }
            for i in range(3)
        ]

        with patch("src.api.services.report_service.get_supabase") as mock_get_supabase:
            mock_supabase = MagicMock()
            mock_supabase.table.return_value = mock_supabase
            mock_supabase.select.return_value = mock_supabase
            mock_supabase.eq.return_value = mock_supabase
            mock_supabase.is_.return_value = mock_supabase
            mock_supabase.order.return_value = mock_supabase
            mock_supabase.limit.return_value = mock_supabase
            mock_supabase.execute.return_value = Mock(data=mock_reports)
            mock_get_supabase.return_value = mock_supabase

            result = await list_user_reports(mock_user_id)

            assert len(result) == 3
            assert all(isinstance(item, ReportListItem) for item in result)

    @pytest.mark.asyncio
    async def test_list_user_reports_respects_limit(self, mock_user_id):
        """Test report listing respects limit parameter"""
        with patch("src.api.services.report_service.get_supabase") as mock_get_supabase:
            mock_supabase = MagicMock()
            mock_supabase.table.return_value = mock_supabase
            mock_supabase.select.return_value = mock_supabase
            mock_supabase.eq.return_value = mock_supabase
            mock_supabase.is_.return_value = mock_supabase
            mock_supabase.order.return_value = mock_supabase
            mock_supabase.limit.return_value = mock_supabase
            mock_supabase.execute.return_value = Mock(data=[])
            mock_get_supabase.return_value = mock_supabase

            await list_user_reports(mock_user_id, limit=10)

            mock_supabase.limit.assert_called_once_with(10)

    @pytest.mark.asyncio
    async def test_list_user_reports_ordered_by_created_at(self, mock_user_id):
        """Test reports are ordered by creation date (descending)"""
        with patch("src.api.services.report_service.get_supabase") as mock_get_supabase:
            mock_supabase = MagicMock()
            mock_supabase.table.return_value = mock_supabase
            mock_supabase.select.return_value = mock_supabase
            mock_supabase.eq.return_value = mock_supabase
            mock_supabase.is_.return_value = mock_supabase
            mock_supabase.order.return_value = mock_supabase
            mock_supabase.limit.return_value = mock_supabase
            mock_supabase.execute.return_value = Mock(data=[])
            mock_get_supabase.return_value = mock_supabase

            await list_user_reports(mock_user_id)

            mock_supabase.order.assert_called_once_with("created_at", desc=True)


class TestSoftDeleteReport:
    """Test suite for soft deleting reports"""

    @pytest.mark.asyncio
    async def test_soft_delete_report_success(self, mock_report_id, mock_user_id):
        """Test successful soft deletion"""
        with patch("src.api.services.report_service.get_supabase") as mock_get_supabase:
            mock_supabase = MagicMock()
            mock_supabase.table.return_value = mock_supabase
            mock_supabase.update.return_value = mock_supabase
            mock_supabase.eq.return_value = mock_supabase
            mock_supabase.execute.return_value = Mock(data=[{"id": mock_report_id}])
            mock_get_supabase.return_value = mock_supabase

            result = await soft_delete_report(mock_report_id, mock_user_id)

            assert result is True
            # Verify deleted_at timestamp set
            update_data = mock_supabase.update.call_args[0][0]
            assert "deleted_at" in update_data

    @pytest.mark.asyncio
    async def test_soft_delete_report_not_found(self, mock_report_id, mock_user_id):
        """Test soft deletion when report not found"""
        with patch("src.api.services.report_service.get_supabase") as mock_get_supabase:
            mock_supabase = MagicMock()
            mock_supabase.table.return_value = mock_supabase
            mock_supabase.update.return_value = mock_supabase
            mock_supabase.eq.return_value = mock_supabase
            mock_supabase.execute.return_value = Mock(data=[])
            mock_get_supabase.return_value = mock_supabase

            result = await soft_delete_report(mock_report_id, mock_user_id)

            assert result is False

    @pytest.mark.asyncio
    async def test_soft_delete_enforces_ownership(self, mock_report_id):
        """Test soft deletion enforces user ownership"""
        with patch("src.api.services.report_service.get_supabase") as mock_get_supabase:
            mock_supabase = MagicMock()
            mock_supabase.table.return_value = mock_supabase
            mock_supabase.update.return_value = mock_supabase
            mock_supabase.eq.return_value = mock_supabase
            mock_supabase.execute.return_value = Mock(data=[])
            mock_get_supabase.return_value = mock_supabase

            await soft_delete_report(mock_report_id, "other_user_id")

            # Verify both report_id and user_id filters applied
            eq_calls = mock_supabase.eq.call_args_list
            assert any(call[0][0] == "id" for call in eq_calls)
            assert any(call[0][0] == "user_id" for call in eq_calls)
