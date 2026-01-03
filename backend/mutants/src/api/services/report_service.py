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


async def x_create_report__mutmut_orig(user_id: str, query: str) -> CreateReportResponse:
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


async def x_create_report__mutmut_1(user_id: str, query: str) -> CreateReportResponse:
    """
    Create a new report record with pending status
    Report generation will be triggered after payment
    """
    supabase = None

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


async def x_create_report__mutmut_2(user_id: str, query: str) -> CreateReportResponse:
    """
    Create a new report record with pending status
    Report generation will be triggered after payment
    """
    supabase = get_supabase()

    report_id = None
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


async def x_create_report__mutmut_3(user_id: str, query: str) -> CreateReportResponse:
    """
    Create a new report record with pending status
    Report generation will be triggered after payment
    """
    supabase = get_supabase()

    report_id = str(None)
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


async def x_create_report__mutmut_4(user_id: str, query: str) -> CreateReportResponse:
    """
    Create a new report record with pending status
    Report generation will be triggered after payment
    """
    supabase = get_supabase()

    report_id = str(uuid.uuid4())
    expires_at = None

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


async def x_create_report__mutmut_5(user_id: str, query: str) -> CreateReportResponse:
    """
    Create a new report record with pending status
    Report generation will be triggered after payment
    """
    supabase = get_supabase()

    report_id = str(uuid.uuid4())
    expires_at = datetime.utcnow() - timedelta(days=settings.REPORT_EXPIRY_DAYS)

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


async def x_create_report__mutmut_6(user_id: str, query: str) -> CreateReportResponse:
    """
    Create a new report record with pending status
    Report generation will be triggered after payment
    """
    supabase = get_supabase()

    report_id = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(days=None)

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


async def x_create_report__mutmut_7(user_id: str, query: str) -> CreateReportResponse:
    """
    Create a new report record with pending status
    Report generation will be triggered after payment
    """
    supabase = get_supabase()

    report_id = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(days=settings.REPORT_EXPIRY_DAYS)

    report_data = None

    supabase.table("reports").insert(report_data).execute()

    return CreateReportResponse(
        report_id=report_id,
        status=ReportStatus.PENDING,
        estimated_completion_seconds=60,
    )


async def x_create_report__mutmut_8(user_id: str, query: str) -> CreateReportResponse:
    """
    Create a new report record with pending status
    Report generation will be triggered after payment
    """
    supabase = get_supabase()

    report_id = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(days=settings.REPORT_EXPIRY_DAYS)

    report_data = {
        "XXidXX": report_id,
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


async def x_create_report__mutmut_9(user_id: str, query: str) -> CreateReportResponse:
    """
    Create a new report record with pending status
    Report generation will be triggered after payment
    """
    supabase = get_supabase()

    report_id = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(days=settings.REPORT_EXPIRY_DAYS)

    report_data = {
        "ID": report_id,
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


async def x_create_report__mutmut_10(user_id: str, query: str) -> CreateReportResponse:
    """
    Create a new report record with pending status
    Report generation will be triggered after payment
    """
    supabase = get_supabase()

    report_id = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(days=settings.REPORT_EXPIRY_DAYS)

    report_data = {
        "id": report_id,
        "XXuser_idXX": user_id,
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


async def x_create_report__mutmut_11(user_id: str, query: str) -> CreateReportResponse:
    """
    Create a new report record with pending status
    Report generation will be triggered after payment
    """
    supabase = get_supabase()

    report_id = str(uuid.uuid4())
    expires_at = datetime.utcnow() + timedelta(days=settings.REPORT_EXPIRY_DAYS)

    report_data = {
        "id": report_id,
        "USER_ID": user_id,
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


async def x_create_report__mutmut_12(user_id: str, query: str) -> CreateReportResponse:
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
        "XXqueryXX": query,
        "status": ReportStatus.PENDING.value,
        "expires_at": expires_at.isoformat(),
    }

    supabase.table("reports").insert(report_data).execute()

    return CreateReportResponse(
        report_id=report_id,
        status=ReportStatus.PENDING,
        estimated_completion_seconds=60,
    )


async def x_create_report__mutmut_13(user_id: str, query: str) -> CreateReportResponse:
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
        "QUERY": query,
        "status": ReportStatus.PENDING.value,
        "expires_at": expires_at.isoformat(),
    }

    supabase.table("reports").insert(report_data).execute()

    return CreateReportResponse(
        report_id=report_id,
        status=ReportStatus.PENDING,
        estimated_completion_seconds=60,
    )


async def x_create_report__mutmut_14(user_id: str, query: str) -> CreateReportResponse:
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
        "XXstatusXX": ReportStatus.PENDING.value,
        "expires_at": expires_at.isoformat(),
    }

    supabase.table("reports").insert(report_data).execute()

    return CreateReportResponse(
        report_id=report_id,
        status=ReportStatus.PENDING,
        estimated_completion_seconds=60,
    )


async def x_create_report__mutmut_15(user_id: str, query: str) -> CreateReportResponse:
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
        "STATUS": ReportStatus.PENDING.value,
        "expires_at": expires_at.isoformat(),
    }

    supabase.table("reports").insert(report_data).execute()

    return CreateReportResponse(
        report_id=report_id,
        status=ReportStatus.PENDING,
        estimated_completion_seconds=60,
    )


async def x_create_report__mutmut_16(user_id: str, query: str) -> CreateReportResponse:
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
        "XXexpires_atXX": expires_at.isoformat(),
    }

    supabase.table("reports").insert(report_data).execute()

    return CreateReportResponse(
        report_id=report_id,
        status=ReportStatus.PENDING,
        estimated_completion_seconds=60,
    )


async def x_create_report__mutmut_17(user_id: str, query: str) -> CreateReportResponse:
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
        "EXPIRES_AT": expires_at.isoformat(),
    }

    supabase.table("reports").insert(report_data).execute()

    return CreateReportResponse(
        report_id=report_id,
        status=ReportStatus.PENDING,
        estimated_completion_seconds=60,
    )


async def x_create_report__mutmut_18(user_id: str, query: str) -> CreateReportResponse:
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

    supabase.table("reports").insert(None).execute()

    return CreateReportResponse(
        report_id=report_id,
        status=ReportStatus.PENDING,
        estimated_completion_seconds=60,
    )


async def x_create_report__mutmut_19(user_id: str, query: str) -> CreateReportResponse:
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

    supabase.table(None).insert(report_data).execute()

    return CreateReportResponse(
        report_id=report_id,
        status=ReportStatus.PENDING,
        estimated_completion_seconds=60,
    )


async def x_create_report__mutmut_20(user_id: str, query: str) -> CreateReportResponse:
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

    supabase.table("XXreportsXX").insert(report_data).execute()

    return CreateReportResponse(
        report_id=report_id,
        status=ReportStatus.PENDING,
        estimated_completion_seconds=60,
    )


async def x_create_report__mutmut_21(user_id: str, query: str) -> CreateReportResponse:
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

    supabase.table("REPORTS").insert(report_data).execute()

    return CreateReportResponse(
        report_id=report_id,
        status=ReportStatus.PENDING,
        estimated_completion_seconds=60,
    )


async def x_create_report__mutmut_22(user_id: str, query: str) -> CreateReportResponse:
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
        report_id=None,
        status=ReportStatus.PENDING,
        estimated_completion_seconds=60,
    )


async def x_create_report__mutmut_23(user_id: str, query: str) -> CreateReportResponse:
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
        status=None,
        estimated_completion_seconds=60,
    )


async def x_create_report__mutmut_24(user_id: str, query: str) -> CreateReportResponse:
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
        estimated_completion_seconds=None,
    )


async def x_create_report__mutmut_25(user_id: str, query: str) -> CreateReportResponse:
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
        status=ReportStatus.PENDING,
        estimated_completion_seconds=60,
    )


async def x_create_report__mutmut_26(user_id: str, query: str) -> CreateReportResponse:
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
        estimated_completion_seconds=60,
    )


async def x_create_report__mutmut_27(user_id: str, query: str) -> CreateReportResponse:
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
        )


async def x_create_report__mutmut_28(user_id: str, query: str) -> CreateReportResponse:
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
        estimated_completion_seconds=61,
    )

x_create_report__mutmut_mutants : ClassVar[MutantDict] = {
'x_create_report__mutmut_1': x_create_report__mutmut_1, 
    'x_create_report__mutmut_2': x_create_report__mutmut_2, 
    'x_create_report__mutmut_3': x_create_report__mutmut_3, 
    'x_create_report__mutmut_4': x_create_report__mutmut_4, 
    'x_create_report__mutmut_5': x_create_report__mutmut_5, 
    'x_create_report__mutmut_6': x_create_report__mutmut_6, 
    'x_create_report__mutmut_7': x_create_report__mutmut_7, 
    'x_create_report__mutmut_8': x_create_report__mutmut_8, 
    'x_create_report__mutmut_9': x_create_report__mutmut_9, 
    'x_create_report__mutmut_10': x_create_report__mutmut_10, 
    'x_create_report__mutmut_11': x_create_report__mutmut_11, 
    'x_create_report__mutmut_12': x_create_report__mutmut_12, 
    'x_create_report__mutmut_13': x_create_report__mutmut_13, 
    'x_create_report__mutmut_14': x_create_report__mutmut_14, 
    'x_create_report__mutmut_15': x_create_report__mutmut_15, 
    'x_create_report__mutmut_16': x_create_report__mutmut_16, 
    'x_create_report__mutmut_17': x_create_report__mutmut_17, 
    'x_create_report__mutmut_18': x_create_report__mutmut_18, 
    'x_create_report__mutmut_19': x_create_report__mutmut_19, 
    'x_create_report__mutmut_20': x_create_report__mutmut_20, 
    'x_create_report__mutmut_21': x_create_report__mutmut_21, 
    'x_create_report__mutmut_22': x_create_report__mutmut_22, 
    'x_create_report__mutmut_23': x_create_report__mutmut_23, 
    'x_create_report__mutmut_24': x_create_report__mutmut_24, 
    'x_create_report__mutmut_25': x_create_report__mutmut_25, 
    'x_create_report__mutmut_26': x_create_report__mutmut_26, 
    'x_create_report__mutmut_27': x_create_report__mutmut_27, 
    'x_create_report__mutmut_28': x_create_report__mutmut_28
}

def create_report(*args, **kwargs):
    result = _mutmut_trampoline(x_create_report__mutmut_orig, x_create_report__mutmut_mutants, args, kwargs)
    return result 

create_report.__signature__ = _mutmut_signature(x_create_report__mutmut_orig)
x_create_report__mutmut_orig.__name__ = 'x_create_report'


async def x_trigger_report_generation__mutmut_orig(report_id: str) -> None:
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


async def x_trigger_report_generation__mutmut_1(report_id: str) -> None:
    """
    Trigger AI report generation after payment succeeds
    Updates status from pending → generating → completed
    """
    supabase = None

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


async def x_trigger_report_generation__mutmut_2(report_id: str) -> None:
    """
    Trigger AI report generation after payment succeeds
    Updates status from pending → generating → completed
    """
    supabase = get_supabase()

    try:
        # Get report
        report_result = None

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


async def x_trigger_report_generation__mutmut_3(report_id: str) -> None:
    """
    Trigger AI report generation after payment succeeds
    Updates status from pending → generating → completed
    """
    supabase = get_supabase()

    try:
        # Get report
        report_result = supabase.table("reports").select("*").eq(None, report_id).execute()

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


async def x_trigger_report_generation__mutmut_4(report_id: str) -> None:
    """
    Trigger AI report generation after payment succeeds
    Updates status from pending → generating → completed
    """
    supabase = get_supabase()

    try:
        # Get report
        report_result = supabase.table("reports").select("*").eq("id", None).execute()

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


async def x_trigger_report_generation__mutmut_5(report_id: str) -> None:
    """
    Trigger AI report generation after payment succeeds
    Updates status from pending → generating → completed
    """
    supabase = get_supabase()

    try:
        # Get report
        report_result = supabase.table("reports").select("*").eq(report_id).execute()

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


async def x_trigger_report_generation__mutmut_6(report_id: str) -> None:
    """
    Trigger AI report generation after payment succeeds
    Updates status from pending → generating → completed
    """
    supabase = get_supabase()

    try:
        # Get report
        report_result = supabase.table("reports").select("*").eq("id", ).execute()

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


async def x_trigger_report_generation__mutmut_7(report_id: str) -> None:
    """
    Trigger AI report generation after payment succeeds
    Updates status from pending → generating → completed
    """
    supabase = get_supabase()

    try:
        # Get report
        report_result = supabase.table("reports").select(None).eq("id", report_id).execute()

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


async def x_trigger_report_generation__mutmut_8(report_id: str) -> None:
    """
    Trigger AI report generation after payment succeeds
    Updates status from pending → generating → completed
    """
    supabase = get_supabase()

    try:
        # Get report
        report_result = supabase.table(None).select("*").eq("id", report_id).execute()

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


async def x_trigger_report_generation__mutmut_9(report_id: str) -> None:
    """
    Trigger AI report generation after payment succeeds
    Updates status from pending → generating → completed
    """
    supabase = get_supabase()

    try:
        # Get report
        report_result = supabase.table("XXreportsXX").select("*").eq("id", report_id).execute()

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


async def x_trigger_report_generation__mutmut_10(report_id: str) -> None:
    """
    Trigger AI report generation after payment succeeds
    Updates status from pending → generating → completed
    """
    supabase = get_supabase()

    try:
        # Get report
        report_result = supabase.table("REPORTS").select("*").eq("id", report_id).execute()

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


async def x_trigger_report_generation__mutmut_11(report_id: str) -> None:
    """
    Trigger AI report generation after payment succeeds
    Updates status from pending → generating → completed
    """
    supabase = get_supabase()

    try:
        # Get report
        report_result = supabase.table("reports").select("XX*XX").eq("id", report_id).execute()

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


async def x_trigger_report_generation__mutmut_12(report_id: str) -> None:
    """
    Trigger AI report generation after payment succeeds
    Updates status from pending → generating → completed
    """
    supabase = get_supabase()

    try:
        # Get report
        report_result = supabase.table("reports").select("*").eq("XXidXX", report_id).execute()

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


async def x_trigger_report_generation__mutmut_13(report_id: str) -> None:
    """
    Trigger AI report generation after payment succeeds
    Updates status from pending → generating → completed
    """
    supabase = get_supabase()

    try:
        # Get report
        report_result = supabase.table("reports").select("*").eq("ID", report_id).execute()

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


async def x_trigger_report_generation__mutmut_14(report_id: str) -> None:
    """
    Trigger AI report generation after payment succeeds
    Updates status from pending → generating → completed
    """
    supabase = get_supabase()

    try:
        # Get report
        report_result = supabase.table("reports").select("*").eq("id", report_id).execute()

        if not report_result.data and len(report_result.data) == 0:
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


async def x_trigger_report_generation__mutmut_15(report_id: str) -> None:
    """
    Trigger AI report generation after payment succeeds
    Updates status from pending → generating → completed
    """
    supabase = get_supabase()

    try:
        # Get report
        report_result = supabase.table("reports").select("*").eq("id", report_id).execute()

        if report_result.data or len(report_result.data) == 0:
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


async def x_trigger_report_generation__mutmut_16(report_id: str) -> None:
    """
    Trigger AI report generation after payment succeeds
    Updates status from pending → generating → completed
    """
    supabase = get_supabase()

    try:
        # Get report
        report_result = supabase.table("reports").select("*").eq("id", report_id).execute()

        if not report_result.data or len(report_result.data) != 0:
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


async def x_trigger_report_generation__mutmut_17(report_id: str) -> None:
    """
    Trigger AI report generation after payment succeeds
    Updates status from pending → generating → completed
    """
    supabase = get_supabase()

    try:
        # Get report
        report_result = supabase.table("reports").select("*").eq("id", report_id).execute()

        if not report_result.data or len(report_result.data) == 1:
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


async def x_trigger_report_generation__mutmut_18(report_id: str) -> None:
    """
    Trigger AI report generation after payment succeeds
    Updates status from pending → generating → completed
    """
    supabase = get_supabase()

    try:
        # Get report
        report_result = supabase.table("reports").select("*").eq("id", report_id).execute()

        if not report_result.data or len(report_result.data) == 0:
            raise Exception(None)

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


async def x_trigger_report_generation__mutmut_19(report_id: str) -> None:
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

        report_data = None
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


async def x_trigger_report_generation__mutmut_20(report_id: str) -> None:
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

        report_data = report_result.data[1]
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


async def x_trigger_report_generation__mutmut_21(report_id: str) -> None:
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
        query = None

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


async def x_trigger_report_generation__mutmut_22(report_id: str) -> None:
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
        query = report_data["XXqueryXX"]

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


async def x_trigger_report_generation__mutmut_23(report_id: str) -> None:
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
        query = report_data["QUERY"]

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


async def x_trigger_report_generation__mutmut_24(report_id: str) -> None:
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
        ).eq(None, report_id).execute()

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


async def x_trigger_report_generation__mutmut_25(report_id: str) -> None:
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
        ).eq("id", None).execute()

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


async def x_trigger_report_generation__mutmut_26(report_id: str) -> None:
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
        ).eq(report_id).execute()

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


async def x_trigger_report_generation__mutmut_27(report_id: str) -> None:
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
        ).eq("id", ).execute()

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


async def x_trigger_report_generation__mutmut_28(report_id: str) -> None:
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
            None
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


async def x_trigger_report_generation__mutmut_29(report_id: str) -> None:
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
        supabase.table(None).update(
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


async def x_trigger_report_generation__mutmut_30(report_id: str) -> None:
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
        supabase.table("XXreportsXX").update(
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


async def x_trigger_report_generation__mutmut_31(report_id: str) -> None:
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
        supabase.table("REPORTS").update(
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


async def x_trigger_report_generation__mutmut_32(report_id: str) -> None:
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
                "XXstatusXX": ReportStatus.GENERATING.value,
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


async def x_trigger_report_generation__mutmut_33(report_id: str) -> None:
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
                "STATUS": ReportStatus.GENERATING.value,
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


async def x_trigger_report_generation__mutmut_34(report_id: str) -> None:
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
                "XXupdated_atXX": datetime.utcnow().isoformat(),
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


async def x_trigger_report_generation__mutmut_35(report_id: str) -> None:
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
                "UPDATED_AT": datetime.utcnow().isoformat(),
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


async def x_trigger_report_generation__mutmut_36(report_id: str) -> None:
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
        ).eq("XXidXX", report_id).execute()

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


async def x_trigger_report_generation__mutmut_37(report_id: str) -> None:
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
        ).eq("ID", report_id).execute()

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


async def x_trigger_report_generation__mutmut_38(report_id: str) -> None:
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
        report_content = None

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


async def x_trigger_report_generation__mutmut_39(report_id: str) -> None:
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
        report_content = await generate_report(None)

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


async def x_trigger_report_generation__mutmut_40(report_id: str) -> None:
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
        ).eq(None, report_id).execute()

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


async def x_trigger_report_generation__mutmut_41(report_id: str) -> None:
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
        ).eq("id", None).execute()

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


async def x_trigger_report_generation__mutmut_42(report_id: str) -> None:
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
        ).eq(report_id).execute()

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


async def x_trigger_report_generation__mutmut_43(report_id: str) -> None:
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
        ).eq("id", ).execute()

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


async def x_trigger_report_generation__mutmut_44(report_id: str) -> None:
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
            None
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


async def x_trigger_report_generation__mutmut_45(report_id: str) -> None:
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
        supabase.table(None).update(
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


async def x_trigger_report_generation__mutmut_46(report_id: str) -> None:
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
        supabase.table("XXreportsXX").update(
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


async def x_trigger_report_generation__mutmut_47(report_id: str) -> None:
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
        supabase.table("REPORTS").update(
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


async def x_trigger_report_generation__mutmut_48(report_id: str) -> None:
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
                "XXstatusXX": ReportStatus.COMPLETED.value,
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


async def x_trigger_report_generation__mutmut_49(report_id: str) -> None:
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
                "STATUS": ReportStatus.COMPLETED.value,
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


async def x_trigger_report_generation__mutmut_50(report_id: str) -> None:
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
                "XXcontentXX": report_content.dict(),
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


async def x_trigger_report_generation__mutmut_51(report_id: str) -> None:
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
                "CONTENT": report_content.dict(),
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


async def x_trigger_report_generation__mutmut_52(report_id: str) -> None:
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
                "XXupdated_atXX": datetime.utcnow().isoformat(),
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


async def x_trigger_report_generation__mutmut_53(report_id: str) -> None:
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
                "UPDATED_AT": datetime.utcnow().isoformat(),
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


async def x_trigger_report_generation__mutmut_54(report_id: str) -> None:
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
        ).eq("XXidXX", report_id).execute()

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


async def x_trigger_report_generation__mutmut_55(report_id: str) -> None:
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
        ).eq("ID", report_id).execute()

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


async def x_trigger_report_generation__mutmut_56(report_id: str) -> None:
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
        ).eq(None, report_id).execute()

        raise e


async def x_trigger_report_generation__mutmut_57(report_id: str) -> None:
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
        ).eq("id", None).execute()

        raise e


async def x_trigger_report_generation__mutmut_58(report_id: str) -> None:
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
        ).eq(report_id).execute()

        raise e


async def x_trigger_report_generation__mutmut_59(report_id: str) -> None:
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
        ).eq("id", ).execute()

        raise e


async def x_trigger_report_generation__mutmut_60(report_id: str) -> None:
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
            None
        ).eq("id", report_id).execute()

        raise e


async def x_trigger_report_generation__mutmut_61(report_id: str) -> None:
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
        supabase.table(None).update(
            {
                "status": ReportStatus.FAILED.value,
                "error": str(e),
                "updated_at": datetime.utcnow().isoformat(),
            }
        ).eq("id", report_id).execute()

        raise e


async def x_trigger_report_generation__mutmut_62(report_id: str) -> None:
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
        supabase.table("XXreportsXX").update(
            {
                "status": ReportStatus.FAILED.value,
                "error": str(e),
                "updated_at": datetime.utcnow().isoformat(),
            }
        ).eq("id", report_id).execute()

        raise e


async def x_trigger_report_generation__mutmut_63(report_id: str) -> None:
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
        supabase.table("REPORTS").update(
            {
                "status": ReportStatus.FAILED.value,
                "error": str(e),
                "updated_at": datetime.utcnow().isoformat(),
            }
        ).eq("id", report_id).execute()

        raise e


async def x_trigger_report_generation__mutmut_64(report_id: str) -> None:
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
                "XXstatusXX": ReportStatus.FAILED.value,
                "error": str(e),
                "updated_at": datetime.utcnow().isoformat(),
            }
        ).eq("id", report_id).execute()

        raise e


async def x_trigger_report_generation__mutmut_65(report_id: str) -> None:
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
                "STATUS": ReportStatus.FAILED.value,
                "error": str(e),
                "updated_at": datetime.utcnow().isoformat(),
            }
        ).eq("id", report_id).execute()

        raise e


async def x_trigger_report_generation__mutmut_66(report_id: str) -> None:
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
                "XXerrorXX": str(e),
                "updated_at": datetime.utcnow().isoformat(),
            }
        ).eq("id", report_id).execute()

        raise e


async def x_trigger_report_generation__mutmut_67(report_id: str) -> None:
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
                "ERROR": str(e),
                "updated_at": datetime.utcnow().isoformat(),
            }
        ).eq("id", report_id).execute()

        raise e


async def x_trigger_report_generation__mutmut_68(report_id: str) -> None:
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
                "error": str(None),
                "updated_at": datetime.utcnow().isoformat(),
            }
        ).eq("id", report_id).execute()

        raise e


async def x_trigger_report_generation__mutmut_69(report_id: str) -> None:
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
                "XXupdated_atXX": datetime.utcnow().isoformat(),
            }
        ).eq("id", report_id).execute()

        raise e


async def x_trigger_report_generation__mutmut_70(report_id: str) -> None:
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
                "UPDATED_AT": datetime.utcnow().isoformat(),
            }
        ).eq("id", report_id).execute()

        raise e


async def x_trigger_report_generation__mutmut_71(report_id: str) -> None:
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
        ).eq("XXidXX", report_id).execute()

        raise e


async def x_trigger_report_generation__mutmut_72(report_id: str) -> None:
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
        ).eq("ID", report_id).execute()

        raise e

x_trigger_report_generation__mutmut_mutants : ClassVar[MutantDict] = {
'x_trigger_report_generation__mutmut_1': x_trigger_report_generation__mutmut_1, 
    'x_trigger_report_generation__mutmut_2': x_trigger_report_generation__mutmut_2, 
    'x_trigger_report_generation__mutmut_3': x_trigger_report_generation__mutmut_3, 
    'x_trigger_report_generation__mutmut_4': x_trigger_report_generation__mutmut_4, 
    'x_trigger_report_generation__mutmut_5': x_trigger_report_generation__mutmut_5, 
    'x_trigger_report_generation__mutmut_6': x_trigger_report_generation__mutmut_6, 
    'x_trigger_report_generation__mutmut_7': x_trigger_report_generation__mutmut_7, 
    'x_trigger_report_generation__mutmut_8': x_trigger_report_generation__mutmut_8, 
    'x_trigger_report_generation__mutmut_9': x_trigger_report_generation__mutmut_9, 
    'x_trigger_report_generation__mutmut_10': x_trigger_report_generation__mutmut_10, 
    'x_trigger_report_generation__mutmut_11': x_trigger_report_generation__mutmut_11, 
    'x_trigger_report_generation__mutmut_12': x_trigger_report_generation__mutmut_12, 
    'x_trigger_report_generation__mutmut_13': x_trigger_report_generation__mutmut_13, 
    'x_trigger_report_generation__mutmut_14': x_trigger_report_generation__mutmut_14, 
    'x_trigger_report_generation__mutmut_15': x_trigger_report_generation__mutmut_15, 
    'x_trigger_report_generation__mutmut_16': x_trigger_report_generation__mutmut_16, 
    'x_trigger_report_generation__mutmut_17': x_trigger_report_generation__mutmut_17, 
    'x_trigger_report_generation__mutmut_18': x_trigger_report_generation__mutmut_18, 
    'x_trigger_report_generation__mutmut_19': x_trigger_report_generation__mutmut_19, 
    'x_trigger_report_generation__mutmut_20': x_trigger_report_generation__mutmut_20, 
    'x_trigger_report_generation__mutmut_21': x_trigger_report_generation__mutmut_21, 
    'x_trigger_report_generation__mutmut_22': x_trigger_report_generation__mutmut_22, 
    'x_trigger_report_generation__mutmut_23': x_trigger_report_generation__mutmut_23, 
    'x_trigger_report_generation__mutmut_24': x_trigger_report_generation__mutmut_24, 
    'x_trigger_report_generation__mutmut_25': x_trigger_report_generation__mutmut_25, 
    'x_trigger_report_generation__mutmut_26': x_trigger_report_generation__mutmut_26, 
    'x_trigger_report_generation__mutmut_27': x_trigger_report_generation__mutmut_27, 
    'x_trigger_report_generation__mutmut_28': x_trigger_report_generation__mutmut_28, 
    'x_trigger_report_generation__mutmut_29': x_trigger_report_generation__mutmut_29, 
    'x_trigger_report_generation__mutmut_30': x_trigger_report_generation__mutmut_30, 
    'x_trigger_report_generation__mutmut_31': x_trigger_report_generation__mutmut_31, 
    'x_trigger_report_generation__mutmut_32': x_trigger_report_generation__mutmut_32, 
    'x_trigger_report_generation__mutmut_33': x_trigger_report_generation__mutmut_33, 
    'x_trigger_report_generation__mutmut_34': x_trigger_report_generation__mutmut_34, 
    'x_trigger_report_generation__mutmut_35': x_trigger_report_generation__mutmut_35, 
    'x_trigger_report_generation__mutmut_36': x_trigger_report_generation__mutmut_36, 
    'x_trigger_report_generation__mutmut_37': x_trigger_report_generation__mutmut_37, 
    'x_trigger_report_generation__mutmut_38': x_trigger_report_generation__mutmut_38, 
    'x_trigger_report_generation__mutmut_39': x_trigger_report_generation__mutmut_39, 
    'x_trigger_report_generation__mutmut_40': x_trigger_report_generation__mutmut_40, 
    'x_trigger_report_generation__mutmut_41': x_trigger_report_generation__mutmut_41, 
    'x_trigger_report_generation__mutmut_42': x_trigger_report_generation__mutmut_42, 
    'x_trigger_report_generation__mutmut_43': x_trigger_report_generation__mutmut_43, 
    'x_trigger_report_generation__mutmut_44': x_trigger_report_generation__mutmut_44, 
    'x_trigger_report_generation__mutmut_45': x_trigger_report_generation__mutmut_45, 
    'x_trigger_report_generation__mutmut_46': x_trigger_report_generation__mutmut_46, 
    'x_trigger_report_generation__mutmut_47': x_trigger_report_generation__mutmut_47, 
    'x_trigger_report_generation__mutmut_48': x_trigger_report_generation__mutmut_48, 
    'x_trigger_report_generation__mutmut_49': x_trigger_report_generation__mutmut_49, 
    'x_trigger_report_generation__mutmut_50': x_trigger_report_generation__mutmut_50, 
    'x_trigger_report_generation__mutmut_51': x_trigger_report_generation__mutmut_51, 
    'x_trigger_report_generation__mutmut_52': x_trigger_report_generation__mutmut_52, 
    'x_trigger_report_generation__mutmut_53': x_trigger_report_generation__mutmut_53, 
    'x_trigger_report_generation__mutmut_54': x_trigger_report_generation__mutmut_54, 
    'x_trigger_report_generation__mutmut_55': x_trigger_report_generation__mutmut_55, 
    'x_trigger_report_generation__mutmut_56': x_trigger_report_generation__mutmut_56, 
    'x_trigger_report_generation__mutmut_57': x_trigger_report_generation__mutmut_57, 
    'x_trigger_report_generation__mutmut_58': x_trigger_report_generation__mutmut_58, 
    'x_trigger_report_generation__mutmut_59': x_trigger_report_generation__mutmut_59, 
    'x_trigger_report_generation__mutmut_60': x_trigger_report_generation__mutmut_60, 
    'x_trigger_report_generation__mutmut_61': x_trigger_report_generation__mutmut_61, 
    'x_trigger_report_generation__mutmut_62': x_trigger_report_generation__mutmut_62, 
    'x_trigger_report_generation__mutmut_63': x_trigger_report_generation__mutmut_63, 
    'x_trigger_report_generation__mutmut_64': x_trigger_report_generation__mutmut_64, 
    'x_trigger_report_generation__mutmut_65': x_trigger_report_generation__mutmut_65, 
    'x_trigger_report_generation__mutmut_66': x_trigger_report_generation__mutmut_66, 
    'x_trigger_report_generation__mutmut_67': x_trigger_report_generation__mutmut_67, 
    'x_trigger_report_generation__mutmut_68': x_trigger_report_generation__mutmut_68, 
    'x_trigger_report_generation__mutmut_69': x_trigger_report_generation__mutmut_69, 
    'x_trigger_report_generation__mutmut_70': x_trigger_report_generation__mutmut_70, 
    'x_trigger_report_generation__mutmut_71': x_trigger_report_generation__mutmut_71, 
    'x_trigger_report_generation__mutmut_72': x_trigger_report_generation__mutmut_72
}

def trigger_report_generation(*args, **kwargs):
    result = _mutmut_trampoline(x_trigger_report_generation__mutmut_orig, x_trigger_report_generation__mutmut_mutants, args, kwargs)
    return result 

trigger_report_generation.__signature__ = _mutmut_signature(x_trigger_report_generation__mutmut_orig)
x_trigger_report_generation__mutmut_orig.__name__ = 'x_trigger_report_generation'


async def x_get_report__mutmut_orig(report_id: str, user_id: str) -> Optional[Report]:
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


async def x_get_report__mutmut_1(report_id: str, user_id: str) -> Optional[Report]:
    """
    Get report by ID (with user ownership check)
    """
    supabase = None

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


async def x_get_report__mutmut_2(report_id: str, user_id: str) -> Optional[Report]:
    """
    Get report by ID (with user ownership check)
    """
    supabase = get_supabase()

    result = None

    if result.data and len(result.data) > 0:
        return Report(**result.data[0])
    return None


async def x_get_report__mutmut_3(report_id: str, user_id: str) -> Optional[Report]:
    """
    Get report by ID (with user ownership check)
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .select("*")
        .eq("id", report_id)
        .eq("user_id", user_id)
        .is_(None, "null")
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Report(**result.data[0])
    return None


async def x_get_report__mutmut_4(report_id: str, user_id: str) -> Optional[Report]:
    """
    Get report by ID (with user ownership check)
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .select("*")
        .eq("id", report_id)
        .eq("user_id", user_id)
        .is_("deleted_at", None)
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Report(**result.data[0])
    return None


async def x_get_report__mutmut_5(report_id: str, user_id: str) -> Optional[Report]:
    """
    Get report by ID (with user ownership check)
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .select("*")
        .eq("id", report_id)
        .eq("user_id", user_id)
        .is_("null")
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Report(**result.data[0])
    return None


async def x_get_report__mutmut_6(report_id: str, user_id: str) -> Optional[Report]:
    """
    Get report by ID (with user ownership check)
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .select("*")
        .eq("id", report_id)
        .eq("user_id", user_id)
        .is_("deleted_at", )
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Report(**result.data[0])
    return None


async def x_get_report__mutmut_7(report_id: str, user_id: str) -> Optional[Report]:
    """
    Get report by ID (with user ownership check)
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .select("*")
        .eq("id", report_id)
        .eq(None, user_id)
        .is_("deleted_at", "null")
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Report(**result.data[0])
    return None


async def x_get_report__mutmut_8(report_id: str, user_id: str) -> Optional[Report]:
    """
    Get report by ID (with user ownership check)
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .select("*")
        .eq("id", report_id)
        .eq("user_id", None)
        .is_("deleted_at", "null")
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Report(**result.data[0])
    return None


async def x_get_report__mutmut_9(report_id: str, user_id: str) -> Optional[Report]:
    """
    Get report by ID (with user ownership check)
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .select("*")
        .eq("id", report_id)
        .eq(user_id)
        .is_("deleted_at", "null")
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Report(**result.data[0])
    return None


async def x_get_report__mutmut_10(report_id: str, user_id: str) -> Optional[Report]:
    """
    Get report by ID (with user ownership check)
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .select("*")
        .eq("id", report_id)
        .eq("user_id", )
        .is_("deleted_at", "null")
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Report(**result.data[0])
    return None


async def x_get_report__mutmut_11(report_id: str, user_id: str) -> Optional[Report]:
    """
    Get report by ID (with user ownership check)
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .select("*")
        .eq(None, report_id)
        .eq("user_id", user_id)
        .is_("deleted_at", "null")
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Report(**result.data[0])
    return None


async def x_get_report__mutmut_12(report_id: str, user_id: str) -> Optional[Report]:
    """
    Get report by ID (with user ownership check)
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .select("*")
        .eq("id", None)
        .eq("user_id", user_id)
        .is_("deleted_at", "null")
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Report(**result.data[0])
    return None


async def x_get_report__mutmut_13(report_id: str, user_id: str) -> Optional[Report]:
    """
    Get report by ID (with user ownership check)
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .select("*")
        .eq(report_id)
        .eq("user_id", user_id)
        .is_("deleted_at", "null")
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Report(**result.data[0])
    return None


async def x_get_report__mutmut_14(report_id: str, user_id: str) -> Optional[Report]:
    """
    Get report by ID (with user ownership check)
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .select("*")
        .eq("id", )
        .eq("user_id", user_id)
        .is_("deleted_at", "null")
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Report(**result.data[0])
    return None


async def x_get_report__mutmut_15(report_id: str, user_id: str) -> Optional[Report]:
    """
    Get report by ID (with user ownership check)
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .select(None)
        .eq("id", report_id)
        .eq("user_id", user_id)
        .is_("deleted_at", "null")
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Report(**result.data[0])
    return None


async def x_get_report__mutmut_16(report_id: str, user_id: str) -> Optional[Report]:
    """
    Get report by ID (with user ownership check)
    """
    supabase = get_supabase()

    result = (
        supabase.table(None)
        .select("*")
        .eq("id", report_id)
        .eq("user_id", user_id)
        .is_("deleted_at", "null")
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Report(**result.data[0])
    return None


async def x_get_report__mutmut_17(report_id: str, user_id: str) -> Optional[Report]:
    """
    Get report by ID (with user ownership check)
    """
    supabase = get_supabase()

    result = (
        supabase.table("XXreportsXX")
        .select("*")
        .eq("id", report_id)
        .eq("user_id", user_id)
        .is_("deleted_at", "null")
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Report(**result.data[0])
    return None


async def x_get_report__mutmut_18(report_id: str, user_id: str) -> Optional[Report]:
    """
    Get report by ID (with user ownership check)
    """
    supabase = get_supabase()

    result = (
        supabase.table("REPORTS")
        .select("*")
        .eq("id", report_id)
        .eq("user_id", user_id)
        .is_("deleted_at", "null")
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Report(**result.data[0])
    return None


async def x_get_report__mutmut_19(report_id: str, user_id: str) -> Optional[Report]:
    """
    Get report by ID (with user ownership check)
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .select("XX*XX")
        .eq("id", report_id)
        .eq("user_id", user_id)
        .is_("deleted_at", "null")
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Report(**result.data[0])
    return None


async def x_get_report__mutmut_20(report_id: str, user_id: str) -> Optional[Report]:
    """
    Get report by ID (with user ownership check)
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .select("*")
        .eq("XXidXX", report_id)
        .eq("user_id", user_id)
        .is_("deleted_at", "null")
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Report(**result.data[0])
    return None


async def x_get_report__mutmut_21(report_id: str, user_id: str) -> Optional[Report]:
    """
    Get report by ID (with user ownership check)
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .select("*")
        .eq("ID", report_id)
        .eq("user_id", user_id)
        .is_("deleted_at", "null")
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Report(**result.data[0])
    return None


async def x_get_report__mutmut_22(report_id: str, user_id: str) -> Optional[Report]:
    """
    Get report by ID (with user ownership check)
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .select("*")
        .eq("id", report_id)
        .eq("XXuser_idXX", user_id)
        .is_("deleted_at", "null")
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Report(**result.data[0])
    return None


async def x_get_report__mutmut_23(report_id: str, user_id: str) -> Optional[Report]:
    """
    Get report by ID (with user ownership check)
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .select("*")
        .eq("id", report_id)
        .eq("USER_ID", user_id)
        .is_("deleted_at", "null")
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Report(**result.data[0])
    return None


async def x_get_report__mutmut_24(report_id: str, user_id: str) -> Optional[Report]:
    """
    Get report by ID (with user ownership check)
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .select("*")
        .eq("id", report_id)
        .eq("user_id", user_id)
        .is_("XXdeleted_atXX", "null")
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Report(**result.data[0])
    return None


async def x_get_report__mutmut_25(report_id: str, user_id: str) -> Optional[Report]:
    """
    Get report by ID (with user ownership check)
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .select("*")
        .eq("id", report_id)
        .eq("user_id", user_id)
        .is_("DELETED_AT", "null")
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Report(**result.data[0])
    return None


async def x_get_report__mutmut_26(report_id: str, user_id: str) -> Optional[Report]:
    """
    Get report by ID (with user ownership check)
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .select("*")
        .eq("id", report_id)
        .eq("user_id", user_id)
        .is_("deleted_at", "XXnullXX")
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Report(**result.data[0])
    return None


async def x_get_report__mutmut_27(report_id: str, user_id: str) -> Optional[Report]:
    """
    Get report by ID (with user ownership check)
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .select("*")
        .eq("id", report_id)
        .eq("user_id", user_id)
        .is_("deleted_at", "NULL")
        .execute()
    )

    if result.data and len(result.data) > 0:
        return Report(**result.data[0])
    return None


async def x_get_report__mutmut_28(report_id: str, user_id: str) -> Optional[Report]:
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

    if result.data or len(result.data) > 0:
        return Report(**result.data[0])
    return None


async def x_get_report__mutmut_29(report_id: str, user_id: str) -> Optional[Report]:
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

    if result.data and len(result.data) >= 0:
        return Report(**result.data[0])
    return None


async def x_get_report__mutmut_30(report_id: str, user_id: str) -> Optional[Report]:
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

    if result.data and len(result.data) > 1:
        return Report(**result.data[0])
    return None


async def x_get_report__mutmut_31(report_id: str, user_id: str) -> Optional[Report]:
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
        return Report(**result.data[1])
    return None

x_get_report__mutmut_mutants : ClassVar[MutantDict] = {
'x_get_report__mutmut_1': x_get_report__mutmut_1, 
    'x_get_report__mutmut_2': x_get_report__mutmut_2, 
    'x_get_report__mutmut_3': x_get_report__mutmut_3, 
    'x_get_report__mutmut_4': x_get_report__mutmut_4, 
    'x_get_report__mutmut_5': x_get_report__mutmut_5, 
    'x_get_report__mutmut_6': x_get_report__mutmut_6, 
    'x_get_report__mutmut_7': x_get_report__mutmut_7, 
    'x_get_report__mutmut_8': x_get_report__mutmut_8, 
    'x_get_report__mutmut_9': x_get_report__mutmut_9, 
    'x_get_report__mutmut_10': x_get_report__mutmut_10, 
    'x_get_report__mutmut_11': x_get_report__mutmut_11, 
    'x_get_report__mutmut_12': x_get_report__mutmut_12, 
    'x_get_report__mutmut_13': x_get_report__mutmut_13, 
    'x_get_report__mutmut_14': x_get_report__mutmut_14, 
    'x_get_report__mutmut_15': x_get_report__mutmut_15, 
    'x_get_report__mutmut_16': x_get_report__mutmut_16, 
    'x_get_report__mutmut_17': x_get_report__mutmut_17, 
    'x_get_report__mutmut_18': x_get_report__mutmut_18, 
    'x_get_report__mutmut_19': x_get_report__mutmut_19, 
    'x_get_report__mutmut_20': x_get_report__mutmut_20, 
    'x_get_report__mutmut_21': x_get_report__mutmut_21, 
    'x_get_report__mutmut_22': x_get_report__mutmut_22, 
    'x_get_report__mutmut_23': x_get_report__mutmut_23, 
    'x_get_report__mutmut_24': x_get_report__mutmut_24, 
    'x_get_report__mutmut_25': x_get_report__mutmut_25, 
    'x_get_report__mutmut_26': x_get_report__mutmut_26, 
    'x_get_report__mutmut_27': x_get_report__mutmut_27, 
    'x_get_report__mutmut_28': x_get_report__mutmut_28, 
    'x_get_report__mutmut_29': x_get_report__mutmut_29, 
    'x_get_report__mutmut_30': x_get_report__mutmut_30, 
    'x_get_report__mutmut_31': x_get_report__mutmut_31
}

def get_report(*args, **kwargs):
    result = _mutmut_trampoline(x_get_report__mutmut_orig, x_get_report__mutmut_mutants, args, kwargs)
    return result 

get_report.__signature__ = _mutmut_signature(x_get_report__mutmut_orig)
x_get_report__mutmut_orig.__name__ = 'x_get_report'


async def x_list_user_reports__mutmut_orig(user_id: str, limit: int = 50) -> List[ReportListItem]:
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


async def x_list_user_reports__mutmut_1(user_id: str, limit: int = 51) -> List[ReportListItem]:
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


async def x_list_user_reports__mutmut_2(user_id: str, limit: int = 50) -> List[ReportListItem]:
    """
    List all reports for a user
    """
    supabase = None

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


async def x_list_user_reports__mutmut_3(user_id: str, limit: int = 50) -> List[ReportListItem]:
    """
    List all reports for a user
    """
    supabase = get_supabase()

    result = None

    return [ReportListItem(**item) for item in result.data]


async def x_list_user_reports__mutmut_4(user_id: str, limit: int = 50) -> List[ReportListItem]:
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
        .limit(None)
        .execute()
    )

    return [ReportListItem(**item) for item in result.data]


async def x_list_user_reports__mutmut_5(user_id: str, limit: int = 50) -> List[ReportListItem]:
    """
    List all reports for a user
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .select("id, query, status, created_at, expires_at")
        .eq("user_id", user_id)
        .is_("deleted_at", "null")
        .order(None, desc=True)
        .limit(limit)
        .execute()
    )

    return [ReportListItem(**item) for item in result.data]


async def x_list_user_reports__mutmut_6(user_id: str, limit: int = 50) -> List[ReportListItem]:
    """
    List all reports for a user
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .select("id, query, status, created_at, expires_at")
        .eq("user_id", user_id)
        .is_("deleted_at", "null")
        .order("created_at", desc=None)
        .limit(limit)
        .execute()
    )

    return [ReportListItem(**item) for item in result.data]


async def x_list_user_reports__mutmut_7(user_id: str, limit: int = 50) -> List[ReportListItem]:
    """
    List all reports for a user
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .select("id, query, status, created_at, expires_at")
        .eq("user_id", user_id)
        .is_("deleted_at", "null")
        .order(desc=True)
        .limit(limit)
        .execute()
    )

    return [ReportListItem(**item) for item in result.data]


async def x_list_user_reports__mutmut_8(user_id: str, limit: int = 50) -> List[ReportListItem]:
    """
    List all reports for a user
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .select("id, query, status, created_at, expires_at")
        .eq("user_id", user_id)
        .is_("deleted_at", "null")
        .order("created_at", )
        .limit(limit)
        .execute()
    )

    return [ReportListItem(**item) for item in result.data]


async def x_list_user_reports__mutmut_9(user_id: str, limit: int = 50) -> List[ReportListItem]:
    """
    List all reports for a user
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .select("id, query, status, created_at, expires_at")
        .eq("user_id", user_id)
        .is_(None, "null")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )

    return [ReportListItem(**item) for item in result.data]


async def x_list_user_reports__mutmut_10(user_id: str, limit: int = 50) -> List[ReportListItem]:
    """
    List all reports for a user
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .select("id, query, status, created_at, expires_at")
        .eq("user_id", user_id)
        .is_("deleted_at", None)
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )

    return [ReportListItem(**item) for item in result.data]


async def x_list_user_reports__mutmut_11(user_id: str, limit: int = 50) -> List[ReportListItem]:
    """
    List all reports for a user
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .select("id, query, status, created_at, expires_at")
        .eq("user_id", user_id)
        .is_("null")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )

    return [ReportListItem(**item) for item in result.data]


async def x_list_user_reports__mutmut_12(user_id: str, limit: int = 50) -> List[ReportListItem]:
    """
    List all reports for a user
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .select("id, query, status, created_at, expires_at")
        .eq("user_id", user_id)
        .is_("deleted_at", )
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )

    return [ReportListItem(**item) for item in result.data]


async def x_list_user_reports__mutmut_13(user_id: str, limit: int = 50) -> List[ReportListItem]:
    """
    List all reports for a user
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .select("id, query, status, created_at, expires_at")
        .eq(None, user_id)
        .is_("deleted_at", "null")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )

    return [ReportListItem(**item) for item in result.data]


async def x_list_user_reports__mutmut_14(user_id: str, limit: int = 50) -> List[ReportListItem]:
    """
    List all reports for a user
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .select("id, query, status, created_at, expires_at")
        .eq("user_id", None)
        .is_("deleted_at", "null")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )

    return [ReportListItem(**item) for item in result.data]


async def x_list_user_reports__mutmut_15(user_id: str, limit: int = 50) -> List[ReportListItem]:
    """
    List all reports for a user
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .select("id, query, status, created_at, expires_at")
        .eq(user_id)
        .is_("deleted_at", "null")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )

    return [ReportListItem(**item) for item in result.data]


async def x_list_user_reports__mutmut_16(user_id: str, limit: int = 50) -> List[ReportListItem]:
    """
    List all reports for a user
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .select("id, query, status, created_at, expires_at")
        .eq("user_id", )
        .is_("deleted_at", "null")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )

    return [ReportListItem(**item) for item in result.data]


async def x_list_user_reports__mutmut_17(user_id: str, limit: int = 50) -> List[ReportListItem]:
    """
    List all reports for a user
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .select(None)
        .eq("user_id", user_id)
        .is_("deleted_at", "null")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )

    return [ReportListItem(**item) for item in result.data]


async def x_list_user_reports__mutmut_18(user_id: str, limit: int = 50) -> List[ReportListItem]:
    """
    List all reports for a user
    """
    supabase = get_supabase()

    result = (
        supabase.table(None)
        .select("id, query, status, created_at, expires_at")
        .eq("user_id", user_id)
        .is_("deleted_at", "null")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )

    return [ReportListItem(**item) for item in result.data]


async def x_list_user_reports__mutmut_19(user_id: str, limit: int = 50) -> List[ReportListItem]:
    """
    List all reports for a user
    """
    supabase = get_supabase()

    result = (
        supabase.table("XXreportsXX")
        .select("id, query, status, created_at, expires_at")
        .eq("user_id", user_id)
        .is_("deleted_at", "null")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )

    return [ReportListItem(**item) for item in result.data]


async def x_list_user_reports__mutmut_20(user_id: str, limit: int = 50) -> List[ReportListItem]:
    """
    List all reports for a user
    """
    supabase = get_supabase()

    result = (
        supabase.table("REPORTS")
        .select("id, query, status, created_at, expires_at")
        .eq("user_id", user_id)
        .is_("deleted_at", "null")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )

    return [ReportListItem(**item) for item in result.data]


async def x_list_user_reports__mutmut_21(user_id: str, limit: int = 50) -> List[ReportListItem]:
    """
    List all reports for a user
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .select("XXid, query, status, created_at, expires_atXX")
        .eq("user_id", user_id)
        .is_("deleted_at", "null")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )

    return [ReportListItem(**item) for item in result.data]


async def x_list_user_reports__mutmut_22(user_id: str, limit: int = 50) -> List[ReportListItem]:
    """
    List all reports for a user
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .select("ID, QUERY, STATUS, CREATED_AT, EXPIRES_AT")
        .eq("user_id", user_id)
        .is_("deleted_at", "null")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )

    return [ReportListItem(**item) for item in result.data]


async def x_list_user_reports__mutmut_23(user_id: str, limit: int = 50) -> List[ReportListItem]:
    """
    List all reports for a user
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .select("id, query, status, created_at, expires_at")
        .eq("XXuser_idXX", user_id)
        .is_("deleted_at", "null")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )

    return [ReportListItem(**item) for item in result.data]


async def x_list_user_reports__mutmut_24(user_id: str, limit: int = 50) -> List[ReportListItem]:
    """
    List all reports for a user
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .select("id, query, status, created_at, expires_at")
        .eq("USER_ID", user_id)
        .is_("deleted_at", "null")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )

    return [ReportListItem(**item) for item in result.data]


async def x_list_user_reports__mutmut_25(user_id: str, limit: int = 50) -> List[ReportListItem]:
    """
    List all reports for a user
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .select("id, query, status, created_at, expires_at")
        .eq("user_id", user_id)
        .is_("XXdeleted_atXX", "null")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )

    return [ReportListItem(**item) for item in result.data]


async def x_list_user_reports__mutmut_26(user_id: str, limit: int = 50) -> List[ReportListItem]:
    """
    List all reports for a user
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .select("id, query, status, created_at, expires_at")
        .eq("user_id", user_id)
        .is_("DELETED_AT", "null")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )

    return [ReportListItem(**item) for item in result.data]


async def x_list_user_reports__mutmut_27(user_id: str, limit: int = 50) -> List[ReportListItem]:
    """
    List all reports for a user
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .select("id, query, status, created_at, expires_at")
        .eq("user_id", user_id)
        .is_("deleted_at", "XXnullXX")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )

    return [ReportListItem(**item) for item in result.data]


async def x_list_user_reports__mutmut_28(user_id: str, limit: int = 50) -> List[ReportListItem]:
    """
    List all reports for a user
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .select("id, query, status, created_at, expires_at")
        .eq("user_id", user_id)
        .is_("deleted_at", "NULL")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )

    return [ReportListItem(**item) for item in result.data]


async def x_list_user_reports__mutmut_29(user_id: str, limit: int = 50) -> List[ReportListItem]:
    """
    List all reports for a user
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .select("id, query, status, created_at, expires_at")
        .eq("user_id", user_id)
        .is_("deleted_at", "null")
        .order("XXcreated_atXX", desc=True)
        .limit(limit)
        .execute()
    )

    return [ReportListItem(**item) for item in result.data]


async def x_list_user_reports__mutmut_30(user_id: str, limit: int = 50) -> List[ReportListItem]:
    """
    List all reports for a user
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .select("id, query, status, created_at, expires_at")
        .eq("user_id", user_id)
        .is_("deleted_at", "null")
        .order("CREATED_AT", desc=True)
        .limit(limit)
        .execute()
    )

    return [ReportListItem(**item) for item in result.data]


async def x_list_user_reports__mutmut_31(user_id: str, limit: int = 50) -> List[ReportListItem]:
    """
    List all reports for a user
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .select("id, query, status, created_at, expires_at")
        .eq("user_id", user_id)
        .is_("deleted_at", "null")
        .order("created_at", desc=False)
        .limit(limit)
        .execute()
    )

    return [ReportListItem(**item) for item in result.data]

x_list_user_reports__mutmut_mutants : ClassVar[MutantDict] = {
'x_list_user_reports__mutmut_1': x_list_user_reports__mutmut_1, 
    'x_list_user_reports__mutmut_2': x_list_user_reports__mutmut_2, 
    'x_list_user_reports__mutmut_3': x_list_user_reports__mutmut_3, 
    'x_list_user_reports__mutmut_4': x_list_user_reports__mutmut_4, 
    'x_list_user_reports__mutmut_5': x_list_user_reports__mutmut_5, 
    'x_list_user_reports__mutmut_6': x_list_user_reports__mutmut_6, 
    'x_list_user_reports__mutmut_7': x_list_user_reports__mutmut_7, 
    'x_list_user_reports__mutmut_8': x_list_user_reports__mutmut_8, 
    'x_list_user_reports__mutmut_9': x_list_user_reports__mutmut_9, 
    'x_list_user_reports__mutmut_10': x_list_user_reports__mutmut_10, 
    'x_list_user_reports__mutmut_11': x_list_user_reports__mutmut_11, 
    'x_list_user_reports__mutmut_12': x_list_user_reports__mutmut_12, 
    'x_list_user_reports__mutmut_13': x_list_user_reports__mutmut_13, 
    'x_list_user_reports__mutmut_14': x_list_user_reports__mutmut_14, 
    'x_list_user_reports__mutmut_15': x_list_user_reports__mutmut_15, 
    'x_list_user_reports__mutmut_16': x_list_user_reports__mutmut_16, 
    'x_list_user_reports__mutmut_17': x_list_user_reports__mutmut_17, 
    'x_list_user_reports__mutmut_18': x_list_user_reports__mutmut_18, 
    'x_list_user_reports__mutmut_19': x_list_user_reports__mutmut_19, 
    'x_list_user_reports__mutmut_20': x_list_user_reports__mutmut_20, 
    'x_list_user_reports__mutmut_21': x_list_user_reports__mutmut_21, 
    'x_list_user_reports__mutmut_22': x_list_user_reports__mutmut_22, 
    'x_list_user_reports__mutmut_23': x_list_user_reports__mutmut_23, 
    'x_list_user_reports__mutmut_24': x_list_user_reports__mutmut_24, 
    'x_list_user_reports__mutmut_25': x_list_user_reports__mutmut_25, 
    'x_list_user_reports__mutmut_26': x_list_user_reports__mutmut_26, 
    'x_list_user_reports__mutmut_27': x_list_user_reports__mutmut_27, 
    'x_list_user_reports__mutmut_28': x_list_user_reports__mutmut_28, 
    'x_list_user_reports__mutmut_29': x_list_user_reports__mutmut_29, 
    'x_list_user_reports__mutmut_30': x_list_user_reports__mutmut_30, 
    'x_list_user_reports__mutmut_31': x_list_user_reports__mutmut_31
}

def list_user_reports(*args, **kwargs):
    result = _mutmut_trampoline(x_list_user_reports__mutmut_orig, x_list_user_reports__mutmut_mutants, args, kwargs)
    return result 

list_user_reports.__signature__ = _mutmut_signature(x_list_user_reports__mutmut_orig)
x_list_user_reports__mutmut_orig.__name__ = 'x_list_user_reports'


async def x_update_report_status__mutmut_orig(report_id: str, status: str, error: Optional[str] = None) -> None:
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


async def x_update_report_status__mutmut_1(report_id: str, status: str, error: Optional[str] = None) -> None:
    """
    Update report status (used by streaming endpoint)
    """
    supabase = None

    update_data = {
        "status": status,
        "updated_at": datetime.utcnow().isoformat(),
    }

    if error:
        update_data["error"] = error

    supabase.table("reports").update(update_data).eq("id", report_id).execute()


async def x_update_report_status__mutmut_2(report_id: str, status: str, error: Optional[str] = None) -> None:
    """
    Update report status (used by streaming endpoint)
    """
    supabase = get_supabase()

    update_data = None

    if error:
        update_data["error"] = error

    supabase.table("reports").update(update_data).eq("id", report_id).execute()


async def x_update_report_status__mutmut_3(report_id: str, status: str, error: Optional[str] = None) -> None:
    """
    Update report status (used by streaming endpoint)
    """
    supabase = get_supabase()

    update_data = {
        "XXstatusXX": status,
        "updated_at": datetime.utcnow().isoformat(),
    }

    if error:
        update_data["error"] = error

    supabase.table("reports").update(update_data).eq("id", report_id).execute()


async def x_update_report_status__mutmut_4(report_id: str, status: str, error: Optional[str] = None) -> None:
    """
    Update report status (used by streaming endpoint)
    """
    supabase = get_supabase()

    update_data = {
        "STATUS": status,
        "updated_at": datetime.utcnow().isoformat(),
    }

    if error:
        update_data["error"] = error

    supabase.table("reports").update(update_data).eq("id", report_id).execute()


async def x_update_report_status__mutmut_5(report_id: str, status: str, error: Optional[str] = None) -> None:
    """
    Update report status (used by streaming endpoint)
    """
    supabase = get_supabase()

    update_data = {
        "status": status,
        "XXupdated_atXX": datetime.utcnow().isoformat(),
    }

    if error:
        update_data["error"] = error

    supabase.table("reports").update(update_data).eq("id", report_id).execute()


async def x_update_report_status__mutmut_6(report_id: str, status: str, error: Optional[str] = None) -> None:
    """
    Update report status (used by streaming endpoint)
    """
    supabase = get_supabase()

    update_data = {
        "status": status,
        "UPDATED_AT": datetime.utcnow().isoformat(),
    }

    if error:
        update_data["error"] = error

    supabase.table("reports").update(update_data).eq("id", report_id).execute()


async def x_update_report_status__mutmut_7(report_id: str, status: str, error: Optional[str] = None) -> None:
    """
    Update report status (used by streaming endpoint)
    """
    supabase = get_supabase()

    update_data = {
        "status": status,
        "updated_at": datetime.utcnow().isoformat(),
    }

    if error:
        update_data["error"] = None

    supabase.table("reports").update(update_data).eq("id", report_id).execute()


async def x_update_report_status__mutmut_8(report_id: str, status: str, error: Optional[str] = None) -> None:
    """
    Update report status (used by streaming endpoint)
    """
    supabase = get_supabase()

    update_data = {
        "status": status,
        "updated_at": datetime.utcnow().isoformat(),
    }

    if error:
        update_data["XXerrorXX"] = error

    supabase.table("reports").update(update_data).eq("id", report_id).execute()


async def x_update_report_status__mutmut_9(report_id: str, status: str, error: Optional[str] = None) -> None:
    """
    Update report status (used by streaming endpoint)
    """
    supabase = get_supabase()

    update_data = {
        "status": status,
        "updated_at": datetime.utcnow().isoformat(),
    }

    if error:
        update_data["ERROR"] = error

    supabase.table("reports").update(update_data).eq("id", report_id).execute()


async def x_update_report_status__mutmut_10(report_id: str, status: str, error: Optional[str] = None) -> None:
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

    supabase.table("reports").update(update_data).eq(None, report_id).execute()


async def x_update_report_status__mutmut_11(report_id: str, status: str, error: Optional[str] = None) -> None:
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

    supabase.table("reports").update(update_data).eq("id", None).execute()


async def x_update_report_status__mutmut_12(report_id: str, status: str, error: Optional[str] = None) -> None:
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

    supabase.table("reports").update(update_data).eq(report_id).execute()


async def x_update_report_status__mutmut_13(report_id: str, status: str, error: Optional[str] = None) -> None:
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

    supabase.table("reports").update(update_data).eq("id", ).execute()


async def x_update_report_status__mutmut_14(report_id: str, status: str, error: Optional[str] = None) -> None:
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

    supabase.table("reports").update(None).eq("id", report_id).execute()


async def x_update_report_status__mutmut_15(report_id: str, status: str, error: Optional[str] = None) -> None:
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

    supabase.table(None).update(update_data).eq("id", report_id).execute()


async def x_update_report_status__mutmut_16(report_id: str, status: str, error: Optional[str] = None) -> None:
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

    supabase.table("XXreportsXX").update(update_data).eq("id", report_id).execute()


async def x_update_report_status__mutmut_17(report_id: str, status: str, error: Optional[str] = None) -> None:
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

    supabase.table("REPORTS").update(update_data).eq("id", report_id).execute()


async def x_update_report_status__mutmut_18(report_id: str, status: str, error: Optional[str] = None) -> None:
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

    supabase.table("reports").update(update_data).eq("XXidXX", report_id).execute()


async def x_update_report_status__mutmut_19(report_id: str, status: str, error: Optional[str] = None) -> None:
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

    supabase.table("reports").update(update_data).eq("ID", report_id).execute()

x_update_report_status__mutmut_mutants : ClassVar[MutantDict] = {
'x_update_report_status__mutmut_1': x_update_report_status__mutmut_1, 
    'x_update_report_status__mutmut_2': x_update_report_status__mutmut_2, 
    'x_update_report_status__mutmut_3': x_update_report_status__mutmut_3, 
    'x_update_report_status__mutmut_4': x_update_report_status__mutmut_4, 
    'x_update_report_status__mutmut_5': x_update_report_status__mutmut_5, 
    'x_update_report_status__mutmut_6': x_update_report_status__mutmut_6, 
    'x_update_report_status__mutmut_7': x_update_report_status__mutmut_7, 
    'x_update_report_status__mutmut_8': x_update_report_status__mutmut_8, 
    'x_update_report_status__mutmut_9': x_update_report_status__mutmut_9, 
    'x_update_report_status__mutmut_10': x_update_report_status__mutmut_10, 
    'x_update_report_status__mutmut_11': x_update_report_status__mutmut_11, 
    'x_update_report_status__mutmut_12': x_update_report_status__mutmut_12, 
    'x_update_report_status__mutmut_13': x_update_report_status__mutmut_13, 
    'x_update_report_status__mutmut_14': x_update_report_status__mutmut_14, 
    'x_update_report_status__mutmut_15': x_update_report_status__mutmut_15, 
    'x_update_report_status__mutmut_16': x_update_report_status__mutmut_16, 
    'x_update_report_status__mutmut_17': x_update_report_status__mutmut_17, 
    'x_update_report_status__mutmut_18': x_update_report_status__mutmut_18, 
    'x_update_report_status__mutmut_19': x_update_report_status__mutmut_19
}

def update_report_status(*args, **kwargs):
    result = _mutmut_trampoline(x_update_report_status__mutmut_orig, x_update_report_status__mutmut_mutants, args, kwargs)
    return result 

update_report_status.__signature__ = _mutmut_signature(x_update_report_status__mutmut_orig)
x_update_report_status__mutmut_orig.__name__ = 'x_update_report_status'


async def x_soft_delete_report__mutmut_orig(report_id: str, user_id: str) -> bool:
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


async def x_soft_delete_report__mutmut_1(report_id: str, user_id: str) -> bool:
    """
    Soft delete a report (set deleted_at timestamp)
    """
    supabase = None

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


async def x_soft_delete_report__mutmut_2(report_id: str, user_id: str) -> bool:
    """
    Soft delete a report (set deleted_at timestamp)
    """
    supabase = get_supabase()

    result = None

    return len(result.data) > 0


async def x_soft_delete_report__mutmut_3(report_id: str, user_id: str) -> bool:
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
        .eq(None, user_id)
        .execute()
    )

    return len(result.data) > 0


async def x_soft_delete_report__mutmut_4(report_id: str, user_id: str) -> bool:
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
        .eq("user_id", None)
        .execute()
    )

    return len(result.data) > 0


async def x_soft_delete_report__mutmut_5(report_id: str, user_id: str) -> bool:
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
        .eq(user_id)
        .execute()
    )

    return len(result.data) > 0


async def x_soft_delete_report__mutmut_6(report_id: str, user_id: str) -> bool:
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
        .eq("user_id", )
        .execute()
    )

    return len(result.data) > 0


async def x_soft_delete_report__mutmut_7(report_id: str, user_id: str) -> bool:
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
        .eq(None, report_id)
        .eq("user_id", user_id)
        .execute()
    )

    return len(result.data) > 0


async def x_soft_delete_report__mutmut_8(report_id: str, user_id: str) -> bool:
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
        .eq("id", None)
        .eq("user_id", user_id)
        .execute()
    )

    return len(result.data) > 0


async def x_soft_delete_report__mutmut_9(report_id: str, user_id: str) -> bool:
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
        .eq(report_id)
        .eq("user_id", user_id)
        .execute()
    )

    return len(result.data) > 0


async def x_soft_delete_report__mutmut_10(report_id: str, user_id: str) -> bool:
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
        .eq("id", )
        .eq("user_id", user_id)
        .execute()
    )

    return len(result.data) > 0


async def x_soft_delete_report__mutmut_11(report_id: str, user_id: str) -> bool:
    """
    Soft delete a report (set deleted_at timestamp)
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .update(
            None
        )
        .eq("id", report_id)
        .eq("user_id", user_id)
        .execute()
    )

    return len(result.data) > 0


async def x_soft_delete_report__mutmut_12(report_id: str, user_id: str) -> bool:
    """
    Soft delete a report (set deleted_at timestamp)
    """
    supabase = get_supabase()

    result = (
        supabase.table(None)
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


async def x_soft_delete_report__mutmut_13(report_id: str, user_id: str) -> bool:
    """
    Soft delete a report (set deleted_at timestamp)
    """
    supabase = get_supabase()

    result = (
        supabase.table("XXreportsXX")
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


async def x_soft_delete_report__mutmut_14(report_id: str, user_id: str) -> bool:
    """
    Soft delete a report (set deleted_at timestamp)
    """
    supabase = get_supabase()

    result = (
        supabase.table("REPORTS")
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


async def x_soft_delete_report__mutmut_15(report_id: str, user_id: str) -> bool:
    """
    Soft delete a report (set deleted_at timestamp)
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .update(
            {
                "XXdeleted_atXX": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
            }
        )
        .eq("id", report_id)
        .eq("user_id", user_id)
        .execute()
    )

    return len(result.data) > 0


async def x_soft_delete_report__mutmut_16(report_id: str, user_id: str) -> bool:
    """
    Soft delete a report (set deleted_at timestamp)
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .update(
            {
                "DELETED_AT": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
            }
        )
        .eq("id", report_id)
        .eq("user_id", user_id)
        .execute()
    )

    return len(result.data) > 0


async def x_soft_delete_report__mutmut_17(report_id: str, user_id: str) -> bool:
    """
    Soft delete a report (set deleted_at timestamp)
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .update(
            {
                "deleted_at": datetime.utcnow().isoformat(),
                "XXupdated_atXX": datetime.utcnow().isoformat(),
            }
        )
        .eq("id", report_id)
        .eq("user_id", user_id)
        .execute()
    )

    return len(result.data) > 0


async def x_soft_delete_report__mutmut_18(report_id: str, user_id: str) -> bool:
    """
    Soft delete a report (set deleted_at timestamp)
    """
    supabase = get_supabase()

    result = (
        supabase.table("reports")
        .update(
            {
                "deleted_at": datetime.utcnow().isoformat(),
                "UPDATED_AT": datetime.utcnow().isoformat(),
            }
        )
        .eq("id", report_id)
        .eq("user_id", user_id)
        .execute()
    )

    return len(result.data) > 0


async def x_soft_delete_report__mutmut_19(report_id: str, user_id: str) -> bool:
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
        .eq("XXidXX", report_id)
        .eq("user_id", user_id)
        .execute()
    )

    return len(result.data) > 0


async def x_soft_delete_report__mutmut_20(report_id: str, user_id: str) -> bool:
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
        .eq("ID", report_id)
        .eq("user_id", user_id)
        .execute()
    )

    return len(result.data) > 0


async def x_soft_delete_report__mutmut_21(report_id: str, user_id: str) -> bool:
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
        .eq("XXuser_idXX", user_id)
        .execute()
    )

    return len(result.data) > 0


async def x_soft_delete_report__mutmut_22(report_id: str, user_id: str) -> bool:
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
        .eq("USER_ID", user_id)
        .execute()
    )

    return len(result.data) > 0


async def x_soft_delete_report__mutmut_23(report_id: str, user_id: str) -> bool:
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

    return len(result.data) >= 0


async def x_soft_delete_report__mutmut_24(report_id: str, user_id: str) -> bool:
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

    return len(result.data) > 1

x_soft_delete_report__mutmut_mutants : ClassVar[MutantDict] = {
'x_soft_delete_report__mutmut_1': x_soft_delete_report__mutmut_1, 
    'x_soft_delete_report__mutmut_2': x_soft_delete_report__mutmut_2, 
    'x_soft_delete_report__mutmut_3': x_soft_delete_report__mutmut_3, 
    'x_soft_delete_report__mutmut_4': x_soft_delete_report__mutmut_4, 
    'x_soft_delete_report__mutmut_5': x_soft_delete_report__mutmut_5, 
    'x_soft_delete_report__mutmut_6': x_soft_delete_report__mutmut_6, 
    'x_soft_delete_report__mutmut_7': x_soft_delete_report__mutmut_7, 
    'x_soft_delete_report__mutmut_8': x_soft_delete_report__mutmut_8, 
    'x_soft_delete_report__mutmut_9': x_soft_delete_report__mutmut_9, 
    'x_soft_delete_report__mutmut_10': x_soft_delete_report__mutmut_10, 
    'x_soft_delete_report__mutmut_11': x_soft_delete_report__mutmut_11, 
    'x_soft_delete_report__mutmut_12': x_soft_delete_report__mutmut_12, 
    'x_soft_delete_report__mutmut_13': x_soft_delete_report__mutmut_13, 
    'x_soft_delete_report__mutmut_14': x_soft_delete_report__mutmut_14, 
    'x_soft_delete_report__mutmut_15': x_soft_delete_report__mutmut_15, 
    'x_soft_delete_report__mutmut_16': x_soft_delete_report__mutmut_16, 
    'x_soft_delete_report__mutmut_17': x_soft_delete_report__mutmut_17, 
    'x_soft_delete_report__mutmut_18': x_soft_delete_report__mutmut_18, 
    'x_soft_delete_report__mutmut_19': x_soft_delete_report__mutmut_19, 
    'x_soft_delete_report__mutmut_20': x_soft_delete_report__mutmut_20, 
    'x_soft_delete_report__mutmut_21': x_soft_delete_report__mutmut_21, 
    'x_soft_delete_report__mutmut_22': x_soft_delete_report__mutmut_22, 
    'x_soft_delete_report__mutmut_23': x_soft_delete_report__mutmut_23, 
    'x_soft_delete_report__mutmut_24': x_soft_delete_report__mutmut_24
}

def soft_delete_report(*args, **kwargs):
    result = _mutmut_trampoline(x_soft_delete_report__mutmut_orig, x_soft_delete_report__mutmut_mutants, args, kwargs)
    return result 

soft_delete_report.__signature__ = _mutmut_signature(x_soft_delete_report__mutmut_orig)
x_soft_delete_report__mutmut_orig.__name__ = 'x_soft_delete_report'
