"""
FastAPI routes for Server-Sent Events (SSE) streaming.

Provides real-time progress updates for debate generation via SSE.
Clients connect to the stream endpoint and receive events as they occur.

Event types:
- progress: Progress updates with step number and message
- message: New debate messages as they're generated
- complete: Debate completed successfully
- error: Error occurred during debate generation
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse
import asyncio
import json

from services.job_manager import job_manager


router = APIRouter(prefix="/api/debates", tags=["streaming"])


async def event_generator(debate_id: str):
    """
    Async generator that yields SSE events from a debate job's progress queue.

    This function:
    1. Retrieves the debate job
    2. Continuously polls the progress_queue
    3. Yields events in SSE format
    4. Closes when receiving a 'complete' or 'error' event

    Args:
        debate_id: The debate job ID

    Yields:
        dict: SSE events with 'event' and 'data' keys

    The event format follows SSE standard:
    {
        "event": "progress" | "message" | "complete" | "error",
        "data": <event-specific data>
    }
    """

    # Get the job
    job = await job_manager.get_job(debate_id)

    if not job:
        # Send error event and close
        yield {
            "event": "error",
            "data": json.dumps({"error": f"Debate {debate_id} not found"})
        }
        return

    # Send initial connection event
    yield {
        "event": "connected",
        "data": json.dumps({
            "id": job.id,
            "status": job.status.value
        })
    }

    # Stream events from the progress queue
    try:
        while True:
            # Wait for next event from the queue (with timeout)
            try:
                event_data = await asyncio.wait_for(
                    job.progress_queue.get(),
                    timeout=0.5  # Check every 500ms
                )

                # Extract event type and data
                event_type = event_data.get("type", "unknown")
                event_payload = event_data.get("data", {})

                # Yield the event
                yield {
                    "event": event_type,
                    "data": json.dumps(event_payload)
                }

                # If this is a complete or error event, close the stream
                if event_type in ["complete", "error"]:
                    break

            except asyncio.TimeoutError:
                # No event received, send keepalive ping
                yield {
                    "event": "ping",
                    "data": json.dumps({"timestamp": asyncio.get_event_loop().time()})
                }

    except asyncio.CancelledError:
        # Client disconnected
        print(f"Client disconnected from debate {debate_id}")
    except Exception as e:
        # Unexpected error
        print(f"Error in event stream for debate {debate_id}: {e}")
        yield {
            "event": "error",
            "data": json.dumps({"error": str(e)})
        }


@router.get("/{debate_id}/stream")
async def stream_debate(debate_id: str):
    """
    SSE endpoint for streaming debate progress and messages.

    Clients should connect to this endpoint immediately after creating a debate
    to receive real-time updates.

    Connection lifecycle:
    1. Client connects
    2. Server sends 'connected' event
    3. Server streams 'progress' and 'message' events as debate proceeds
    4. Server sends 'complete' or 'error' event
    5. Connection closes

    Args:
        debate_id: The debate job ID

    Returns:
        EventSourceResponse: SSE stream

    Example client code (JavaScript):
        const eventSource = new EventSource('/api/debates/deb_123/stream');

        eventSource.addEventListener('progress', (e) => {
            const data = JSON.parse(e.data);
            console.log(`${data.step}: ${data.message}`);
        });

        eventSource.addEventListener('message', (e) => {
            const data = JSON.parse(e.data);
            console.log(`${data.speaker}: ${data.content}`);
        });

        eventSource.addEventListener('complete', (e) => {
            console.log('Debate completed!');
            eventSource.close();
        });

        eventSource.addEventListener('error', (e) => {
            const data = JSON.parse(e.data);
            console.error('Error:', data.error);
            eventSource.close();
        });
    """

    # Verify debate exists before starting stream
    job = await job_manager.get_job(debate_id)
    if not job:
        raise HTTPException(
            status_code=404,
            detail=f"Debate {debate_id} not found"
        )

    # Return SSE stream
    return EventSourceResponse(
        event_generator(debate_id),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Disable nginx buffering
        }
    )
