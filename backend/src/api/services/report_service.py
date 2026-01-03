"""
Report service for managing report lifecycle
Handles creation, generation, and retrieval
"""

import uuid
from datetime import datetime, timedelta
from typing import Optional, List
from src.lib.supabase import get_supabase
from src.config import settings
from src.api.models.report import (
    Report,
    ReportStatus,
    CreateReportResponse,
    ReportListItem,
)
from src.api.services.ai_service import generate_report


async def create_report(user_id: str, query: str) -> CreateReportResponse:
    """
    Create a new report record with pending status
    Report generation will be triggered after payment
    """
    supabase = get_supabase()

    report_id = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(days=settings.REPORT_EXPIRY_DAYS)

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
    supabase = get_supabase()

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
    supabase = get_supabase()

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
    supabase = get_supabase()

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
    supabase = get_supabase()

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
    supabase = get_supabase()

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
