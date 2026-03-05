"""
In-memory job queue and state management for debate jobs.

This module manages the lifecycle of debate jobs, including creation, tracking,
and cleanup. For v1, we use in-memory storage (debates lost on restart), which
is simple and sufficient for development/testing.

Future: Can be easily replaced with Redis or database persistence.
"""

import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from dataclasses import dataclass, field
import time

from backend.models import DebateStatus, CreateDebateRequest, DebateMessage


@dataclass
class DebateJob:
    """
    Represents a single debate job with all its state and progress tracking.

    Attributes:
        id: Unique identifier for the debate
        status: Current status (pending/running/completed/failed)
        parameters: Original request parameters
        messages: List of generated debate messages
        progress_queue: Async queue for streaming progress updates via SSE
        created_at: Timestamp when job was created
        completed_at: Timestamp when job completed (if applicable)
        error: Error message if job failed
    """
    id: str
    status: DebateStatus
    parameters: CreateDebateRequest
    messages: List[DebateMessage] = field(default_factory=list)
    progress_queue: asyncio.Queue = field(default_factory=asyncio.Queue)
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    error: Optional[str] = None


class JobManager:
    """
    Manages all debate jobs with in-memory storage and concurrent execution limits.

    Design decisions:
    - In-memory storage: Simple for v1, no database setup required
    - Max concurrent debates: Prevents API rate limit issues
    - Auto-cleanup: Removes old jobs to prevent memory leaks
    """

    def __init__(self, max_concurrent_debates: int = 3, cleanup_hours: int = 24):
        """
        Initialize the job manager.

        Args:
            max_concurrent_debates: Maximum number of debates running simultaneously
            cleanup_hours: Hours to keep completed debates before cleanup
        """
        self.jobs: Dict[str, DebateJob] = {}
        self.max_concurrent_debates = max_concurrent_debates
        self.cleanup_hours = cleanup_hours
        self._lock = asyncio.Lock()

    def _generate_id(self) -> str:
        """Generate a unique debate ID using timestamp"""
        return f"deb_{int(time.time() * 1000)}"

    async def create_job(self, parameters: CreateDebateRequest) -> DebateJob:
        """
        Create a new debate job.

        Args:
            parameters: Debate parameters from the request

        Returns:
            The created DebateJob
        """
        async with self._lock:
            job_id = self._generate_id()
            job = DebateJob(
                id=job_id,
                status=DebateStatus.PENDING,
                parameters=parameters
            )
            self.jobs[job_id] = job
            return job

    async def get_job(self, job_id: str) -> Optional[DebateJob]:
        """
        Retrieve a job by ID.

        Args:
            job_id: The debate job ID

        Returns:
            The DebateJob if found, None otherwise
        """
        return self.jobs.get(job_id)

    async def list_jobs(
        self,
        page: int = 1,
        page_size: int = 20,
        status: Optional[DebateStatus] = None
    ) -> tuple[List[DebateJob], int]:
        """
        List all jobs with pagination and optional status filtering.

        Args:
            page: Page number (1-indexed)
            page_size: Number of items per page
            status: Optional status filter

        Returns:
            Tuple of (jobs list, total count)
        """
        # Filter by status if provided
        all_jobs = list(self.jobs.values())
        if status:
            all_jobs = [job for job in all_jobs if job.status == status]

        # Sort by created_at (newest first)
        all_jobs.sort(key=lambda j: j.created_at, reverse=True)

        # Paginate
        total = len(all_jobs)
        start = (page - 1) * page_size
        end = start + page_size
        paginated_jobs = all_jobs[start:end]

        return paginated_jobs, total

    async def delete_job(self, job_id: str) -> bool:
        """
        Delete a job by ID.

        Args:
            job_id: The debate job ID

        Returns:
            True if job was deleted, False if not found
        """
        async with self._lock:
            if job_id in self.jobs:
                del self.jobs[job_id]
                return True
            return False

    async def update_job_status(
        self,
        job_id: str,
        status: DebateStatus,
        error: Optional[str] = None
    ) -> None:
        """
        Update the status of a job.

        Args:
            job_id: The debate job ID
            status: New status
            error: Optional error message (for failed status)
        """
        job = await self.get_job(job_id)
        if job:
            job.status = status
            if status in [DebateStatus.COMPLETED, DebateStatus.FAILED]:
                job.completed_at = datetime.now()
            if error:
                job.error = error

    async def add_message(self, job_id: str, message: DebateMessage) -> None:
        """
        Add a message to a job's message list.

        Args:
            job_id: The debate job ID
            message: The debate message to add
        """
        job = await self.get_job(job_id)
        if job:
            job.messages.append(message)

    def count_running_jobs(self) -> int:
        """
        Count the number of currently running jobs.

        Returns:
            Number of jobs with RUNNING status
        """
        return sum(1 for job in self.jobs.values() if job.status == DebateStatus.RUNNING)

    def can_start_new_debate(self) -> bool:
        """
        Check if a new debate can be started based on concurrent limit.

        Returns:
            True if a new debate can start, False otherwise
        """
        return self.count_running_jobs() < self.max_concurrent_debates

    async def cleanup_old_jobs(self) -> int:
        """
        Remove completed/failed jobs older than cleanup_hours.

        This prevents memory leaks in long-running servers. Should be called
        periodically (e.g., via background task).

        Returns:
            Number of jobs cleaned up
        """
        cutoff_time = datetime.now() - timedelta(hours=self.cleanup_hours)

        async with self._lock:
            jobs_to_delete = [
                job_id
                for job_id, job in self.jobs.items()
                if job.status in [DebateStatus.COMPLETED, DebateStatus.FAILED]
                and job.completed_at
                and job.completed_at < cutoff_time
            ]

            for job_id in jobs_to_delete:
                del self.jobs[job_id]

            return len(jobs_to_delete)

    def get_stats(self) -> dict:
        """
        Get statistics about current jobs.

        Returns:
            Dictionary with job statistics
        """
        total = len(self.jobs)
        pending = sum(1 for job in self.jobs.values() if job.status == DebateStatus.PENDING)
        running = sum(1 for job in self.jobs.values() if job.status == DebateStatus.RUNNING)
        completed = sum(1 for job in self.jobs.values() if job.status == DebateStatus.COMPLETED)
        failed = sum(1 for job in self.jobs.values() if job.status == DebateStatus.FAILED)

        return {
            "total": total,
            "pending": pending,
            "running": running,
            "completed": completed,
            "failed": failed,
            "max_concurrent": self.max_concurrent_debates
        }


# Global job manager instance
job_manager = JobManager()


async def start_cleanup_task():
    """
    Background task to periodically cleanup old jobs.

    Runs every hour and removes jobs older than 24 hours.
    """
    while True:
        await asyncio.sleep(3600)  # Run every hour
        cleaned = await job_manager.cleanup_old_jobs()
        if cleaned > 0:
            print(f"Cleaned up {cleaned} old debate jobs")
