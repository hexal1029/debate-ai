"""
输出格式化模块
提供终端美化输出和文件输出功能
"""

import os
from datetime import datetime
from typing import List
from .debate_engine import DebateMessage

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.markdown import Markdown
    from rich.text import Text
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


class DebateFormatter:
    """辩论输出格式化器"""

    def __init__(self, use_rich: bool = True):
        """
        初始化格式化器

        Args:
            use_rich: 是否使用rich库进行美化（如果可用）
        """
        self.use_rich = use_rich and RICH_AVAILABLE
        if self.use_rich:
            self.console = Console()

    def print_message(self, message: DebateMessage):
        """
        打印单条辩论消息到终端

        Args:
            message: 辩论消息对象
        """
        if self.use_rich:
            self._print_message_rich(message)
        else:
            self._print_message_plain(message)

    def _print_message_rich(self, message: DebateMessage):
        """使用rich库打印美化消息"""
        # 根据角色选择颜色
        if message.role == "moderator":
            color = "cyan"
            title_style = "bold cyan"
        elif message.role == "character1":
            color = "green"
            title_style = "bold green"
        else:  # character2
            color = "yellow"
            title_style = "bold yellow"

        # 创建标题
        title = Text(f"【{message.speaker}】", style=title_style)

        # 创建面板
        panel = Panel(
            message.content,
            title=title,
            border_style=color,
            padding=(1, 2)
        )

        self.console.print(panel)
        self.console.print()  # 空行

    def _print_message_plain(self, message: DebateMessage):
        """打印纯文本消息（无rich库时的fallback）"""
        separator = "=" * 60
        print(f"\n{separator}")
        print(f"【{message.speaker}】")
        print(separator)
        print(message.content)
        print(separator)
        print()

    def print_progress(self, progress_text: str):
        """
        打印进度信息

        Args:
            progress_text: 进度文本
        """
        if self.use_rich:
            self.console.print(f"[bold blue]{progress_text}[/bold blue]")
        else:
            print(f"\n{progress_text}")

    def save_to_file(
        self,
        messages: List[DebateMessage],
        character1_name: str,
        character2_name: str,
        topic: str,
        output_dir: str = "outputs",
        metadata: dict = None
    ) -> str:
        """
        将辩论保存为Markdown文件

        Args:
            messages: 辩论消息列表
            character1_name: 角色1名称
            character2_name: 角色2名称
            topic: 辩论话题
            output_dir: 输出目录
            metadata: 元数据（生成时间、参数配置等）

        Returns:
            保存的文件路径
        """
        # 确保输出目录存在
        os.makedirs(output_dir, exist_ok=True)

        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        # 清理文件名中的特殊字符
        safe_char1 = self._sanitize_filename(character1_name)
        safe_char2 = self._sanitize_filename(character2_name)
        safe_topic = self._sanitize_filename(topic)

        filename = f"{safe_char1}_vs_{safe_char2}_{safe_topic}_{timestamp}.md"
        filepath = os.path.join(output_dir, filename)

        # 生成Markdown内容
        md_content = self._generate_markdown(
            messages=messages,
            character1_name=character1_name,
            character2_name=character2_name,
            topic=topic,
            metadata=metadata
        )

        # 写入文件
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(md_content)

        return filepath

    def _sanitize_filename(self, text: str, max_length: int = 30) -> str:
        """
        清理文件名，移除特殊字符

        Args:
            text: 原始文本
            max_length: 最大长度

        Returns:
            安全的文件名片段
        """
        # 移除或替换特殊字符
        safe = text.replace('/', '_').replace('\\', '_').replace(':', '_')
        safe = safe.replace('?', '').replace('*', '').replace('"', '')
        safe = safe.replace('<', '').replace('>', '').replace('|', '')
        safe = safe.strip()

        # 截断过长的文本
        if len(safe) > max_length:
            safe = safe[:max_length]

        return safe

    def _generate_markdown(
        self,
        messages: List[DebateMessage],
        character1_name: str,
        character2_name: str,
        topic: str,
        metadata: dict = None
    ) -> str:
        """
        生成Markdown格式的辩论内容

        Args:
            messages: 辩论消息列表
            character1_name: 角色1名称
            character2_name: 角色2名称
            topic: 辩论话题
            metadata: 元数据

        Returns:
            Markdown格式的字符串
        """
        lines = []

        # 标题
        lines.append(f"# {character1_name} vs {character2_name}：{topic}")
        lines.append("")

        # 元信息
        lines.append("## 辩论信息")
        lines.append("")
        lines.append(f"- **辩论话题**: {topic}")
        lines.append(f"- **辩论双方**: {character1_name} vs {character2_name}")
        lines.append(f"- **生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        if metadata:
            lines.append(f"- **使用模型**: {metadata.get('model', 'N/A')}")
            lines.append(f"- **辩论轮数**: {metadata.get('rounds', 'N/A')}")
            lines.append(f"- **辩论风格**: {metadata.get('style', 'N/A')}")
            lines.append(f"- **输出语言**: {metadata.get('language', 'N/A')}")

        lines.append("")
        lines.append("---")
        lines.append("")

        # 辩论内容
        lines.append("## 辩论实录")
        lines.append("")

        for i, message in enumerate(messages, 1):
            # 根据角色设置emoji（可选）
            if message.role == "moderator":
                emoji = "🎤"
            elif message.role == "character1":
                emoji = "🔵"
            else:
                emoji = "🟡"

            # 发言者标题
            lines.append(f"### {emoji} {message.speaker}")
            lines.append("")

            # 发言内容
            lines.append(message.content)
            lines.append("")

            # 如果不是最后一条，添加分隔线
            if i < len(messages):
                lines.append("---")
                lines.append("")

        # 页脚
        lines.append("---")
        lines.append("")
        lines.append("*本辩论由 AI 历史人物辩论生成器自动生成*")
        lines.append("")

        return "\n".join(lines)
