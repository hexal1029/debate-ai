"""
FastAPI routes for debate style information.

Provides metadata about available debate styles to help the frontend
build the style selector UI with descriptions and recommendations.
"""

from fastapi import APIRouter
import sys
from pathlib import Path

# Add parent directory to path to import from src/
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.style_config import STYLE_CONFIGS

from backend.models import StylesResponse, StyleInfo


router = APIRouter(prefix="/api/styles", tags=["styles"])


STYLE_DESCRIPTIONS = {
    "academic": {
        "zh": "学术风格 - 严谨、深入、论证充分",
        "en": "Academic style - rigorous, in-depth, well-reasoned"
    },
    "casual-chat": {
        "zh": "轻松对话 - 口语化、简洁、快速来回",
        "en": "Casual chat - conversational, concise, quick exchanges"
    },
    "heated-debate": {
        "zh": "激烈争论 - 犀利、直接、针锋相对",
        "en": "Heated debate - sharp, direct, confrontational"
    },
    "comedy-duo": {
        "zh": "双簧相声 - 幽默、配合、娱乐性强 (非对抗模式)",
        "en": "Comedy duo - humorous, collaborative, entertaining (non-adversarial)"
    }
}


@router.get("", response_model=StylesResponse)
async def get_styles(language: str = "zh"):
    """
    Get information about all available debate styles.

    This endpoint provides the frontend with style metadata including:
    - Display name
    - Description
    - Model parameters (max_tokens, temperature)
    - Recommended rounds
    - Word limit guidance
    - Whether it's collaborative vs adversarial

    Args:
        language: Language for descriptions ('zh' or 'en', default: 'zh')

    Returns:
        StylesResponse with list of all styles
    """

    styles = []

    for style_name, config in STYLE_CONFIGS.items():
        # Get description in requested language
        desc = STYLE_DESCRIPTIONS[style_name].get(language, STYLE_DESCRIPTIONS[style_name]["zh"])

        style_info = StyleInfo(
            name=style_name,
            description=desc,
            max_tokens=config.max_tokens,
            temperature=config.temperature,
            default_rounds=config.default_rounds,
            word_limit=config.word_limit,
            is_collaborative=config.is_collaborative
        )
        styles.append(style_info)

    return StylesResponse(styles=styles)


@router.get("/{style_name}", response_model=StyleInfo)
async def get_style(style_name: str, language: str = "zh"):
    """
    Get information about a specific debate style.

    Args:
        style_name: Name of the style (academic/casual-chat/heated-debate/comedy-duo)
        language: Language for description ('zh' or 'en', default: 'zh')

    Returns:
        StyleInfo for the requested style

    Raises:
        HTTPException 404: If style not found
    """
    from fastapi import HTTPException

    if style_name not in STYLE_CONFIGS:
        raise HTTPException(
            status_code=404,
            detail=f"Style '{style_name}' not found. Available styles: {list(STYLE_CONFIGS.keys())}"
        )

    config = STYLE_CONFIGS[style_name]
    desc = STYLE_DESCRIPTIONS[style_name].get(language, STYLE_DESCRIPTIONS[style_name]["zh"])

    return StyleInfo(
        name=style_name,
        description=desc,
        max_tokens=config.max_tokens,
        temperature=config.temperature,
        default_rounds=config.default_rounds,
        word_limit=config.word_limit,
        is_collaborative=config.is_collaborative
    )
