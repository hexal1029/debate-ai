"""
动态角色构建器模块（核心模块）
负责动态研究历史人物并构建角色设定
"""

from typing import Dict, Tuple
from .ai_client import AIClient


class Character:
    """角色数据类"""

    def __init__(self, name: str, profile: str, system_prompt: str):
        """
        初始化角色

        Args:
            name: 角色名称
            profile: 角色研究结果（背景、思想、风格等）
            system_prompt: 用于AI角色扮演的system prompt
        """
        self.name = name
        self.profile = profile
        self.system_prompt = system_prompt

    def __repr__(self) -> str:
        return f"Character(name='{self.name}')"


class CharacterBuilder:
    """动态角色构建器"""

    def __init__(self, ai_client: AIClient, language: str = "zh"):
        """
        初始化角色构建器

        Args:
            ai_client: AI客户端实例
            language: 输出语言
        """
        self.ai_client = ai_client
        self.language = language

    def build_character(self, character_name: str, topic: str, style: str = "academic", language_style: str = "现代口语") -> Character:
        """
        构建单个角色（核心功能）

        这个方法完全动态化：
        1. 使用AI研究该人物的背景、思想、风格
        2. 生成详细的角色profile
        3. 将profile转化为system prompt（根据风格调整）

        Args:
            character_name: 人物名称（任意字符串）
            topic: 辩论话题
            style: 辩论风格
            language_style: 语言风格（文言/半文半白/现代口语）

        Returns:
            Character对象，包含完整的角色设定
        """
        # 第一步：AI研究该人物，生成详细的profile
        profile = self.ai_client.generate_character_profile(
            character_name=character_name,
            topic=topic,
            language=self.language
        )

        # 第二步：将profile转化为system prompt（传递风格和语言风格参数）
        system_prompt = self.ai_client.create_system_prompt(
            profile=profile,
            character_name=character_name,
            topic=topic,
            language=self.language,
            style=style,
            language_style=language_style
        )

        # 创建并返回Character对象
        return Character(
            name=character_name,
            profile=profile,
            system_prompt=system_prompt
        )

    def build_characters(
        self,
        character1_name: str,
        character2_name: str,
        topic: str
    ) -> Tuple[Character, Character]:
        """
        并行构建两个角色

        Args:
            character1_name: 角色1名称
            character2_name: 角色2名称
            topic: 辩论话题

        Returns:
            (角色1, 角色2) 的元组
        """
        # 注：实际实现中可以使用多线程并行调用以提高速度
        # 这里为了简单起见采用顺序调用
        character1 = self.build_character(character1_name, topic)
        character2 = self.build_character(character2_name, topic)

        return character1, character2

    def get_character_summary(self, character: Character, max_length: int = 200) -> str:
        """
        获取角色的简要摘要（用于主持人介绍等）

        Args:
            character: Character对象
            max_length: 最大长度（字符数）

        Returns:
            角色摘要文本
        """
        # 简单截取profile的前部分作为摘要
        # 可以进一步优化，使用AI生成专门的摘要
        summary = character.profile.strip()

        if len(summary) > max_length:
            # 截断到最后一个完整句子
            summary = summary[:max_length]
            # 找到最后一个句号或问号
            last_period = max(
                summary.rfind('。'),
                summary.rfind('.'),
                summary.rfind('!'),
                summary.rfind('！'),
                summary.rfind('?'),
                summary.rfind('？')
            )
            if last_period > max_length // 2:  # 如果句号位置合理
                summary = summary[:last_period + 1]
            else:
                summary = summary + "..."

        return summary
