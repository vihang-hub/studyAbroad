"""
Report Model

SQLAlchemy model for reports table.
Maps to data-model.md reports table schema with soft delete support.
"""

from datetime import datetime, timedelta
from sqlalchemy import String, DateTime, ForeignKey, Text, func, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column
from database.models.user import Base
import uuid
import enum
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg is not None:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


class ReportStatus(str, enum.Enum):
    """Report status enumeration"""

    PENDING = "pending"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"
    EXPIRED = "expired"


class Report(Base):
    """
    Report Model

    Represents AI-generated study & migration reports.
    Implements soft delete pattern with expires_at and deleted_at.

    Columns:
        report_id: Unique identifier
        user_id: Owner of the report (foreign key)
        subject: Field of study
        country: Destination country (always 'UK' in MVP)
        status: Current state of report generation
        content: JSON structure containing all 10 mandatory sections
        citations: Array of source references
        generation_metadata: AI model details
        created_at: When payment succeeded
        completed_at: When AI generation finished
        expires_at: 30 days from creation
        error_message: Details if generation failed
        updated_at: Last modification timestamp
    """

    __tablename__ = "reports"

    report_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False
    )
    subject: Mapped[str] = mapped_column(String(200), nullable=False)
    country: Mapped[str] = mapped_column(String(50), default="UK", nullable=False)
    status: Mapped[ReportStatus] = mapped_column(
        SQLEnum(ReportStatus, name="report_status"), default=ReportStatus.PENDING, nullable=False
    )
    content: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    citations: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    generation_metadata: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.utcnow() + timedelta(days=30),
        nullable=False,
    )
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self) -> str:
        return f"<Report(report_id={self.report_id}, subject={self.subject}, status={self.status})>"
