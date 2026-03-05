"""
FastAPI routes for debate CRUD operations.

Endpoints:
- POST /api/debates - Create a new debate
- GET /api/debates - List all debates (with pagination)
- GET /api/debates/{id} - Get single debate details
- DELETE /api/debates/{id} - Delete a debate
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional
import os

from backend.models import (
    CreateDebateRequest,
    CreateDebateResponse,
    DebateListResponse,
    DebateDetail,
    DebateSummary,
    DebateStatus
)
from backend.services.job_manager import job_manager
from backend.services.debate_service import start_debate


router = APIRouter(prefix="/api/debates", tags=["debates"])


def get_api_key() -> str:
    """
    Get Anthropic API key from environment.

    Raises:
        HTTPException: If API key is not configured
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="ANTHROPIC_API_KEY not configured in environment"
        )
    return api_key


@router.post("", response_model=CreateDebateResponse)
async def create_debate(
    request: CreateDebateRequest,
    api_key: str = Depends(get_api_key)
):
    """
    Create a new debate job.

    The debate runs asynchronously in the background. Use the returned ID
    to connect to the SSE stream endpoint for real-time updates.

    Returns:
        CreateDebateResponse with debate ID and initial status
    """

    # Check if we can start a new debate (concurrent limit)
    if not job_manager.can_start_new_debate():
        raise HTTPException(
            status_code=429,
            detail=f"Maximum concurrent debates ({job_manager.max_concurrent_debates}) reached. Please wait for a debate to complete."
        )

    # Create the job
    job = await job_manager.create_job(request)

    # Start the debate in the background
    await start_debate(job, api_key)

    return CreateDebateResponse(
        id=job.id,
        status=job.status,
        created_at=job.created_at
    )


@router.get("", response_model=DebateListResponse)
async def list_debates(
    page: int = Query(default=1, ge=1, description="Page number"),
    page_size: int = Query(default=20, ge=1, le=100, description="Items per page"),
    status: Optional[DebateStatus] = Query(default=None, description="Filter by status")
):
    """
    List all debates with pagination and optional status filtering.

    Args:
        page: Page number (1-indexed)
        page_size: Number of items per page (max 100)
        status: Optional status filter (pending/running/completed/failed)

    Returns:
        DebateListResponse with paginated list of debates
    """
    jobs, total = await job_manager.list_jobs(
        page=page,
        page_size=page_size,
        status=status
    )

    # Convert to summary format
    debates = [
        DebateSummary(
            id=job.id,
            status=job.status,
            parameters=job.parameters,
            message_count=len(job.messages),
            created_at=job.created_at,
            completed_at=job.completed_at
        )
        for job in jobs
    ]

    return DebateListResponse(
        debates=debates,
        total=total,
        page=page,
        page_size=page_size
    )


@router.get("/{debate_id}", response_model=DebateDetail)
async def get_debate(debate_id: str):
    """
    Get detailed information about a specific debate.

    Args:
        debate_id: The debate ID

    Returns:
        DebateDetail with full debate information including all messages

    Raises:
        HTTPException 404: If debate not found
    """
    job = await job_manager.get_job(debate_id)

    if not job:
        raise HTTPException(
            status_code=404,
            detail=f"Debate {debate_id} not found"
        )

    return DebateDetail(
        id=job.id,
        status=job.status,
        parameters=job.parameters,
        messages=job.messages,
        created_at=job.created_at,
        completed_at=job.completed_at,
        error=job.error
    )


@router.delete("/{debate_id}")
async def delete_debate(debate_id: str):
    """
    Delete a debate.

    Args:
        debate_id: The debate ID

    Returns:
        Success message

    Raises:
        HTTPException 404: If debate not found
    """
    deleted = await job_manager.delete_job(debate_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Debate {debate_id} not found"
        )

    return {"message": f"Debate {debate_id} deleted successfully"}


@router.get("/_stats")
async def get_stats():
    """
    Get statistics about current debates.

    This is an admin/debug endpoint that returns counts of debates by status.

    Returns:
        Dictionary with debate statistics
    """
    return job_manager.get_stats()
