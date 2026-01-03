"""
API Request/Response Pydantic Models

Pydantic models for validating API requests and responses in the FastAPI backend.
These models mirror the TypeScript Zod schemas for consistency.

Module: backend.models.schemas
"""

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator
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


# ==============================================================================
# ENUMS
# ==============================================================================


class Country(str, Enum):
    """Supported countries (MVP: UK only)"""

    UK = "UK"


class ReportStatus(str, Enum):
    """Report generation status"""

    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"


class PaymentStatus(str, Enum):
    """Payment processing status"""

    REQUIRES_PAYMENT_METHOD = "requires_payment_method"
    REQUIRES_CONFIRMATION = "requires_confirmation"
    PROCESSING = "processing"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELED = "canceled"
    BYPASSED = "bypassed"


class AuthProvider(str, Enum):
    """Authentication providers"""

    GOOGLE = "google"
    APPLE = "apple"
    FACEBOOK = "facebook"
    EMAIL = "email"


class EnvironmentMode(str, Enum):
    """Application environment modes"""

    DEV = "dev"
    TEST = "test"
    PRODUCTION = "production"


class HealthStatus(str, Enum):
    """Health check status"""

    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


class SSEEventType(str, Enum):
    """Server-Sent Events types"""

    START = "start"
    CHUNK = "chunk"
    CITATION = "citation"
    COMPLETE = "complete"
    ERROR = "error"


class ErrorCode(str, Enum):
    """API error codes"""

    VALIDATION_ERROR = "VALIDATION_ERROR"
    UNAUTHORIZED = "UNAUTHORIZED"
    FORBIDDEN = "FORBIDDEN"
    NOT_FOUND = "NOT_FOUND"
    PAYMENT_REQUIRED = "PAYMENT_REQUIRED"
    PAYMENT_FAILED = "PAYMENT_FAILED"
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"
    GEMINI_API_ERROR = "GEMINI_API_ERROR"
    DATABASE_ERROR = "DATABASE_ERROR"
    REPORT_GENERATION_FAILED = "REPORT_GENERATION_FAILED"
    REPORT_EXPIRED = "REPORT_EXPIRED"
    REPORT_DELETED = "REPORT_DELETED"
    INVALID_COUNTRY = "INVALID_COUNTRY"
    INVALID_SUBJECT = "INVALID_SUBJECT"


# ==============================================================================
# BASE MODELS
# ==============================================================================


class BaseSchema(BaseModel):
    """Base schema with common configuration"""

    model_config = {
        "use_enum_values": True,
        "validate_assignment": True,
        "arbitrary_types_allowed": False,
        "str_strip_whitespace": True,
    }


# ==============================================================================
# REPORT MODELS
# ==============================================================================


class CostRange(BaseSchema):
    """Cost range with min/max and currency"""

    min: Decimal = Field(..., ge=0, description="Minimum cost")
    max: Decimal = Field(..., ge=0, description="Maximum cost")
    currency: str = Field(default="GBP", pattern="^GBP$")

    @field_validator("max")
    @classmethod
    def validate_max_greater_than_min(cls, v: Decimal, info) -> Decimal:
        """Ensure max is greater than or equal to min"""
        if "min" in info.data and v < info.data["min"]:
            raise ValueError("max must be greater than or equal to min")
        return v


class ActionPlan(BaseSchema):
    """30/60/90 day action plan"""

    day_30: List[str] = Field(..., min_length=1, alias="30_day", description="30-day action items")
    day_60: List[str] = Field(..., min_length=1, alias="60_day", description="60-day action items")
    day_90: List[str] = Field(..., min_length=1, alias="90_day", description="90-day action items")


class ReportContent(BaseSchema):
    """
    Report content structure (matches spec mandatory sections)

    All fields correspond to the 10 mandatory sections in spec.md Section 11.
    """

    executive_summary: List[str] = Field(
        ...,
        min_length=5,
        max_length=10,
        description="5-10 bullet point summary",
    )
    study_options: Dict[str, Any] = Field(
        ...,
        description="Universities and programs available",
    )
    estimated_costs: Dict[str, CostRange] = Field(
        ...,
        description="Tuition and living cost estimates",
    )
    visa_overview: str = Field(
        ...,
        min_length=1,
        description="High-level visa and immigration information",
    )
    post_study_work: str = Field(
        ...,
        min_length=1,
        description="Post-study work visa options",
    )
    job_prospects: str = Field(
        ...,
        min_length=1,
        description="Employment prospects in chosen field",
    )
    fallback_jobs: str = Field(
        ...,
        min_length=1,
        description="Alternative career paths",
    )
    risks: str = Field(
        ...,
        min_length=1,
        description="Realistic risks and challenges",
    )
    action_plan: ActionPlan = Field(
        ...,
        description="30/60/90 day action plan",
    )

    @field_validator("estimated_costs")
    @classmethod
    def validate_estimated_costs(cls, v: Dict[str, Any]) -> Dict[str, Any]:
        """Ensure tuition and living costs are present"""
        if "tuition" not in v or "living" not in v:
            raise ValueError("estimated_costs must include 'tuition' and 'living' fields")
        return v


class Citation(BaseSchema):
    """Citation for RAG integrity"""

    source: str = Field(..., min_length=1, description="Name of the source")
    url: str = Field(..., description="Source URL")
    retrieved_at: datetime = Field(..., description="Timestamp when data was retrieved")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0-1)")


class CreateReportRequest(BaseSchema):
    """Request to create a new report"""

    subject: str = Field(..., min_length=1, max_length=255, description="Field of study")
    country: Country = Field(default=Country.UK, description="Destination country (UK only)")


class CreateReportResponse(BaseSchema):
    """Response after initiating report creation"""

    report_id: UUID = Field(..., alias="reportId")
    stream_url: str = Field(..., alias="streamUrl")
    status: ReportStatus
    created_at: datetime = Field(..., alias="createdAt")
    expires_at: datetime = Field(..., alias="expiresAt")


class ReportSummary(BaseSchema):
    """Summary of a report (for list endpoint)"""

    report_id: UUID = Field(..., alias="reportId")
    subject: str
    country: Country
    status: ReportStatus
    created_at: datetime = Field(..., alias="createdAt")
    expires_at: datetime = Field(..., alias="expiresAt")


class ListReportsResponse(BaseSchema):
    """Response for list reports endpoint"""

    reports: List[ReportSummary]
    total: int = Field(..., ge=0)
    limit: int = Field(..., ge=1)
    offset: int = Field(..., ge=0)


class ReportResponse(BaseSchema):
    """Full report response"""

    report_id: UUID = Field(..., alias="reportId")
    user_id: UUID = Field(..., alias="userId")
    subject: str
    country: Country
    status: ReportStatus
    content: ReportContent
    citations: List[Citation] = Field(
        ..., min_length=1, description="At least one citation required"
    )
    created_at: datetime = Field(..., alias="createdAt")
    expires_at: datetime = Field(..., alias="expiresAt")


# ==============================================================================
# PAYMENT MODELS
# ==============================================================================


class CreatePaymentRequest(BaseSchema):
    """Request to create a payment"""

    amount: Decimal = Field(..., ge=Decimal("2.99"), le=Decimal("2.99"))
    currency: str = Field(default="GBP", pattern="^GBP$")
    report_subject: str = Field(..., min_length=1, alias="reportSubject")


class CreatePaymentResponse(BaseSchema):
    """Response after creating a payment intent"""

    payment_id: UUID = Field(..., alias="paymentId")
    client_secret: str = Field(..., alias="clientSecret")
    amount: Decimal
    currency: str
    status: PaymentStatus
    bypassed: Optional[bool] = Field(
        default=None, description="True if payment bypassed (dev/test)"
    )


# ==============================================================================
# HEALTH CHECK MODELS
# ==============================================================================


class HealthCheck(BaseSchema):
    """Individual service health check"""

    status: HealthStatus
    latency_ms: Optional[int] = Field(default=None, ge=0, alias="latency_ms")
    error: Optional[str] = None


class HealthResponse(BaseSchema):
    """Basic health check response"""

    status: HealthStatus
    timestamp: datetime
    environment: EnvironmentMode
    version: str


class DetailedHealthResponse(HealthResponse):
    """Detailed health check response with service checks"""

    checks: Dict[str, HealthCheck] = Field(
        ...,
        description="Health status of individual services",
    )


# ==============================================================================
# ERROR MODELS
# ==============================================================================


class ErrorDetail(BaseSchema):
    """Error detail structure"""

    code: ErrorCode = Field(..., description="Machine-readable error code")
    message: str = Field(..., description="Human-readable error message")
    correlation_id: UUID = Field(..., alias="correlationId", description="Request correlation ID")
    timestamp: datetime
    details: Optional[Dict[str, Any]] = None


class ErrorResponse(BaseSchema):
    """Standard error response"""

    error: ErrorDetail


# ==============================================================================
# SSE MODELS
# ==============================================================================


class SSEStartEvent(BaseSchema):
    """SSE start event data"""

    report_id: UUID = Field(..., alias="reportId")
    status: ReportStatus


class SSEChunkEvent(BaseSchema):
    """SSE chunk event data"""

    section: str
    content: str


class SSECompleteEvent(BaseSchema):
    """SSE complete event data"""

    report_id: UUID = Field(..., alias="reportId")
    status: ReportStatus


class SSEEvent(BaseSchema):
    """Generic SSE event"""

    event: SSEEventType
    data: Dict[str, Any]


# ==============================================================================
# DATABASE MODELS
# ==============================================================================


class UserDB(BaseSchema):
    """User database model"""

    user_id: UUID
    clerk_user_id: str
    auth_provider: AuthProvider
    email: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None


class ReportDB(BaseSchema):
    """Report database model"""

    report_id: UUID
    user_id: UUID
    subject: str
    country: Country
    content: Dict[str, Any]
    citations: List[Dict[str, Any]]
    status: ReportStatus
    created_at: datetime
    expires_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None


class PaymentDB(BaseSchema):
    """Payment database model"""

    payment_id: UUID
    user_id: UUID
    report_id: Optional[UUID] = None
    stripe_payment_intent_id: Optional[str] = None
    stripe_client_secret: Optional[str] = None
    amount: Decimal
    currency: str
    status: PaymentStatus
    bypassed: bool = False
    failure_reason: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None


# ==============================================================================
# UTILITY MODELS
# ==============================================================================


class PaginationParams(BaseSchema):
    """Pagination parameters"""

    limit: int = Field(default=50, ge=1, le=100)
    offset: int = Field(default=0, ge=0)
