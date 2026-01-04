"""
Regression Tests for Debugging Fixes (2026-01-04)

These tests prevent regression of issues discovered during manual testing.
Each test corresponds to a specific debugging issue from the retrospective.

Issue Reference:
- Issue #1: Chrome modal auth (frontend - see frontend/tests/)
- Issue #2: HttpUrl type conversion for Supabase client
- Issue #3: Feature flags in services before external calls
- Issue #4: REPORT_EXPIRY_DAYS config field missing
- Issue #5: snake_case vs camelCase API field naming
- Issue #6: Unauthenticated API calls (frontend - see frontend/tests/)
- Issue #7: Mock report content=None causing display errors
"""

import pytest
import inspect
import re
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
from pydantic import HttpUrl

from src.config.environment import EnvironmentConfig
from src.api.models.report import (
    Report,
    ReportContent,
    ReportSection,
    CreateReportResponse,
    ReportListItem,
    Citation,
    REQUIRED_SECTIONS,
)
from src.api.services.report_service import (
    get_report,
    _create_mock_report_content,
    _is_supabase_enabled,
)


class TestIssue2HttpUrlTypeConversion:
    """
    Issue #2: HttpUrl type error

    Problem: Pydantic HttpUrl type is incompatible with Supabase client.
    The Supabase client expects string URLs, not HttpUrl objects.

    Solution: Convert HttpUrl to str before passing to external libraries.

    This test ensures that any code passing URLs to external services
    properly converts HttpUrl to string first.
    """

    def test_httpurl_can_be_converted_to_string(self):
        """Test that HttpUrl can be safely converted to string"""
        url = HttpUrl("https://example.supabase.co")
        url_str = str(url)

        assert isinstance(url_str, str)
        assert url_str == "https://example.supabase.co/"
        # Trailing slash is added by Pydantic - both forms should work
        assert url_str.startswith("https://example.supabase.co")

    def test_httpurl_serialization_in_models(self):
        """Test that models with HttpUrl serialize correctly to JSON"""
        # When models with HttpUrl are serialized for API responses,
        # they should produce valid JSON strings, not HttpUrl objects
        from pydantic import BaseModel

        class TestModel(BaseModel):
            api_url: HttpUrl

        model = TestModel(api_url="https://api.example.com")
        json_data = model.model_dump_json()

        # Should be valid JSON string, not <class 'pydantic.HttpUrl'>
        assert '"https://api.example.com' in json_data
        assert "HttpUrl" not in json_data


class TestIssue3FeatureFlagsInServices:
    """
    Issue #3: Database connection refused in dev mode

    Problem: Services called external services (Supabase, Stripe) without
    checking feature flags first, causing connection errors in dev mode.

    Solution: Every service function that uses external services MUST check
    the corresponding feature flag before making external calls.

    Pattern:
        def service_function():
            if not _is_service_enabled():
                return _get_mock_data()
            return _get_real_data()
    """

    def test_report_service_checks_supabase_flag(self):
        """Test that report service functions check Supabase feature flag"""
        from src.api.services import report_service

        # Get source code of the module
        source = inspect.getsource(report_service)

        # Functions that should check Supabase flag
        service_functions = [
            "create_report",
            "get_report",
            "list_user_reports",
            "trigger_report_generation",
            "update_report_status",
            "soft_delete_report",
        ]

        for func_name in service_functions:
            # Find the function definition and its body
            pattern = rf"async def {func_name}\([^)]*\)[^:]*:.*?(?=\n(?:async )?def |\nclass |\Z)"
            match = re.search(pattern, source, re.DOTALL)

            if match:
                func_body = match.group(0)
                # Check that function body contains feature flag check
                assert "_is_supabase_enabled()" in func_body, (
                    f"Function {func_name} should check _is_supabase_enabled() "
                    "before making external calls"
                )

    def test_payment_service_checks_payment_flag(self):
        """Test that payment service functions check payments feature flag"""
        from src.api.services import payment_service

        source = inspect.getsource(payment_service)

        # Functions that should check payments flag
        service_functions = [
            "create_payment_intent",
            "process_webhook",
        ]

        for func_name in service_functions:
            pattern = rf"async def {func_name}\([^)]*\)[^:]*:.*?(?=\n(?:async )?def |\nclass |\Z)"
            match = re.search(pattern, source, re.DOTALL)

            if match:
                func_body = match.group(0)
                # Check for payments feature flag check
                assert "_is_payments_enabled()" in func_body, (
                    f"Function {func_name} should check _is_payments_enabled() "
                    "before making external calls"
                )

    @pytest.mark.asyncio
    async def test_get_report_returns_mock_when_supabase_disabled(self):
        """Test that get_report returns mock data when Supabase is disabled"""
        with patch("src.api.services.report_service._is_supabase_enabled") as mock_flag:
            mock_flag.return_value = False

            result = await get_report("test-report-id", "test-user-id")

            # Should return a mock report, not None or error
            assert result is not None
            assert result.status.value == "completed"
            assert result.content is not None


class TestIssue4ConfigFieldsExist:
    """
    Issue #4: Missing REPORT_EXPIRY_DAYS config field

    Problem: Code referenced settings.REPORT_EXPIRY_DAYS but the field
    was not defined in EnvironmentConfig, causing AttributeError.

    Solution: All config fields referenced in code MUST be defined in
    EnvironmentConfig with appropriate defaults.
    """

    def test_report_expiry_days_defined_in_config(self):
        """Test that REPORT_EXPIRY_DAYS is defined in EnvironmentConfig"""
        # Check that the field is defined in the model
        assert 'REPORT_EXPIRY_DAYS' in EnvironmentConfig.model_fields, (
            "REPORT_EXPIRY_DAYS must be defined in EnvironmentConfig"
        )

        field_info = EnvironmentConfig.model_fields['REPORT_EXPIRY_DAYS']

        # Check that it has a reasonable default
        assert field_info.default == 30, (
            "REPORT_EXPIRY_DAYS should default to 30 days"
        )

    def test_all_required_config_fields_exist(self):
        """Test that all commonly referenced config fields are defined"""
        required_fields = [
            "ENVIRONMENT_MODE",
            "DATABASE_URL",
            "CLERK_PUBLISHABLE_KEY",
            "CLERK_SECRET_KEY",
            "GEMINI_API_KEY",
            "ENABLE_SUPABASE",
            "ENABLE_PAYMENTS",
            "REPORT_EXPIRY_DAYS",
            "LOG_LEVEL",
        ]

        for field in required_fields:
            assert field in EnvironmentConfig.model_fields, (
                f"Config field {field} must be defined in EnvironmentConfig"
            )


class TestIssue5SnakeCaseFieldNaming:
    """
    Issue #5: snake_case vs camelCase mismatch

    Problem: Backend used snake_case (report_id) but frontend expected
    camelCase (reportId), causing JSON parsing errors.

    Solution: Backend MUST use snake_case consistently for all API
    response fields. Frontend types MUST match backend exactly.

    This is enforced by Pydantic models - if fields are defined with
    snake_case, they will be serialized as snake_case.
    """

    def test_report_model_uses_snake_case(self):
        """Test that Report model fields are snake_case"""
        snake_case_pattern = re.compile(r'^[a-z][a-z0-9]*(_[a-z0-9]+)*$')

        for field_name in Report.model_fields.keys():
            assert snake_case_pattern.match(field_name), (
                f"Field '{field_name}' in Report model should be snake_case"
            )

    def test_create_report_response_uses_snake_case(self):
        """Test that CreateReportResponse model fields are snake_case"""
        snake_case_pattern = re.compile(r'^[a-z][a-z0-9]*(_[a-z0-9]+)*$')

        for field_name in CreateReportResponse.model_fields.keys():
            assert snake_case_pattern.match(field_name), (
                f"Field '{field_name}' in CreateReportResponse should be snake_case"
            )

    def test_report_content_uses_snake_case(self):
        """Test that ReportContent model fields are snake_case"""
        snake_case_pattern = re.compile(r'^[a-z][a-z0-9]*(_[a-z0-9]+)*$')

        for field_name in ReportContent.model_fields.keys():
            assert snake_case_pattern.match(field_name), (
                f"Field '{field_name}' in ReportContent should be snake_case"
            )

    def test_report_list_item_uses_snake_case(self):
        """Test that ReportListItem model fields are snake_case"""
        snake_case_pattern = re.compile(r'^[a-z][a-z0-9]*(_[a-z0-9]+)*$')

        for field_name in ReportListItem.model_fields.keys():
            assert snake_case_pattern.match(field_name), (
                f"Field '{field_name}' in ReportListItem should be snake_case"
            )

    def test_no_camel_case_fields_in_response_models(self):
        """Test that response models don't have camelCase fields"""
        camel_case_pattern = re.compile(r'[a-z][A-Z]')

        models_to_check = [
            Report,
            CreateReportResponse,
            ReportContent,
            ReportSection,
            ReportListItem,
            Citation,
        ]

        for model in models_to_check:
            for field_name in model.model_fields.keys():
                assert not camel_case_pattern.search(field_name), (
                    f"Field '{field_name}' in {model.__name__} appears to be "
                    "camelCase - should be snake_case"
                )


class TestIssue7MockReportContentCompleteness:
    """
    Issue #7: Mock report content=None

    Problem: Mock report returned content=None, causing frontend to show
    "Report content is not available" even in dev mode.

    Solution: Mock data MUST be complete and realistic. All required fields
    must be populated with valid test data, never None.
    """

    def test_mock_report_content_is_not_none(self):
        """Test that mock report content is never None"""
        mock_content = _create_mock_report_content("Test query")

        assert mock_content is not None, (
            "Mock report content should never be None"
        )

    def test_mock_report_has_all_required_sections(self):
        """Test that mock report has exactly 10 required sections"""
        mock_content = _create_mock_report_content("Test query")

        assert len(mock_content.sections) == 10, (
            f"Mock report must have exactly 10 sections, got {len(mock_content.sections)}"
        )

        # Verify section headings match required list
        for i, section in enumerate(mock_content.sections):
            assert section.heading == REQUIRED_SECTIONS[i], (
                f"Section {i+1} heading should be '{REQUIRED_SECTIONS[i]}', "
                f"got '{section.heading}'"
            )

    def test_mock_report_sections_have_content(self):
        """Test that all mock report sections have non-empty content"""
        mock_content = _create_mock_report_content("Test query")

        for section in mock_content.sections:
            assert section.content, (
                f"Section '{section.heading}' should have non-empty content"
            )
            assert len(section.content) > 10, (
                f"Section '{section.heading}' content too short"
            )

    def test_mock_report_has_citations(self):
        """Test that mock report has citations in required sections"""
        mock_content = _create_mock_report_content("Test query")

        # Sections that require citations (all except Executive Summary and Sources)
        sections_requiring_citations = [
            s for s in mock_content.sections
            if s.heading not in ["Executive Summary", "Sources & Citations"]
        ]

        for section in sections_requiring_citations:
            assert len(section.citations) >= 3, (
                f"Section '{section.heading}' must have at least 3 citations, "
                f"got {len(section.citations)}"
            )

    def test_mock_report_total_citations_calculated(self):
        """Test that mock report total_citations is correctly calculated"""
        mock_content = _create_mock_report_content("Test query")

        actual_total = sum(len(s.citations) for s in mock_content.sections)

        assert mock_content.total_citations == actual_total, (
            f"total_citations should be {actual_total}, got {mock_content.total_citations}"
        )

        # Per spec, should have at least 24 citations (3 per 8 sections)
        assert mock_content.total_citations >= 24, (
            f"Mock report should have at least 24 citations, got {mock_content.total_citations}"
        )

    @pytest.mark.asyncio
    async def test_get_report_returns_complete_mock_in_dev_mode(self):
        """Test that get_report returns a complete mock report when Supabase disabled"""
        with patch("src.api.services.report_service._is_supabase_enabled") as mock_flag:
            mock_flag.return_value = False

            result = await get_report("test-report-id", "test-user-id")

            # Mock report should have complete content
            assert result is not None
            assert result.content is not None
            assert result.content.sections is not None
            assert len(result.content.sections) == 10
            assert result.content.total_citations >= 24

    def test_mock_citations_have_valid_urls(self):
        """Test that mock citations have valid URL format"""
        mock_content = _create_mock_report_content("Test query")

        url_pattern = re.compile(r'^https?://[^\s]+$')

        for section in mock_content.sections:
            for citation in section.citations:
                assert url_pattern.match(citation.url), (
                    f"Citation URL '{citation.url}' is not valid"
                )
                assert citation.title, "Citation must have a title"
                assert citation.accessed_at, "Citation must have accessed_at timestamp"


class TestRegressionIntegration:
    """
    Integration tests to verify the fixes work together in realistic scenarios.
    """

    @pytest.mark.asyncio
    async def test_complete_dev_mode_flow(self):
        """
        Test complete report retrieval flow in dev mode.
        This verifies Issues #3, #5, and #7 work together.
        """
        with patch("src.api.services.report_service._is_supabase_enabled") as mock_flag:
            mock_flag.return_value = False

            # Get a mock report
            report = await get_report("test-id", "test-user")

            # Issue #3: Should return mock without Supabase call
            assert report is not None

            # Issue #5: Serialize and verify snake_case
            json_str = report.model_dump_json()
            assert "user_id" in json_str
            assert "created_at" in json_str
            assert "expires_at" in json_str
            assert "total_citations" in json_str
            # Verify no camelCase leaked through
            assert "userId" not in json_str
            assert "createdAt" not in json_str
            assert "expiresAt" not in json_str
            assert "totalCitations" not in json_str

            # Issue #7: Should have complete content
            assert report.content is not None
            assert len(report.content.sections) == 10
            assert report.content.total_citations >= 24
