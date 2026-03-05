"""
FastAPI backend for AI Historical Debate Generator.

This is the main entry point for the web API. It wraps the existing debate-ai
CLI tool with a RESTful API and SSE streaming for real-time updates.

Architecture:
- Approach A (FastAPI wrapper) - Imports and reuses existing src/ modules
- In-memory job queue for v1 (no database required)
- SSE for real-time progress streaming
- CORS enabled for Next.js frontend

To run:
    uvicorn backend.main:app --reload --port 8000

Or with environment variable:
    ANTHROPIC_API_KEY=sk-ant-xxx uvicorn backend.main:app --reload --port 8000
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import os
from dotenv import load_dotenv

from backend.routes import debates, stream, styles
from backend.services.job_manager import start_cleanup_task


# Load environment variables from .env file
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle manager for the FastAPI app.

    On startup:
    - Start background cleanup task for old jobs

    On shutdown:
    - Cleanup resources
    """
    # Startup
    import asyncio
    cleanup_task = asyncio.create_task(start_cleanup_task())

    yield

    # Shutdown
    cleanup_task.cancel()
    try:
        await cleanup_task
    except asyncio.CancelledError:
        pass


# Create FastAPI app
app = FastAPI(
    title="AI Historical Debate Generator API",
    description="REST API for generating debates between historical figures using Claude AI",
    version="1.0.0",
    lifespan=lifespan
)


# Configure CORS
# For development, allow localhost:3000 (Next.js dev server)
# For production, set CORS_ORIGINS environment variable with allowed domains
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


# Register routers
app.include_router(debates.router)
app.include_router(stream.router)
app.include_router(styles.router)


@app.get("/")
async def root():
    """
    Root endpoint with API information.

    Returns:
        API welcome message and documentation links
    """
    return {
        "message": "AI Historical Debate Generator API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "create_debate": "POST /api/debates",
            "list_debates": "GET /api/debates",
            "get_debate": "GET /api/debates/{id}",
            "stream_debate": "GET /api/debates/{id}/stream",
            "delete_debate": "DELETE /api/debates/{id}",
            "get_styles": "GET /api/styles",
            "health": "GET /health"
        }
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring and deployment.

    Returns:
        Health status and basic system information
    """
    from backend.services.job_manager import job_manager

    # Check if API key is configured
    api_key_configured = bool(os.getenv("ANTHROPIC_API_KEY"))

    # Get job stats
    stats = job_manager.get_stats()

    return {
        "status": "healthy",
        "api_key_configured": api_key_configured,
        "jobs": stats
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for uncaught errors.

    This provides a consistent error response format and prevents
    internal server errors from exposing sensitive information.
    """
    import traceback

    # Log the error
    print(f"Unhandled exception: {exc}")
    print(traceback.format_exc())

    # Return generic error to client
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if os.getenv("DEBUG") else "An unexpected error occurred"
        }
    )


if __name__ == "__main__":
    import uvicorn

    # Get port from environment or use default
    port = int(os.getenv("BACKEND_PORT", 8000))

    # Run the app
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=port,
        reload=True  # Auto-reload on code changes (development only)
    )
