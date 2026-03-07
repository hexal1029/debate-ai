"""
Pydantic models for request/response validation in the FastAPI backend.

These models define the structure of data exchanged between the frontend and backend,
ensuring type safety and automatic validation.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime
from enum import Enum


class DebateStatus(str, Enum):
    """Enum for debate job status"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class CreateDebateRequest(BaseModel):
    """Request model for creating a new debate"""
    p1: str = Field(..., min_length=1, max_length=100, description="First debater name")
    p2: str = Field(..., min_length=1, max_length=100, description="Second debater name")
    topic: str = Field(..., min_length=1, max_length=200, description="Debate topic")
    rounds: int = Field(default=5, ge=1, le=20, description="Number of debate rounds")
    style: Literal["academic", "casual-chat", "heated-debate", "comedy-duo"] = Field(
        default="academic",
        description="Debate style"
    )
    language: Literal["zh", "en"] = Field(default="zh", description="Output language")
    word_limit: Optional[int] = Field(
        default=None,
        ge=20,
        le=500,
        description="Optional word limit per response"
    )
    language_style: Literal["文言", "半文半白", "现代口语"] = Field(
        default="现代口语",
        description="Language style for Chinese output"
    )
    use_cache: bool = Field(
        default=True,
        description="Enable character profile caching (speeds up generation)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "p1": "牛顿",
                "p2": "莱布尼茨",
                "topic": "微积分的发明权",
                "rounds": 5,
                "style": "academic",
                "language": "zh",
                "word_limit": None,
                "language_style": "现代口语"
            }
        }


class CreateDebateResponse(BaseModel):
    """Response model after creating a debate"""
    id: str = Field(..., description="Unique debate ID")
    status: DebateStatus = Field(..., description="Current status of the debate")
    created_at: datetime = Field(..., description="Timestamp when debate was created")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "deb_1709876543",
                "status": "pending",
                "created_at": "2026-03-05T10:30:00Z"
            }
        }


class DebateMessage(BaseModel):
    """Model for individual debate messages"""
    speaker: str = Field(..., description="Name of the speaker")
    role: Literal["moderator", "character1", "character2", "both"] = Field(
        ...,
        description="Role of the speaker"
    )
    content: str = Field(..., description="Message content")

    class Config:
        json_schema_extra = {
            "example": {
                "speaker": "主持人",
                "role": "moderator",
                "content": "欢迎来到今天的辩论..."
            }
        }


class DebateSummary(BaseModel):
    """Summary model for debate list view"""
    id: str
    status: DebateStatus
    parameters: CreateDebateRequest
    message_count: int = Field(default=0, description="Number of messages generated")
    created_at: datetime
    completed_at: Optional[datetime] = None


class DebateDetail(BaseModel):
    """Detailed model for single debate view"""
    id: str
    status: DebateStatus
    parameters: CreateDebateRequest
    messages: List[DebateMessage] = Field(default_factory=list)
    created_at: datetime
    completed_at: Optional[datetime] = None
    error: Optional[str] = None


class DebateListResponse(BaseModel):
    """Response model for listing debates"""
    debates: List[DebateSummary]
    total: int = Field(..., description="Total number of debates")
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)


class ProgressEvent(BaseModel):
    """Model for SSE progress events"""
    step: str = Field(..., description="Current step (e.g., '2/7')")
    message: str = Field(..., description="Progress message")


class MessageEvent(BaseModel):
    """Model for SSE message events"""
    speaker: str
    role: str
    content: str


class CompleteEvent(BaseModel):
    """Model for SSE complete events"""
    id: str


class ErrorEvent(BaseModel):
    """Model for SSE error events"""
    error: str


class StyleInfo(BaseModel):
    """Model for debate style information"""
    name: str
    description: str
    max_tokens: int
    temperature: float
    default_rounds: int
    word_limit: str
    is_collaborative: bool

    class Config:
        json_schema_extra = {
            "example": {
                "name": "academic",
                "description": "学术风格 - 严谨、深入、论证充分",
                "max_tokens": 1500,
                "temperature": 0.8,
                "default_rounds": 5,
                "word_limit": "250-400字",
                "is_collaborative": False
            }
        }


class StylesResponse(BaseModel):
    """Response model for listing available styles"""
    styles: List[StyleInfo]
