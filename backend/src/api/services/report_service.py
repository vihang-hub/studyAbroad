"""
Report service for managing report lifecycle
Handles creation, generation, and retrieval
"""

import uuid
from datetime import datetime, timedelta
from typing import Optional, List
from src.config import settings
from src.api.models.report import (
    Report,
    ReportStatus,
    CreateReportResponse,
    ReportListItem,
    ReportContent,
    ReportSection,
    Citation,
)
from src.api.services.ai_service import generate_report
from src.feature_flags import feature_flags, Feature

# Note: get_supabase is imported dynamically in _get_supabase() to avoid
# initialization errors when Supabase is disabled


def _is_supabase_enabled() -> bool:
    """Check if Supabase is enabled via feature flag"""
    return feature_flags.is_enabled(Feature.SUPABASE)


def _get_supabase():
    """Get Supabase client only when enabled"""
    if not _is_supabase_enabled():
        raise RuntimeError("Supabase is disabled in dev mode")
    from src.lib.supabase import get_supabase
    return get_supabase()


def _create_mock_citation(title: str, url: str) -> Citation:
    """Create a mock citation for dev testing"""
    return Citation(
        title=title,
        url=url,
        snippet="Mock citation snippet for development testing.",
        accessed_at=datetime.utcnow(),
    )


def _create_mock_report_content(query: str) -> ReportContent:
    """
    Create mock report content for dev testing.
    Satisfies all validation requirements:
    - Exactly 10 sections with required headings
    - At least 3 citations per section (except Executive Summary and Sources & Citations)
    """
    now = datetime.utcnow()

    # Helper to create 3 citations for a section
    def make_citations(section_name: str) -> List[Citation]:
        return [
            _create_mock_citation(
                f"{section_name} - Source {i}",
                f"https://example.com/{section_name.lower().replace(' ', '-')}/source-{i}"
            )
            for i in range(1, 4)
        ]

    sections = [
        ReportSection(
            heading="Executive Summary",
            content=f"This is a mock executive summary for your query: '{query}'. "
                    "In dev mode, this report contains placeholder content to test the UI flow. "
                    "When connected to the AI service, this section will provide a comprehensive "
                    "overview of studying in the UK based on your specific interests.",
            citations=[],  # Executive Summary doesn't require citations
        ),
        ReportSection(
            heading="Study Options in the UK",
            content="The UK offers a wide range of study options including undergraduate degrees, "
                    "postgraduate programs, and research opportunities. Top universities include "
                    "Oxford, Cambridge, Imperial College London, and many Russell Group institutions. "
                    "Course durations typically range from 1-4 years depending on the level of study.",
            citations=make_citations("Study Options"),
        ),
        ReportSection(
            heading="Estimated Cost of Studying",
            content="Tuition fees for international students typically range from £10,000 to £38,000 "
                    "per year depending on the course and institution. Living costs average £12,000-£15,000 "
                    "per year outside London and £15,000-£20,000 in London. Scholarships and financial "
                    "aid options are available through various organizations.",
            citations=make_citations("Costs"),
        ),
        ReportSection(
            heading="Visa & Immigration Overview",
            content="International students require a Student visa (formerly Tier 4) to study in the UK. "
                    "Requirements include a Confirmation of Acceptance for Studies (CAS), proof of funds, "
                    "English language proficiency, and valid passport. Processing typically takes 3-4 weeks.",
            citations=make_citations("Visa"),
        ),
        ReportSection(
            heading="Post-Study Work Options",
            content="The Graduate Route allows students to stay and work in the UK for 2 years after "
                    "completing a degree (3 years for PhD graduates). This provides time to gain work "
                    "experience and potentially transition to a Skilled Worker visa for longer-term employment.",
            citations=make_citations("Post Study Work"),
        ),
        ReportSection(
            heading="Job Prospects in the Chosen Subject",
            content="Job prospects vary by field of study. STEM subjects, healthcare, and business "
                    "consistently show strong employment rates. Many universities have career services "
                    "and industry partnerships to help students secure employment.",
            citations=make_citations("Job Prospects"),
        ),
        ReportSection(
            heading="Fallback Job Prospects (Out-of-Field)",
            content="Even if direct employment in your field isn't immediately available, transferable "
                    "skills from UK education are valued across sectors. Common fallback options include "
                    "consulting, project management, teaching, and administrative roles.",
            citations=make_citations("Fallback Jobs"),
        ),
        ReportSection(
            heading="Risks & Reality Check",
            content="Key risks include high living costs especially in London, competitive job market "
                    "for certain fields, visa restrictions, and adjustment to a new culture and climate. "
                    "It's important to have realistic expectations and contingency plans.",
            citations=make_citations("Risks"),
        ),
        ReportSection(
            heading="30/60/90-Day Action Plan",
            content="30 days: Research universities and programs, check entry requirements. "
                    "60 days: Prepare application materials, take required tests (IELTS/TOEFL). "
                    "90 days: Submit applications, arrange funding, begin visa preparation.",
            citations=make_citations("Action Plan"),
        ),
        ReportSection(
            heading="Sources & Citations",
            content="All information in this report has been compiled from official UK government sources, "
                    "university websites, and reputable education consultancies. Please verify current "
                    "requirements as policies may change.",
            citations=[],  # Sources & Citations section doesn't require additional citations
        ),
    ]

    # Count total citations (3 citations * 8 sections that require them = 24)
    total_citations = sum(len(s.citations) for s in sections)

    return ReportContent(
        query=query,
        summary=f"Comprehensive analysis for: {query}. This mock report demonstrates the full "
                "10-section structure that will be generated by our AI service.",
        sections=sections,
        total_citations=total_citations,
        generated_at=now,
    )


async def create_report(user_id: str, query: str) -> CreateReportResponse:
    """
    Create a new report record with pending status
    Report generation will be triggered after payment
    """
    report_id = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(days=settings.REPORT_EXPIRY_DAYS)

    # In dev mode without Supabase, just return mock response
    if not _is_supabase_enabled():
        return CreateReportResponse(
            report_id=report_id,
            status=ReportStatus.PENDING,
            estimated_completion_seconds=60,
        )

    supabase = _get_supabase()

    report_data = {
        "id": report_id,
        "user_id": user_id,
        "query": query,
        "status": ReportStatus.PENDING.value,
        "expires_at": expires_at.isoformat(),
    }

    supabase.table("reports").insert(report_data).execute()

    return CreateReportResponse(
        report_id=report_id,
        status=ReportStatus.PENDING,
        estimated_completion_seconds=60,
    )


async def trigger_report_generation(report_id: str) -> None:
    """
    Trigger AI report generation after payment succeeds
    Updates status from pending → generating → completed
    """
    # In dev mode without Supabase, skip database operations
    if not _is_supabase_enabled():
        return

    supabase = _get_supabase()

    try:
        # Get report
        report_result = supabase.table("reports").select("*").eq("id", report_id).execute()

        if not report_result.data or len(report_result.data) == 0:
            raise Exception(f"Report {report_id} not found")

        report_data = report_result.data[0]
        query = report_data["query"]

        # Update status to generating
        supabase.table("reports").update(
            {
                "status": ReportStatus.GENERATING.value,
                "updated_at": datetime.utcnow().isoformat(),
            }
        ).eq("id", report_id).execute()

        # Generate report using AI
        report_content = await generate_report(query)

        # Store generated content
        supabase.table("reports").update(
            {
                "status": ReportStatus.COMPLETED.value,
                "content": report_content.dict(),
                "updated_at": datetime.utcnow().isoformat(),
            }
        ).eq("id", report_id).execute()

    except Exception as e:
        # Handle generation failure
        supabase.table("reports").update(
            {
                "status": ReportStatus.FAILED.value,
                "error": str(e),
                "updated_at": datetime.utcnow().isoformat(),
            }
        ).eq("id", report_id).execute()

        raise e


async def get_report(report_id: str, user_id: str) -> Optional[Report]:
    """
    Get report by ID (with user ownership check)
    """
    # In dev mode without Supabase, return a mock completed report
    if not _is_supabase_enabled():
        # Return mock report for dev testing with full content
        mock_query = "I want to study Computer Science in the UK"
        return Report(
            id=report_id,
            user_id=user_id,
            query=mock_query,
            status=ReportStatus.COMPLETED,
            content=_create_mock_report_content(mock_query),
            error=None,
            expires_at=datetime.utcnow() + timedelta(days=settings.REPORT_EXPIRY_DAYS),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow(),
            deleted_at=None,
        )

    supabase = _get_supabase()

    result = (
        supabase.table("reports")
        .select("*")
        .eq("id", report_id)
        .eq("user_id", user_id)
        .is_("deleted_at", "null")
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Report(**result.data[0])
    return None


async def list_user_reports(user_id: str, limit: int = 50) -> List[ReportListItem]:
    """
    List all reports for a user
    """
    # In dev mode without Supabase, return empty list
    if not _is_supabase_enabled():
        return []

    supabase = _get_supabase()

    result = (
        supabase.table("reports")
        .select("id, query, status, created_at, expires_at")
        .eq("user_id", user_id)
        .is_("deleted_at", "null")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )

    return [ReportListItem(**item) for item in result.data]


async def update_report_status(report_id: str, status: str, error: Optional[str] = None) -> None:
    """
    Update report status (used by streaming endpoint)
    """
    # In dev mode without Supabase, skip database operations
    if not _is_supabase_enabled():
        return

    supabase = _get_supabase()

    update_data = {
        "status": status,
        "updated_at": datetime.utcnow().isoformat(),
    }

    if error:
        update_data["error"] = error

    supabase.table("reports").update(update_data).eq("id", report_id).execute()


async def soft_delete_report(report_id: str, user_id: str) -> bool:
    """
    Soft delete a report (set deleted_at timestamp)
    """
    # In dev mode without Supabase, return False (no deletion happened)
    if not _is_supabase_enabled():
        return False

    supabase = _get_supabase()

    result = (
        supabase.table("reports")
        .update(
            {
                "deleted_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
            }
        )
        .eq("id", report_id)
        .eq("user_id", user_id)
        .execute()
    )

    return len(result.data) > 0
