"""
Integration layer between FastAPI and existing Python debate modules.

This module imports and reuses the existing debate-ai codebase (src/) without
modification, wrapping it in an async-friendly interface for web usage.

Design decisions:
- Uses asyncio.to_thread() to wrap blocking debate generation calls
- Streams progress via asyncio.Queue for real-time SSE updates
- Maintains existing module structure and prompt engineering
- No modifications to src/ code - pure integration layer
"""

import asyncio
import sys
import os
from typing import Optional
from pathlib import Path

# Add parent directory to path to import from src/
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.ai_client import AIClient
from src.character_builder import CharacterBuilder
from src.debate_engine import DebateEngine, DebateMessage as SrcDebateMessage
from src.style_config import get_style_config, create_custom_style_config

from models import DebateMessage, DebateStatus
from services.job_manager import DebateJob, job_manager


async def run_debate_job(job: DebateJob, api_key: str) -> None:
    """
    Run a complete debate job in the background with progress streaming.

    This function orchestrates the entire debate flow:
    1. Initialize AI client
    2. Build character 1 profile (AI research)
    3. Build character 2 profile (AI research)
    4. Run debate engine with multiple rounds
    5. Stream progress and messages to the job's progress_queue

    All blocking I/O operations are wrapped in asyncio.to_thread() to prevent
    blocking the event loop.

    Args:
        job: The DebateJob containing parameters and progress queue
        api_key: Anthropic API key

    Note:
        This function updates the job status and handles errors internally.
        Clients should listen to the progress_queue via SSE for updates.
    """

    try:
        # Update status to running
        await job_manager.update_job_status(job.id, DebateStatus.RUNNING)

        # Send progress: Step 1/7 - Initialize AI Client
        await job.progress_queue.put({
            "type": "progress",
            "data": {
                "step": "1/7",
                "message": "初始化AI客户端..." if job.parameters.language == "zh" else "Initializing AI client..."
            }
        })

        # Step 1: Initialize AI Client
        ai_client = await asyncio.to_thread(
            AIClient,
            api_key=api_key
        )

        # Step 2: Build Character 1
        await job.progress_queue.put({
            "type": "progress",
            "data": {
                "step": "2/7",
                "message": f"正在研究 {job.parameters.p1} 的背景和思想..." if job.parameters.language == "zh"
                          else f"Researching {job.parameters.p1}'s background and philosophy..."
            }
        })

        character_builder = CharacterBuilder(
            ai_client=ai_client,
            language=job.parameters.language,
            use_cache=getattr(job.parameters, 'use_cache', True)  # Default: use cache
        )

        # Get style config
        if job.parameters.word_limit:
            style_config = create_custom_style_config(
                job.parameters.style,
                job.parameters.word_limit
            )
        else:
            style_config = get_style_config(job.parameters.style)

        character1 = await asyncio.to_thread(
            character_builder.build_character,
            job.parameters.p1,
            job.parameters.topic,
            style_config,
            job.parameters.language_style
        )

        # Step 3: Build Character 2
        await job.progress_queue.put({
            "type": "progress",
            "data": {
                "step": "3/7",
                "message": f"正在研究 {job.parameters.p2} 的背景和思想..." if job.parameters.language == "zh"
                          else f"Researching {job.parameters.p2}'s background and philosophy..."
            }
        })

        character2 = await asyncio.to_thread(
            character_builder.build_character,
            job.parameters.p2,
            job.parameters.topic,
            style_config,
            job.parameters.language_style
        )

        # Step 4: Create Debate Engine
        await job.progress_queue.put({
            "type": "progress",
            "data": {
                "step": "4/7",
                "message": "初始化辩论引擎..." if job.parameters.language == "zh" else "Initializing debate engine..."
            }
        })

        debate_engine = DebateEngine(
            ai_client=ai_client,
            character1=character1,
            character2=character2,
            topic=job.parameters.topic,
            language=job.parameters.language,
            rounds=job.parameters.rounds,
            style_config=style_config,
            enable_streaming=True  # Enable streaming for web UI
        )

        # Get event loop reference for thread-safe callback
        loop = asyncio.get_event_loop()

        # Set up streaming callback to forward events to SSE
        def stream_callback(event: dict):
            """
            Handle streaming events from debate engine.

            Event types:
            - partial_message: Token-by-token updates (many events per message)
            - message: Complete message (one event per message)

            IMPORTANT: This callback runs in a worker thread (via asyncio.to_thread),
            so we must use run_coroutine_threadsafe to safely schedule coroutines.
            """
            try:
                # Forward streaming event to SSE queue (thread-safe)
                asyncio.run_coroutine_threadsafe(
                    job.progress_queue.put(event),
                    loop
                )
            except Exception as e:
                print(f"Error in stream_callback: {e}")

        debate_engine.set_stream_callback(stream_callback)

        # Step 5-7: Run Debate with progress callbacks
        # We'll update progress dynamically as the debate progresses

        debate_step_counter = [5]  # Use list to allow modification in nested function

        def progress_callback(msg: str):
            """
            Callback function for debate engine to report progress.

            IMPORTANT: This runs in a separate thread (from debate_engine), so we need to
            use asyncio.run_coroutine_threadsafe to send progress updates safely.
            """
            try:
                # Determine step number (5-7)
                step = debate_step_counter[0]
                if step < 7:
                    debate_step_counter[0] += 1

                # Create progress update
                progress_data = {
                    "type": "progress",
                    "data": {
                        "step": f"{min(step, 7)}/7",
                        "message": msg
                    }
                }

                # Schedule the coroutine in the event loop (thread-safe)
                asyncio.run_coroutine_threadsafe(
                    job.progress_queue.put(progress_data),
                    loop
                )
            except Exception as e:
                print(f"Error in progress_callback: {e}")

        # Run the debate (this is blocking, so wrap in to_thread)
        # Note: With streaming enabled, messages are sent in real-time via stream_callback
        # We still need to collect them for the job's message list
        messages = await asyncio.to_thread(
            debate_engine.run_debate,
            progress_callback=progress_callback
        )

        # Store messages in job (for later retrieval)
        # Note: Messages are already streamed via SSE in real-time,
        # this is just for persistent storage
        for src_msg in messages:
            backend_msg = DebateMessage(
                speaker=src_msg.speaker,
                role=src_msg.role,
                content=src_msg.content
            )
            await job_manager.add_message(job.id, backend_msg)

        # Mark as completed
        await job_manager.update_job_status(job.id, DebateStatus.COMPLETED)

        # Send completion event
        await job.progress_queue.put({
            "type": "complete",
            "data": {
                "id": job.id
            }
        })

    except Exception as e:
        # Handle any errors
        error_msg = str(e)
        print(f"Error in debate job {job.id}: {error_msg}")

        await job_manager.update_job_status(
            job.id,
            DebateStatus.FAILED,
            error=error_msg
        )

        # Send error event
        await job.progress_queue.put({
            "type": "error",
            "data": {
                "error": error_msg
            }
        })


async def start_debate(job: DebateJob, api_key: str) -> None:
    """
    Start a debate job as a background task.

    This creates an asyncio task that runs independently, allowing the
    API endpoint to return immediately while the debate runs in the background.

    Args:
        job: The DebateJob to run
        api_key: Anthropic API key
    """
    asyncio.create_task(run_debate_job(job, api_key))
