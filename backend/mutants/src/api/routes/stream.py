"""
Streaming report generation endpoint
Uses Server-Sent Events (SSE) to stream AI responses per specification Section 5 & 9

Integrates with dependency injection for database, logging, and feature flags.
"""

import json
import asyncio
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
import structlog

from api.services.auth_service import get_current_user_id
from api.services.ai_service import generate_report_stream
from api.services.report_service import get_report, update_report_status
from dependencies import (
    get_db,
    get_request_logger,
)
from database.types import DatabaseAdapter

router = APIRouter(prefix="/stream", tags=["Streaming"])
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


@router.get("/reports/{report_id}")
async def stream_report_generation(
    report_id: str,
    user_id: str = Depends(get_current_user_id),
    db: DatabaseAdapter = Depends(get_db),
    logger: structlog.BoundLogger = Depends(get_request_logger),
):
    """
    Stream report generation progress using Server-Sent Events (SSE)

    Per specification Section 5 & 9: "Streaming response rendering" - Gemini-style

    Client receives SSE events:
    - data: {"type": "start", "report_id": "..."}
    - data: {"type": "section", "section_num": 1, "heading": "...", "content": "...", "citations": [...]}
    - data: {"type": "progress", "current_section": 3, "total_sections": 10}
    - data: {"type": "complete", "report_id": "..."}
    - data: {"type": "error", "message": "..."}

    Frontend uses EventSource API or Vercel AI SDK to consume stream
    """
    try:
        # Verify report exists and user has access
        report = await get_report(report_id, user_id)
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")

        # Check if report is ready to generate
        if report.status not in ["pending", "generating"]:
            raise HTTPException(
                status_code=400, detail=f"Report status is '{report.status}', cannot stream"
            )

        async def event_generator():
            """Generator function that yields SSE-formatted chunks"""
            try:
                # Update status to generating
                await update_report_status(report_id, "generating")

                # Send start event
                yield f"data: {json.dumps({'type': 'start', 'report_id': report_id})}\n\n"

                # Stream report generation
                section_count = 0
                async for chunk in generate_report_stream(report_id, report.query):
                    chunk_data = json.loads(chunk)

                    if chunk_data.get("type") == "section":
                        section_count += 1
                        # Send progress update
                        yield f"data: {json.dumps({'type': 'progress', 'current_section': section_count, 'total_sections': 10})}\n\n"

                    # Forward chunk to client
                    yield f"data: {chunk}\n\n"

                    # Allow other tasks to run
                    await asyncio.sleep(0)

                # Send completion event
                yield f"data: {json.dumps({'type': 'complete', 'report_id': report_id})}\n\n"

            except Exception as e:
                logger.error("stream_error", report_id=report_id, error=str(e))
                error_msg = json.dumps({"type": "error", "message": str(e)})
                yield f"data: {error_msg}\n\n"

                # Update report status to failed
                await update_report_status(report_id, "failed", error=str(e))

        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no",  # Disable nginx buffering for SSE
                "Access-Control-Allow-Origin": "*",  # Will be restricted by CORS middleware
            },
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("stream_setup_error", report_id=report_id, error=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to setup streaming: {str(e)}")
