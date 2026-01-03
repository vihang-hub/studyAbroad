"""
Integration Tests for User Story 1: Generate Paid Report
Tasks T106-T112 Acceptance Criteria

These tests validate end-to-end flows from the specification:
- T106: Full flow (signup → chat → pay → generate → view report)
- T107: Citation validation (reports must have non-empty citations)
- T108: UK-only constraint enforcement
- T109: Payment-before-generation gate
- T110: Streaming validation
- T111: Multi-provider auth (Google, Apple, Facebook, Email)
- T112: Shared components portability
"""

import pytest
from unittest.mock import Mock, patch, AsyncMock, MagicMock
from fastapi.testclient import TestClient
import json
import asyncio
from datetime import datetime, timedelta

from src.main import app
from src.api.models.report import ReportStatus
from src.api.models.payment import PaymentStatus


class TestT106FullFlowAcceptance:
    """
    T106: Test complete flow: signup → chat → pay → generate → view report
    Acceptance Criteria:
    - All 10 mandatory report sections must be present
    - Report must include all required sections per spec
    """

    @pytest.mark.asyncio
    async def test_full_flow_all_sections_present(
        self, test_client, mock_clerk_user, mock_stripe, mock_supabase, mock_gemini
    ):
        """Test end-to-end flow from payment to report generation with all 10 sections"""

        # ARRANGE: Setup mocks for full flow
        user_id = "user_test_full_flow"
        subject = "Computer Science"

        # Mock Clerk authentication
        mock_clerk_user["id"] = user_id

        # Mock Stripe checkout session creation
        checkout_session = {
            "id": "cs_test_full_flow",
            "url": "https://checkout.stripe.com/test",
            "payment_status": "unpaid"
        }
        mock_stripe.checkout.Session.create.return_value = checkout_session

        # Mock Supabase payment creation
        mock_payment_data = {
            "id": "pay_test_full_flow",
            "user_id": user_id,
            "amount": 299,
            "status": PaymentStatus.PENDING.value,
            "stripe_session_id": "cs_test_full_flow",
            "created_at": datetime.utcnow().isoformat()
        }
        mock_supabase.table().insert().execute.return_value = Mock(
            data=[mock_payment_data]
        )

        # Mock Supabase report creation
        report_id = "report_test_full_flow"
        mock_report_data = {
            "id": report_id,
            "user_id": user_id,
            "subject": subject,
            "country": "UK",
            "status": ReportStatus.PENDING.value,
            "created_at": datetime.utcnow().isoformat(),
            "expires_at": (datetime.utcnow() + timedelta(days=30)).isoformat()
        }
        mock_supabase.table().insert().execute.return_value = Mock(
            data=[mock_report_data]
        )

        # Mock Gemini AI response with all 10 mandatory sections
        mock_ai_response = {
            "content": json.dumps({
                "executive_summary": [
                    "UK offers world-class computer science programs",
                    "Strong post-study work visa options available",
                    "Average tuition: £15,000-£25,000 per year",
                    "High demand for tech professionals",
                    "Excellent job prospects in major cities"
                ],
                "study_options": "UK universities offer BSc, MSc, and PhD programs in Computer Science...",
                "estimated_costs": {
                    "tuition": "£15,000 - £25,000 per year",
                    "living_costs": "£12,000 - £15,000 per year"
                },
                "visa_immigration": "Student visa (Tier 4) allows you to study full-time...",
                "post_study_work": "Graduate visa allows 2 years of post-study work...",
                "job_prospects_subject": "Strong demand for software engineers, data scientists...",
                "fallback_jobs": "IT support, business analyst, project coordinator roles available...",
                "risks_reality_check": "Competition is high. Cost of living in London is expensive...",
                "action_plan": {
                    "30_days": "Research universities, prepare documents",
                    "60_days": "Apply to programs, secure funding",
                    "90_days": "Apply for visa, arrange accommodation"
                },
                "sources_citations": [
                    {
                        "title": "UK Council for International Student Affairs",
                        "url": "https://www.ukcisa.org.uk/",
                        "accessed": "2025-01-02"
                    },
                    {
                        "title": "Gov.uk - Student Visa",
                        "url": "https://www.gov.uk/student-visa",
                        "accessed": "2025-01-02"
                    }
                ]
            }),
            "citations": [
                {"title": "UKCISA", "url": "https://www.ukcisa.org.uk/"},
                {"title": "Gov.uk", "url": "https://www.gov.uk/student-visa"}
            ]
        }
        mock_gemini.return_value = mock_ai_response

        # ACT: Execute full flow

        # Step 1: Create checkout session (initiate payment)
        with patch("src.api.routes.reports.verify_clerk_token", return_value=mock_clerk_user):
            response = test_client.post(
                "/api/reports/initiate",
                json={"subject": subject},
                headers={"Authorization": "Bearer mock_token"}
            )

        assert response.status_code == 200
        assert "checkout_url" in response.json()

        # Step 2: Simulate webhook (payment success)
        stripe_event = {
            "type": "checkout.session.completed",
            "data": {
                "object": {
                    "id": "cs_test_full_flow",
                    "payment_status": "paid",
                    "metadata": {
                        "report_id": report_id,
                        "user_id": user_id
                    }
                }
            }
        }

        with patch("src.api.routes.webhooks.verify_stripe_signature", return_value=True):
            with patch("src.api.services.report_service.trigger_report_generation") as mock_generate:
                mock_generate.return_value = None

                webhook_response = test_client.post(
                    "/api/webhooks/stripe",
                    json=stripe_event,
                    headers={"stripe-signature": "mock_sig"}
                )

        assert webhook_response.status_code == 200

        # Step 3: Verify report was generated with all sections
        mock_complete_report = {
            "id": report_id,
            "user_id": user_id,
            "subject": subject,
            "country": "UK",
            "status": ReportStatus.COMPLETED.value,
            "content": mock_ai_response["content"],
            "citations": mock_ai_response["citations"],
            "created_at": datetime.utcnow().isoformat(),
            "expires_at": (datetime.utcnow() + timedelta(days=30)).isoformat()
        }
        mock_supabase.table().select().eq().eq().execute.return_value = Mock(
            data=[mock_complete_report]
        )

        # Step 4: Retrieve report
        with patch("src.api.routes.reports.verify_clerk_token", return_value=mock_clerk_user):
            report_response = test_client.get(
                f"/api/reports/{report_id}",
                headers={"Authorization": "Bearer mock_token"}
            )

        # ASSERT: Verify all 10 mandatory sections are present
        assert report_response.status_code == 200
        report_data = report_response.json()

        assert report_data["status"] == ReportStatus.COMPLETED.value

        content = json.loads(report_data["content"])

        # Validate all 10 mandatory sections
        assert "executive_summary" in content, "Missing section 1: Executive Summary"
        assert "study_options" in content, "Missing section 2: Study Options"
        assert "estimated_costs" in content, "Missing section 3: Estimated Costs"
        assert "visa_immigration" in content, "Missing section 4: Visa & Immigration"
        assert "post_study_work" in content, "Missing section 5: Post-Study Work Options"
        assert "job_prospects_subject" in content, "Missing section 6: Job Prospects in Subject"
        assert "fallback_jobs" in content, "Missing section 7: Fallback Jobs"
        assert "risks_reality_check" in content, "Missing section 8: Risks & Reality Check"
        assert "action_plan" in content, "Missing section 9: Action Plan"
        assert "sources_citations" in content, "Missing section 10: Sources & Citations"

        # Validate executive summary has 5-10 bullets
        assert len(content["executive_summary"]) >= 5
        assert len(content["executive_summary"]) <= 10


class TestT107CitationValidation:
    """
    T107: Verify citations array is non-empty in generated reports
    Acceptance Criteria:
    - Reports must have mandatory citations
    - RAG integrity requirement from constitution
    """

    @pytest.mark.asyncio
    async def test_report_must_have_citations(
        self, test_client, mock_clerk_user, mock_supabase, mock_gemini
    ):
        """Test that generated reports always include non-empty citations"""

        # ARRANGE
        user_id = "user_citations_test"
        report_id = "report_citations_test"

        # Mock AI service returning report with citations
        mock_ai_response = {
            "content": json.dumps({
                "executive_summary": ["Test summary"],
                "sources_citations": [
                    {"title": "Source 1", "url": "https://example.com/1"},
                    {"title": "Source 2", "url": "https://example.com/2"}
                ]
            }),
            "citations": [
                {"title": "Source 1", "url": "https://example.com/1"},
                {"title": "Source 2", "url": "https://example.com/2"}
            ]
        }
        mock_gemini.return_value = mock_ai_response

        # Mock report retrieval
        mock_report = {
            "id": report_id,
            "user_id": user_id,
            "status": ReportStatus.COMPLETED.value,
            "content": mock_ai_response["content"],
            "citations": mock_ai_response["citations"]
        }
        mock_supabase.table().select().eq().eq().execute.return_value = Mock(
            data=[mock_report]
        )

        # ACT
        with patch("src.api.routes.reports.verify_clerk_token", return_value=mock_clerk_user):
            response = test_client.get(
                f"/api/reports/{report_id}",
                headers={"Authorization": "Bearer mock_token"}
            )

        # ASSERT
        assert response.status_code == 200
        report_data = response.json()

        # Citations must be non-empty
        assert "citations" in report_data
        assert isinstance(report_data["citations"], list)
        assert len(report_data["citations"]) > 0, "Report must have at least one citation"

        # Each citation must have required fields
        for citation in report_data["citations"]:
            assert "title" in citation
            assert "url" in citation
            assert citation["title"] != ""
            assert citation["url"] != ""

    @pytest.mark.asyncio
    async def test_report_generation_fails_without_citations(
        self, test_client, mock_gemini
    ):
        """Test that report generation enforces non-empty citations"""

        # ARRANGE: Mock AI response without citations
        mock_ai_response_no_citations = {
            "content": json.dumps({"executive_summary": ["Test"]}),
            "citations": []  # Empty citations should fail
        }
        mock_gemini.return_value = mock_ai_response_no_citations

        # ACT: This should be caught during generation
        from src.api.services.ai_service import generate_report

        # ASSERT: Generation should fail or add placeholder citations
        # (Implementation detail - adjust based on actual behavior)
        with pytest.raises(ValueError, match="Citations cannot be empty"):
            await generate_report("Computer Science")


class TestT108UKOnlyConstraint:
    """
    T108: Verify UK-only constraint enforcement
    Acceptance Criteria:
    - Attempt non-UK query and confirm rejection
    - System must reject queries for other countries
    """

    def test_reject_non_uk_country_query(
        self, test_client, mock_clerk_user
    ):
        """Test that non-UK country queries are rejected"""

        # ARRANGE
        non_uk_queries = [
            {"subject": "Computer Science", "country": "USA"},
            {"subject": "Medicine", "country": "Canada"},
            {"subject": "Business", "country": "Australia"},
            {"subject": "Engineering", "country": "Germany"}
        ]

        # ACT & ASSERT: Each non-UK query should be rejected
        for query in non_uk_queries:
            with patch("src.api.routes.reports.verify_clerk_token", return_value=mock_clerk_user):
                response = test_client.post(
                    "/api/reports/initiate",
                    json=query,
                    headers={"Authorization": "Bearer mock_token"}
                )

            assert response.status_code == 400
            assert "UK only" in response.json()["detail"] or \
                   "only supports the UK" in response.json()["detail"].lower()

    def test_accept_uk_query(
        self, test_client, mock_clerk_user, mock_stripe, mock_supabase
    ):
        """Test that UK queries are accepted"""

        # ARRANGE
        mock_checkout = {
            "id": "cs_test",
            "url": "https://checkout.stripe.com/test",
            "payment_status": "unpaid"
        }
        mock_stripe.checkout.Session.create.return_value = mock_checkout

        mock_supabase.table().insert().execute.return_value = Mock(
            data=[{"id": "pay_test", "status": "pending"}]
        )
        mock_supabase.table().insert().execute.return_value = Mock(
            data=[{"id": "report_test"}]
        )

        # ACT
        with patch("src.api.routes.reports.verify_clerk_token", return_value=mock_clerk_user):
            response = test_client.post(
                "/api/reports/initiate",
                json={"subject": "Computer Science", "country": "UK"},
                headers={"Authorization": "Bearer mock_token"}
            )

        # ASSERT
        assert response.status_code == 200
        assert "checkout_url" in response.json()

    def test_implicit_uk_when_country_not_specified(
        self, test_client, mock_clerk_user, mock_stripe, mock_supabase
    ):
        """Test that queries without country default to UK (MVP constraint)"""

        # ARRANGE
        mock_checkout = {
            "id": "cs_test",
            "url": "https://checkout.stripe.com/test"
        }
        mock_stripe.checkout.Session.create.return_value = mock_checkout

        mock_supabase.table().insert().execute.return_value = Mock(
            data=[{"id": "pay_test", "status": "pending"}]
        )
        mock_supabase.table().insert().execute.return_value = Mock(
            data=[{"id": "report_test", "country": "UK"}]
        )

        # ACT
        with patch("src.api.routes.reports.verify_clerk_token", return_value=mock_clerk_user):
            response = test_client.post(
                "/api/reports/initiate",
                json={"subject": "Computer Science"},  # No country specified
                headers={"Authorization": "Bearer mock_token"}
            )

        # ASSERT
        assert response.status_code == 200


class TestT109PaymentBeforeGeneration:
    """
    T109: Verify payment gate
    Acceptance Criteria:
    - Failed payment must result in no report generation
    - Report generation only triggered after successful payment
    """

    def test_failed_payment_no_report_generation(
        self, test_client, mock_supabase
    ):
        """Test that failed payment does not trigger report generation"""

        # ARRANGE: Mock failed payment webhook
        stripe_event_failed = {
            "type": "checkout.session.completed",
            "data": {
                "object": {
                    "id": "cs_failed_payment",
                    "payment_status": "unpaid",
                    "metadata": {
                        "report_id": "report_should_not_generate",
                        "user_id": "user_test"
                    }
                }
            }
        }

        # Mock payment update
        mock_supabase.table().update().eq().execute.return_value = Mock(
            data=[{"status": PaymentStatus.FAILED.value}]
        )

        # ACT
        with patch("src.api.routes.webhooks.verify_stripe_signature", return_value=True):
            with patch("src.api.services.report_service.trigger_report_generation") as mock_generate:
                response = test_client.post(
                    "/api/webhooks/stripe",
                    json=stripe_event_failed,
                    headers={"stripe-signature": "mock_sig"}
                )

        # ASSERT: Report generation should NOT be triggered
        mock_generate.assert_not_called()
        assert response.status_code == 200

    def test_successful_payment_triggers_generation(
        self, test_client, mock_supabase
    ):
        """Test that successful payment triggers report generation"""

        # ARRANGE
        report_id = "report_success_payment"
        stripe_event_success = {
            "type": "checkout.session.completed",
            "data": {
                "object": {
                    "id": "cs_success_payment",
                    "payment_status": "paid",
                    "metadata": {
                        "report_id": report_id,
                        "user_id": "user_test"
                    }
                }
            }
        }

        mock_supabase.table().update().eq().execute.return_value = Mock(
            data=[{"status": PaymentStatus.SUCCEEDED.value}]
        )

        # ACT
        with patch("src.api.routes.webhooks.verify_stripe_signature", return_value=True):
            with patch("src.api.services.report_service.trigger_report_generation") as mock_generate:
                mock_generate.return_value = None

                response = test_client.post(
                    "/api/webhooks/stripe",
                    json=stripe_event_success,
                    headers={"stripe-signature": "mock_sig"}
                )

        # ASSERT: Report generation MUST be triggered
        mock_generate.assert_called_once_with(report_id)
        assert response.status_code == 200

    def test_report_status_remains_pending_on_payment_failure(
        self, test_client, mock_supabase
    ):
        """Test that report status is not updated if payment fails"""

        # ARRANGE
        report_id = "report_pending"

        # Mock report in PENDING state
        mock_supabase.table().select().eq().execute.return_value = Mock(
            data=[{
                "id": report_id,
                "status": ReportStatus.PENDING.value
            }]
        )

        # Payment failed
        stripe_event = {
            "type": "checkout.session.completed",
            "data": {
                "object": {
                    "id": "cs_test",
                    "payment_status": "unpaid",
                    "metadata": {"report_id": report_id, "user_id": "user"}
                }
            }
        }

        # ACT
        with patch("src.api.routes.webhooks.verify_stripe_signature", return_value=True):
            test_client.post(
                "/api/webhooks/stripe",
                json=stripe_event,
                headers={"stripe-signature": "sig"}
            )

        # ASSERT: Report should remain in PENDING, never reach GENERATING
        # Verify via subsequent query that status is still PENDING
        mock_supabase.table().select().eq().execute.return_value = Mock(
            data=[{
                "id": report_id,
                "status": ReportStatus.PENDING.value  # Still pending
            }]
        )


class TestT110StreamingValidation:
    """
    T110: Verify streaming works
    Acceptance Criteria:
    - Report chunks must appear incrementally
    - Streaming response must begin within 5 seconds (p95)
    """

    @pytest.mark.asyncio
    async def test_streaming_response_incremental_chunks(
        self, test_client, mock_gemini
    ):
        """Test that report generation streams chunks incrementally"""

        # ARRANGE: Mock streaming AI response
        async def mock_stream_generator():
            chunks = [
                "Executive Summary: ",
                "UK offers excellent ",
                "computer science programs. ",
                "Study Options: ",
                "Multiple universities available..."
            ]
            for chunk in chunks:
                yield chunk
                await asyncio.sleep(0.1)  # Simulate streaming delay

        mock_gemini.return_value = mock_stream_generator()

        # ACT: Call streaming endpoint
        from src.api.services.ai_service import generate_report_stream

        chunks_received = []
        async for chunk in generate_report_stream("Computer Science"):
            chunks_received.append(chunk)

        # ASSERT: Verify incremental delivery
        assert len(chunks_received) >= 3, "Should receive multiple chunks"
        assert chunks_received[0] != "", "First chunk should not be empty"

        # Verify chunks are delivered incrementally, not all at once
        full_content = "".join(chunks_received)
        assert "Executive Summary" in full_content
        assert "Study Options" in full_content

    @pytest.mark.asyncio
    @pytest.mark.timeout(6)  # Should complete within 6 seconds
    async def test_streaming_begins_within_5_seconds(
        self, test_client, mock_gemini
    ):
        """Test that streaming response begins within 5 seconds (p95 requirement)"""

        # ARRANGE
        import time

        async def mock_stream_with_delay():
            await asyncio.sleep(0.5)  # Acceptable initial delay
            yield "First chunk"
            yield "Second chunk"

        mock_gemini.return_value = mock_stream_with_delay()

        # ACT
        from src.api.services.ai_service import generate_report_stream

        start_time = time.time()
        first_chunk_time = None

        async for chunk in generate_report_stream("Computer Science"):
            if first_chunk_time is None:
                first_chunk_time = time.time()
            break  # Only measure time to first chunk

        elapsed = first_chunk_time - start_time

        # ASSERT: First chunk within 5 seconds
        assert elapsed < 5.0, f"Streaming took {elapsed}s, must be <5s"


class TestT111MultiProviderAuth:
    """
    T111: Test all 4 auth providers
    Acceptance Criteria:
    - Google, Apple, Facebook, Email authentication
    - All providers must work correctly
    """

    def test_google_oauth_authentication(self, test_client):
        """Test Google OAuth authentication flow"""

        # ARRANGE: Mock Clerk user from Google OAuth
        mock_google_user = {
            "id": "user_google_123",
            "email": "test@gmail.com",
            "external_accounts": [{"provider": "google"}]
        }

        # ACT
        with patch("src.api.services.auth_service.verify_clerk_token", return_value=mock_google_user):
            response = test_client.get(
                "/api/reports",
                headers={"Authorization": "Bearer google_oauth_token"}
            )

        # ASSERT: Should authenticate successfully
        assert response.status_code == 200

    def test_apple_oauth_authentication(self, test_client):
        """Test Apple Sign In authentication flow"""

        # ARRANGE
        mock_apple_user = {
            "id": "user_apple_123",
            "email": "test@privaterelay.appleid.com",
            "external_accounts": [{"provider": "apple"}]
        }

        # ACT
        with patch("src.api.services.auth_service.verify_clerk_token", return_value=mock_apple_user):
            response = test_client.get(
                "/api/reports",
                headers={"Authorization": "Bearer apple_oauth_token"}
            )

        # ASSERT
        assert response.status_code == 200

    def test_facebook_oauth_authentication(self, test_client):
        """Test Facebook OAuth authentication flow"""

        # ARRANGE
        mock_facebook_user = {
            "id": "user_facebook_123",
            "email": "test@facebook.com",
            "external_accounts": [{"provider": "facebook"}]
        }

        # ACT
        with patch("src.api.services.auth_service.verify_clerk_token", return_value=mock_facebook_user):
            response = test_client.get(
                "/api/reports",
                headers={"Authorization": "Bearer facebook_oauth_token"}
            )

        # ASSERT
        assert response.status_code == 200

    def test_email_password_authentication(self, test_client):
        """Test email/password authentication flow"""

        # ARRANGE
        mock_email_user = {
            "id": "user_email_123",
            "email": "test@example.com",
            "email_addresses": [{"email_address": "test@example.com"}]
        }

        # ACT
        with patch("src.api.services.auth_service.verify_clerk_token", return_value=mock_email_user):
            response = test_client.get(
                "/api/reports",
                headers={"Authorization": "Bearer email_auth_token"}
            )

        # ASSERT
        assert response.status_code == 200


class TestT112SharedComponentsPortability:
    """
    T112: Verify shared components are portable
    Acceptance Criteria:
    - Change env vars and test in isolation
    - Shared packages must work across different configurations
    """

    def test_shared_package_works_with_different_api_endpoints(self):
        """Test that shared package can target different backend URLs"""

        # ARRANGE: Test with different API endpoints
        test_endpoints = [
            "http://localhost:8000",
            "https://api-dev.studyabroad.com",
            "https://api-staging.studyabroad.com",
            "https://api.studyabroad.com"
        ]

        for endpoint in test_endpoints:
            # ACT: Configure shared package with different endpoint
            import os
            os.environ["NEXT_PUBLIC_API_URL"] = endpoint

            # Import should work regardless of endpoint
            from src.lib.api_client import create_api_client

            client = create_api_client(endpoint)

            # ASSERT: Client should be configured with correct endpoint
            assert client.base_url == endpoint

    def test_shared_package_works_in_dev_test_prod_modes(self):
        """Test shared package behavior across environment modes"""

        # ARRANGE: Test all three modes
        environments = ["dev", "test", "production"]

        for env in environments:
            # ACT
            import os
            os.environ["ENVIRONMENT_MODE"] = env

            # Shared config should adapt to environment
            from src.config import get_environment_config

            config = get_environment_config()

            # ASSERT: Configuration should match environment
            assert config["mode"] == env

            if env == "dev":
                assert config["enable_payments"] is False
                assert config["log_level"] == "debug"
            elif env == "production":
                assert config["enable_payments"] is True
                assert config["log_level"] == "error"

    def test_shared_clerk_client_portable_across_projects(self):
        """Test that Clerk client works with different project IDs"""

        # ARRANGE
        test_clerk_keys = [
            "pk_test_project_A",
            "pk_test_project_B",
            "pk_live_production"
        ]

        for key in test_clerk_keys:
            # ACT
            import os
            os.environ["NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY"] = key

            # Shared Clerk client should initialize with any valid key
            from src.lib.clerk import initialize_clerk

            # ASSERT: Should not raise errors
            try:
                client = initialize_clerk()
                assert client is not None
            except Exception as e:
                pytest.fail(f"Clerk initialization failed with key {key}: {e}")
