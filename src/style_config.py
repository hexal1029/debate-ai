"""
风格配置模块
管理不同辩论风格的参数配置
"""

from dataclasses import dataclass
from typing import Dict


@dataclass
class StyleConfig:
    """辩论风格配置"""
    name: str                    # 风格名称
    max_tokens: int             # 最大token数
    temperature: float          # 温度参数
    default_rounds: int         # 建议的默认轮数
    word_limit: str            # 字数限制（用于prompt）
    tone_description: str      # 语气描述
    is_collaborative: bool     # 是否是合作模式（非对抗）


# 所有支持的风格配置
STYLE_CONFIGS: Dict[str, StyleConfig] = {
    "academic": StyleConfig(
        name="学术风格",
        max_tokens=1500,
        temperature=0.8,
        default_rounds=5,
        word_limit="250-400字",
        tone_description="严谨、学术化、论证充分",
        is_collaborative=False
    ),
    "casual-chat": StyleConfig(
        name="轻松对话",
        max_tokens=200,
        temperature=0.9,
        default_rounds=10,
        word_limit="30-50字（1-2句话）",
        tone_description="轻松、口语化、简洁明快",
        is_collaborative=False
    ),
    "heated-debate": StyleConfig(
        name="激烈争论",
        max_tokens=250,
        temperature=1.0,
        default_rounds=8,
        word_limit="40-60字（2-3句话）",
        tone_description="激烈、犀利、针锋相对",
        is_collaborative=False
    ),
    "comedy-duo": StyleConfig(
        name="捧哏",
        max_tokens=200,
        temperature=0.95,
        default_rounds=12,
        word_limit="30-50字（1-2句话）",
        tone_description="幽默、配合、娱乐性强",
        is_collaborative=True  # 关键：合作模式
    )
}


def get_style_config(style: str) -> StyleConfig:
    """
    获取风格配置

    Args:
        style: 风格名称

    Returns:
        StyleConfig对象，如果不存在则返回默认的academic风格
    """
    return STYLE_CONFIGS.get(style, STYLE_CONFIGS["academic"])


def create_custom_style_config(style: str, word_limit: int) -> StyleConfig:
    """
    创建自定义字数限制的风格配置

    Args:
        style: 基础风格名称
        word_limit: 自定义字数限制

    Returns:
        调整后的StyleConfig对象
    """
    # 获取基础配置
    base_config = get_style_config(style)

    # 根据字数估算 max_tokens
    # 中文：1个字约等于1.5-2个tokens
    # 英文：1个词约等于1.3个tokens
    # 为了安全起见，使用 word_limit * 2.5
    estimated_max_tokens = int(word_limit * 2.5)

    # 设置最小值和最大值
    max_tokens = max(100, min(estimated_max_tokens, 4000))

    # 创建新的配置（复制基础配置，只修改相关字段）
    from dataclasses import replace
    return replace(
        base_config,
        max_tokens=max_tokens,
        word_limit=f"{word_limit}字左右"
    )
