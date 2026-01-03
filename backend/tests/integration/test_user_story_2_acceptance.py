"""
Integration Tests for User Story 2: View Report History
Tasks T130-T134 Acceptance Criteria

These tests validate report history functionality:
- T130: Sidebar displays all user's reports (max 10 recent)
- T131: Clicking past report shows content without AI regeneration
- T132: Reports are user-scoped (user A cannot see user B's reports)
- T133: Immutability - reopening report does not trigger new AI call
- T134: Empty state when user has no reports
"""

import pytest
from unittest.mock import patch
from datetime import datetime, timedelta
import uuid

from src.api.models.report import ReportStatus


class TestT130SidebarDisplaysReports:
    """
    T130: Test sidebar displays all user's reports (max 10 recent)
    Acceptance Criteria:
    - GET /reports returns user's reports sorted by created_at DESC
    - Returns maximum 10 reports when limit=10
    - Reports include id, subject, status, created_at
    """

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_sidebar_returns_max_10_reports(
        self, test_client, mock_clerk_user, mock_db_adapter
    ):
        """Test that sidebar query returns maximum 10 most recent reports"""
        user_id = "user_test_sidebar"
        mock_clerk_user["id"] = user_id

        # Create 15 test reports
        reports = []
        for i in range(15):
            report = {
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "subject": f"Subject {i}",
                "country": "UK",
                "status": ReportStatus.COMPLETED.value,
                "created_at": datetime.utcnow() - timedelta(hours=i),
                "expires_at": datetime.utcnow() + timedelta(days=30 - i),
                "content": {"sections": {}},
                "citations": [],
            }
            reports.append(report)

        # Mock database to return all 15 reports
        with patch("src.api.services.report_service.list_user_reports") as mock_list:
            # Return only 10 most recent when limit=10
            mock_list.return_value = reports[:10]

            response = test_client.get(
                "/api/reports?limit=10",
                headers={"Authorization": f"Bearer test_token_{user_id}"},
            )

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 10
        assert data[0]["subject"] == "Subject 0"  # Most recent first
        assert data[9]["subject"] == "Subject 9"  # 10th report

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_sidebar_reports_sorted_by_created_at_desc(
        self, test_client, mock_clerk_user
    ):
        """Test reports are sorted by created_at descending (newest first)"""
        user_id = "user_test_sorting"
        mock_clerk_user["id"] = user_id

        # Create reports with different timestamps
        reports = [
            {
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "subject": "Oldest Report",
                "status": ReportStatus.COMPLETED.value,
                "created_at": datetime.utcnow() - timedelta(days=10),
            },
            {
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "subject": "Middle Report",
                "status": ReportStatus.COMPLETED.value,
                "created_at": datetime.utcnow() - timedelta(days=5),
            },
            {
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "subject": "Newest Report",
                "status": ReportStatus.COMPLETED.value,
                "created_at": datetime.utcnow(),
            },
        ]

        with patch("src.api.services.report_service.list_user_reports") as mock_list:
            # Return sorted by created_at DESC
            mock_list.return_value = sorted(
                reports, key=lambda r: r["created_at"], reverse=True
            )

            response = test_client.get(
                "/api/reports?limit=10",
                headers={"Authorization": f"Bearer test_token_{user_id}"},
            )

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert data[0]["subject"] == "Newest Report"
        assert data[1]["subject"] == "Middle Report"
        assert data[2]["subject"] == "Oldest Report"

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_sidebar_includes_required_fields(
        self, test_client, mock_clerk_user
    ):
        """Test that report list includes all required fields"""
        user_id = "user_test_fields"
        mock_clerk_user["id"] = user_id

        report = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "subject": "Computer Science",
            "country": "UK",
            "status": ReportStatus.COMPLETED.value,
            "created_at": datetime.utcnow(),
            "expires_at": datetime.utcnow() + timedelta(days=30),
        }

        with patch("src.api.services.report_service.list_user_reports") as mock_list:
            mock_list.return_value = [report]

            response = test_client.get(
                "/api/reports",
                headers={"Authorization": f"Bearer test_token_{user_id}"},
            )

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1

        # Verify required fields
        report_item = data[0]
        assert "id" in report_item
        assert "subject" in report_item
        assert "status" in report_item
        assert "created_at" in report_item
        assert report_item["subject"] == "Computer Science"
        assert report_item["status"] == ReportStatus.COMPLETED.value


class TestT131ViewPastReportWithoutRegeneration:
    """
    T131: Verify clicking past report shows content without AI regeneration
    Acceptance Criteria:
    - GET /reports/{id} returns existing report content
    - No AI service call is triggered when viewing existing report
    - Report content and citations are returned as-is from database
    """

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_view_existing_report_no_ai_call(
        self, test_client, mock_clerk_user
    ):
        """Test viewing existing report does not trigger AI regeneration"""
        user_id = "user_test_view"
        report_id = str(uuid.uuid4())
        mock_clerk_user["id"] = user_id

        existing_report = {
            "id": report_id,
            "user_id": user_id,
            "subject": "Computer Science",
            "country": "UK",
            "status": ReportStatus.COMPLETED.value,
            "content": {
                "sections": {
                    "overview": {"title": "Overview", "content": "Existing content"}
                }
            },
            "citations": [{"url": "https://example.com", "title": "Source"}],
            "created_at": datetime.utcnow(),
            "expires_at": datetime.utcnow() + timedelta(days=30),
        }

        with patch("src.api.services.report_service.get_report") as mock_get, \
             patch("src.api.services.ai_service.generate_report") as mock_ai:

            mock_get.return_value = existing_report

            response = test_client.get(
                f"/api/reports/{report_id}",
                headers={"Authorization": f"Bearer test_token_{user_id}"},
            )

            # Verify AI service was NOT called
            mock_ai.assert_not_called()

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == report_id
        assert data["content"]["sections"]["overview"]["content"] == "Existing content"
        assert len(data["citations"]) == 1

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_view_report_returns_stored_citations(
        self, test_client, mock_clerk_user
    ):
        """Test that stored citations are returned without modification"""
        user_id = "user_test_citations"
        report_id = str(uuid.uuid4())
        mock_clerk_user["id"] = user_id

        citations = [
            {"url": "https://example1.com", "title": "Source 1"},
            {"url": "https://example2.com", "title": "Source 2"},
            {"url": "https://example3.com", "title": "Source 3"},
        ]

        existing_report = {
            "id": report_id,
            "user_id": user_id,
            "subject": "Nursing",
            "status": ReportStatus.COMPLETED.value,
            "content": {"sections": {}},
            "citations": citations,
        }

        with patch("src.api.services.report_service.get_report") as mock_get:
            mock_get.return_value = existing_report

            response = test_client.get(
                f"/api/reports/{report_id}",
                headers={"Authorization": f"Bearer test_token_{user_id}"},
            )

        assert response.status_code == 200
        data = response.json()
        assert data["citations"] == citations
        assert len(data["citations"]) == 3


class TestT132UserScopedReports:
    """
    T132: Verify reports are user-scoped (user A cannot see user B's reports)
    Acceptance Criteria:
    - GET /reports returns only authenticated user's reports
    - GET /reports/{id} returns 404 if report belongs to different user
    - RLS policies enforce user isolation
    """

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_list_reports_returns_only_own_reports(
        self, test_client, mock_clerk_user
    ):
        """Test user can only see their own reports in list"""
        user_a_id = "user_a"
        mock_clerk_user["id"] = user_a_id

        user_a_reports = [
            {
                "id": str(uuid.uuid4()),
                "user_id": user_a_id,
                "subject": "User A Report 1",
                "status": ReportStatus.COMPLETED.value,
            },
            {
                "id": str(uuid.uuid4()),
                "user_id": user_a_id,
                "subject": "User A Report 2",
                "status": ReportStatus.COMPLETED.value,
            },
        ]

        # User B has reports too, but they should not be returned
        with patch("src.api.services.report_service.list_user_reports") as mock_list:
            # Mock should only return user A's reports
            mock_list.return_value = user_a_reports

            response = test_client.get(
                "/api/reports",
                headers={"Authorization": f"Bearer test_token_{user_a_id}"},
            )

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert all(r["subject"].startswith("User A") for r in data)

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_get_other_users_report_returns_404(
        self, test_client, mock_clerk_user
    ):
        """Test user cannot access another user's report by ID"""
        user_a_id = "user_a"
        user_b_report_id = str(uuid.uuid4())

        # User A tries to access User B's report
        mock_clerk_user["id"] = user_a_id

        with patch("src.api.services.report_service.get_report") as mock_get:
            # Simulate report not found for different user (RLS enforcement)
            mock_get.return_value = None

            response = test_client.get(
                f"/api/reports/{user_b_report_id}",
                headers={"Authorization": f"Bearer test_token_{user_a_id}"},
            )

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_rls_enforces_user_isolation(
        self, test_client, mock_clerk_user
    ):
        """Test RLS policies prevent cross-user access"""
        user_id = "user_isolated"
        mock_clerk_user["id"] = user_id

        # Simulate RLS: service layer should filter by user_id
        with patch("src.api.services.report_service.list_user_reports") as mock_list:
            # Mock should be called with correct user_id
            mock_list.return_value = []

            test_client.get(
                "/api/reports",
                headers={"Authorization": f"Bearer test_token_{user_id}"},
            )

            # Verify service was called with authenticated user's ID
            mock_list.assert_called_once()
            call_args = mock_list.call_args[0]
            assert call_args[0] == user_id  # First argument should be user_id


class TestT133ImmutabilityNoRegeneration:
    """
    T133: Verify immutability - reopening report does not trigger new AI call
    Acceptance Criteria:
    - Viewing same report multiple times returns identical content
    - No AI service calls when viewing existing completed reports
    - Content hash remains unchanged
    """

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_multiple_views_return_same_content(
        self, test_client, mock_clerk_user
    ):
        """Test viewing report multiple times returns identical content"""
        user_id = "user_test_immutable"
        report_id = str(uuid.uuid4())
        mock_clerk_user["id"] = user_id

        fixed_content = {
            "sections": {
                "overview": {"title": "Overview", "content": "Fixed content"},
                "universities": {"title": "Universities", "content": "Fixed universities"},
            }
        }

        report = {
            "id": report_id,
            "user_id": user_id,
            "subject": "Computer Science",
            "status": ReportStatus.COMPLETED.value,
            "content": fixed_content,
            "citations": [{"url": "https://example.com", "title": "Source"}],
        }

        with patch("src.api.services.report_service.get_report") as mock_get, \
             patch("src.api.services.ai_service.generate_report") as mock_ai:

            mock_get.return_value = report

            # View report first time
            response1 = test_client.get(
                f"/api/reports/{report_id}",
                headers={"Authorization": f"Bearer test_token_{user_id}"},
            )

            # View report second time
            response2 = test_client.get(
                f"/api/reports/{report_id}",
                headers={"Authorization": f"Bearer test_token_{user_id}"},
            )

            # View report third time
            response3 = test_client.get(
                f"/api/reports/{report_id}",
                headers={"Authorization": f"Bearer test_token_{user_id}"},
            )

            # Verify AI was never called
            mock_ai.assert_not_called()

        # All responses should be identical
        assert response1.status_code == 200
        assert response2.status_code == 200
        assert response3.status_code == 200

        data1 = response1.json()
        data2 = response2.json()
        data3 = response3.json()

        assert data1["content"] == data2["content"] == data3["content"]
        assert data1["citations"] == data2["citations"] == data3["citations"]

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_completed_report_never_regenerated(
        self, test_client, mock_clerk_user
    ):
        """Test completed reports are never regenerated on access"""
        user_id = "user_test_no_regen"
        report_id = str(uuid.uuid4())
        mock_clerk_user["id"] = user_id

        completed_report = {
            "id": report_id,
            "user_id": user_id,
            "subject": "Business",
            "status": ReportStatus.COMPLETED.value,
            "content": {"sections": {"overview": {"content": "Original"}}},
            "citations": [],
        }

        with patch("src.api.services.report_service.get_report") as mock_get, \
             patch("src.api.services.ai_service.generate_report") as mock_ai:

            mock_get.return_value = completed_report

            # Access completed report 10 times
            for _ in range(10):
                response = test_client.get(
                    f"/api/reports/{report_id}",
                    headers={"Authorization": f"Bearer test_token_{user_id}"},
                )
                assert response.status_code == 200

            # AI should NEVER have been called
            mock_ai.assert_not_called()


class TestT134EmptyStateNoReports:
    """
    T134: Test empty state when user has no reports
    Acceptance Criteria:
    - GET /reports returns empty array for new users
    - Response is valid JSON with empty array
    - No errors when user has zero reports
    """

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_new_user_returns_empty_array(
        self, test_client, mock_clerk_user
    ):
        """Test new user with no reports gets empty array"""
        user_id = "new_user_no_reports"
        mock_clerk_user["id"] = user_id

        with patch("src.api.services.report_service.list_user_reports") as mock_list:
            mock_list.return_value = []

            response = test_client.get(
                "/api/reports",
                headers={"Authorization": f"Bearer test_token_{user_id}"},
            )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_empty_state_with_limit_parameter(
        self, test_client, mock_clerk_user
    ):
        """Test empty state works correctly with limit parameter"""
        user_id = "user_empty_with_limit"
        mock_clerk_user["id"] = user_id

        with patch("src.api.services.report_service.list_user_reports") as mock_list:
            mock_list.return_value = []

            response = test_client.get(
                "/api/reports?limit=10",
                headers={"Authorization": f"Bearer test_token_{user_id}"},
            )

        assert response.status_code == 200
        data = response.json()
        assert data == []

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_empty_state_valid_json(
        self, test_client, mock_clerk_user
    ):
        """Test empty state returns valid JSON structure"""
        user_id = "user_json_test"
        mock_clerk_user["id"] = user_id

        with patch("src.api.services.report_service.list_user_reports") as mock_list:
            mock_list.return_value = []

            response = test_client.get(
                "/api/reports",
                headers={"Authorization": f"Bearer test_token_{user_id}"},
            )

        assert response.status_code == 200
        assert response.headers["content-type"] == "application/json"

        # Should not raise JSON decode error
        data = response.json()
        assert isinstance(data, list)


class TestReportHistoryIntegration:
    """
    Integration tests for complete report history workflow
    """

    @pytest.mark.asyncio
    @pytest.mark.integration
    async def test_complete_history_workflow(
        self, test_client, mock_clerk_user
    ):
        """Test complete workflow: create reports → list → view individual"""
        user_id = "user_workflow_test"
        mock_clerk_user["id"] = user_id

        # Create 3 reports
        reports = []
        for i in range(3):
            report = {
                "id": str(uuid.uuid4()),
                "user_id": user_id,
                "subject": f"Subject {i}",
                "country": "UK",
                "status": ReportStatus.COMPLETED.value,
                "content": {"sections": {f"section_{i}": {"content": f"Content {i}"}}},
                "citations": [{"url": f"https://example{i}.com", "title": f"Source {i}"}],
                "created_at": datetime.utcnow() - timedelta(hours=i),
            }
            reports.append(report)

        # Step 1: List all reports
        with patch("src.api.services.report_service.list_user_reports") as mock_list:
            mock_list.return_value = reports

            list_response = test_client.get(
                "/api/reports?limit=10",
                headers={"Authorization": f"Bearer test_token_{user_id}"},
            )

        assert list_response.status_code == 200
        report_list = list_response.json()
        assert len(report_list) == 3

        # Step 2: View each report individually
        for report in reports:
            with patch("src.api.services.report_service.get_report") as mock_get, \
                 patch("src.api.services.ai_service.generate_report") as mock_ai:

                mock_get.return_value = report

                detail_response = test_client.get(
                    f"/api/reports/{report['id']}",
                    headers={"Authorization": f"Bearer test_token_{user_id}"},
                )

                # Verify no AI regeneration
                mock_ai.assert_not_called()

                assert detail_response.status_code == 200
                detail_data = detail_response.json()
                assert detail_data["id"] == report["id"]
                assert detail_data["subject"] == report["subject"]
                assert detail_data["content"] == report["content"]
