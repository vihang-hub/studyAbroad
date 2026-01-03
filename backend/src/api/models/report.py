"""
Report Pydantic models
"""

from datetime import datetime
from typing import Optional, List
from enum import Enum
from pydantic import BaseModel, field_validator


class ReportStatus(str, Enum):
    """Report status lifecycle"""

    PENDING = "pending"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"
    EXPIRED = "expired"


class Citation(BaseModel):
    """Citation within report content"""

    title: str
    url: str
    snippet: Optional[str] = None
    accessed_at: datetime


# Required section headings per specification Section 9
REQUIRED_SECTIONS = [
    "Executive Summary",
    "Study Options in the UK",
    "Estimated Cost of Studying",
    "Visa & Immigration Overview",
    "Post-Study Work Options",
    "Job Prospects in the Chosen Subject",
    "Fallback Job Prospects (Out-of-Field)",
    "Risks & Reality Check",
    "30/60/90-Day Action Plan",
    "Sources & Citations",
]


class ReportSection(BaseModel):
    """Section within report content"""

    heading: str
    content: str
    citations: List[Citation] = []

    @field_validator("citations")
    @classmethod
    def validate_citations(cls, v: List[Citation], info) -> List[Citation]:
        """Enforce citation requirements: minimum 3 citations per section except Executive Summary"""
        # Get heading from field data if available
        data = info.data if hasattr(info, "data") else {}
        heading = data.get("heading", "")

        # Executive Summary and Sources & Citations can have different citation requirements
        if heading not in ["Executive Summary", "Sources & Citations"]:
            if len(v) < 3:
                raise ValueError(
                    f"Section '{heading}' must have at least 3 citations, got {len(v)}. "
                    "Per specification Section 9, all factual claims must include citations."
                )
        return v


class ReportContent(BaseModel):
    """Complete report content"""

    query: str
    summary: str
    sections: List[ReportSection]
    total_citations: int
    generated_at: datetime

    @field_validator("sections")
    @classmethod
    def validate_sections(cls, v: List[ReportSection]) -> List[ReportSection]:
        """
        Enforce specification Section 9 requirements:
        - Exactly 10 sections
        - Correct section headings in exact order
        """
        if len(v) != 10:
            raise ValueError(
                f"Report must have exactly 10 sections per specification Section 9, got {len(v)}"
            )

        section_headings = [s.heading for s in v]
        for i, required in enumerate(REQUIRED_SECTIONS):
            if section_headings[i] != required:
                raise ValueError(
                    f"Section {i + 1} must be '{required}' per specification Section 9, "
                    f"got '{section_headings[i]}'"
                )

        return v

    @field_validator("total_citations")
    @classmethod
    def validate_total_citations(cls, v: int) -> int:
        """Ensure report has citations (spec requires citations for all factual claims)"""
        if v == 0:
            raise ValueError(
                "Report must include citations per specification Section 9. "
                "No uncited confident claims are allowed."
            )
        return v


class Report(BaseModel):
    """Report model"""

    id: str
    user_id: str
    query: str
    status: ReportStatus
    content: Optional[ReportContent] = None
    error: Optional[str] = None
    expires_at: datetime
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CreateReportRequest(BaseModel):
    """Request to create a new report"""

    query: str


class CreateReportResponse(BaseModel):
    """Response after creating a report with payment details"""

    report_id: str
    status: ReportStatus
    estimated_completion_seconds: int = 60
    # Payment fields from Stripe checkout (added by /initiate endpoint)
    client_secret: Optional[str] = None
    payment_intent_id: Optional[str] = None
    amount: Optional[int] = None
    currency: Optional[str] = None


class ReportListItem(BaseModel):
    """Report list item (summary view)"""

    id: str
    query: str
    status: ReportStatus
    created_at: datetime
    expires_at: datetime
