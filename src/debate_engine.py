"""
辩论引擎模块
控制辩论流程、管理对话上下文
"""

from typing import List, Dict, Tuple, Callable, Optional
from .ai_client import AIClient
from .character_builder import Character
from .prompter import Prompter


class DebateMessage:
    """辩论消息数据类"""

    def __init__(self, speaker: str, role: str, content: str):
        """
        初始化辩论消息

        Args:
            speaker: 发言者名称
            role: 角色类型（"moderator", "character1", "character2"）
            content: 消息内容
        """
        self.speaker = speaker
        self.role = role
        self.content = content

    def __repr__(self) -> str:
        return f"DebateMessage(speaker='{self.speaker}', role='{self.role}')"


class DebateEngine:
    """辩论引擎"""

    def __init__(
        self,
        ai_client: AIClient,
        character1: Character,
        character2: Character,
        topic: str,
        language: str = "zh",
        rounds: int = 5,
        style: str = "academic",
        style_config = None,
        enable_streaming: bool = False
    ):
        """
        初始化辩论引擎

        Args:
            ai_client: AI客户端
            character1: 角色1
            character2: 角色2
            topic: 辩论话题
            language: 输出语言
            rounds: 辩论轮数
            style: 辩论风格
            style_config: 可选的自定义风格配置（如果提供，优先使用）
            enable_streaming: 是否启用流式输出（默认: False）
        """
        self.ai_client = ai_client
        self.character1 = character1
        self.character2 = character2
        self.topic = topic
        self.language = language
        self.rounds = rounds
        self.style = style
        self.enable_streaming = enable_streaming

        # 如果提供了自定义配置，使用它；否则根据 style 获取默认配置
        if style_config:
            self.style_config = style_config
        else:
            from .style_config import get_style_config
            self.style_config = get_style_config(style)

        self.prompter = Prompter(language=language, style=style, style_config=self.style_config)

        # 辩论历史记录
        self.messages: List[DebateMessage] = []

        # 为两个角色维护各自的对话历史
        self.character1_context: List[Dict[str, str]] = []
        self.character2_context: List[Dict[str, str]] = []

        # Streaming callback (set by set_stream_callback)
        self._stream_callback: Optional[Callable] = None

    def set_stream_callback(self, callback: Callable):
        """
        设置流式输出回调函数

        Args:
            callback: 回调函数，接收事件字典作为参数
                     事件格式: {
                         "type": "partial_message" | "message",
                         "data": {
                             "speaker": str,
                             "role": str,
                             "content": str,
                             "is_complete": bool
                         }
                     }
        """
        self._stream_callback = callback

    def run_debate(self, progress_callback: Optional[Callable[[str], None]] = None) -> List[DebateMessage]:
        """
        运行完整辩论/表演流程

        Args:
            progress_callback: 进度回调函数，用于显示进度

        Returns:
            完整的辩论/表演消息列表
        """
        # 根据风格选择流程
        if self.style_config.is_collaborative:
            return self._run_collaborative_performance(progress_callback)
        else:
            return self._run_standard_debate(progress_callback)

    def _run_standard_debate(self, progress_callback: Optional[Callable[[str], None]] = None) -> List[DebateMessage]:
        """
        运行标准辩论流程（对抗模式）

        Args:
            progress_callback: 进度回调函数，用于显示进度

        Returns:
            完整的辩论消息列表
        """
        total_steps = 2 + 2 + self.rounds * 2 + 2 + 1  # 研究2人+开场2人+辩论轮次*2+总结2人+主持人总结

        current_step = 3  # 前面已经完成了角色研究（步骤1-2）

        # 1. 主持人开场白
        if progress_callback:
            progress_callback(f"[{current_step}/{total_steps}] 生成主持人开场白...")
        current_step += 1

        moderator_opening = self._generate_moderator_opening()
        self.messages.append(DebateMessage("主持人" if self.language == "zh" else "Moderator", "moderator", moderator_opening))

        # 2. 角色1开场陈述
        if progress_callback:
            progress_callback(f"[{current_step}/{total_steps}] {self.character1.name} 开场陈述...")
        current_step += 1

        char1_opening = self._generate_character_speech(
            character=self.character1,
            prompt_content=self.prompter.get_opening_statement_prompt(is_first=True, opponent_name=self.character2.name),
            is_character1=True
        )
        self.messages.append(DebateMessage(self.character1.name, "character1", char1_opening))

        # 3. 角色2开场陈述
        if progress_callback:
            progress_callback(f"[{current_step}/{total_steps}] {self.character2.name} 开场陈述...")
        current_step += 1

        char2_opening = self._generate_character_speech(
            character=self.character2,
            prompt_content=self.prompter.get_opening_statement_prompt(is_first=False, opponent_name=self.character1.name),
            is_character1=False
        )
        self.messages.append(DebateMessage(self.character2.name, "character2", char2_opening))

        # 4. 多轮辩论交锋
        for round_num in range(1, self.rounds + 1):
            # 角色1发言
            if progress_callback:
                progress_callback(f"[{current_step}/{total_steps}] 第{round_num}轮 - {self.character1.name} 发言...")
            current_step += 1

            char1_rebuttal = self._generate_character_speech(
                character=self.character1,
                prompt_content=self.prompter.get_rebuttal_prompt(
                    round_num=round_num,
                    total_rounds=self.rounds,
                    opponent_last_statement=self.messages[-1].content
                ),
                is_character1=True
            )
            self.messages.append(DebateMessage(self.character1.name, "character1", char1_rebuttal))

            # 角色2发言
            if progress_callback:
                progress_callback(f"[{current_step}/{total_steps}] 第{round_num}轮 - {self.character2.name} 发言...")
            current_step += 1

            char2_rebuttal = self._generate_character_speech(
                character=self.character2,
                prompt_content=self.prompter.get_rebuttal_prompt(
                    round_num=round_num,
                    total_rounds=self.rounds,
                    opponent_last_statement=self.messages[-1].content
                ),
                is_character1=False
            )
            self.messages.append(DebateMessage(self.character2.name, "character2", char2_rebuttal))

        # 5. 角色1总结陈词
        if progress_callback:
            progress_callback(f"[{current_step}/{total_steps}] {self.character1.name} 总结陈词...")
        current_step += 1

        char1_closing = self._generate_character_speech(
            character=self.character1,
            prompt_content=self.prompter.get_closing_statement_prompt(
                debate_history=self._get_debate_history_text()
            ),
            is_character1=True
        )
        self.messages.append(DebateMessage(self.character1.name, "character1", char1_closing))

        # 6. 角色2总结陈词
        if progress_callback:
            progress_callback(f"[{current_step}/{total_steps}] {self.character2.name} 总结陈词...")
        current_step += 1

        char2_closing = self._generate_character_speech(
            character=self.character2,
            prompt_content=self.prompter.get_closing_statement_prompt(
                debate_history=self._get_debate_history_text()
            ),
            is_character1=False
        )
        self.messages.append(DebateMessage(self.character2.name, "character2", char2_closing))

        # 7. 主持人总结点评
        if progress_callback:
            progress_callback(f"[{current_step}/{total_steps}] 生成主持人总结点评...")

        moderator_closing = self._generate_moderator_closing()
        self.messages.append(DebateMessage("主持人" if self.language == "zh" else "Moderator", "moderator", moderator_closing))

        return self.messages

    def _generate_moderator_opening(self) -> str:
        """生成主持人开场白（支持流式输出）"""
        prompt = self.prompter.get_moderator_opening(
            character1_name=self.character1.name,
            character2_name=self.character2.name,
            topic=self.topic,
            profile1=self.character1.profile,
            profile2=self.character2.profile
        )

        messages = [{"role": "user", "content": prompt}]
        # 主持人使用稍高的 max_tokens
        moderator_tokens = max(self.style_config.max_tokens * 2, 800)

        # Use streaming if enabled
        if self.enable_streaming and self._stream_callback:
            partial_content = [""]

            def on_token(token: str):
                partial_content[0] += token
                try:
                    self._stream_callback({
                        "type": "partial_message",
                        "data": {
                            "speaker": "主持人" if self.language == "zh" else "Moderator",
                            "role": "moderator",
                            "content": partial_content[0],
                            "is_complete": False
                        }
                    })
                except:
                    pass

            response = self.ai_client.generate_text_stream(
                messages, max_tokens=moderator_tokens, temperature=0.8, on_token=on_token
            )

            # Emit complete event
            try:
                self._stream_callback({
                    "type": "message",
                    "data": {
                        "speaker": "主持人" if self.language == "zh" else "Moderator",
                        "role": "moderator",
                        "content": response,
                        "is_complete": True
                    }
                })
            except:
                pass

            return response
        else:
            return self.ai_client.generate_text(messages, max_tokens=moderator_tokens, temperature=0.8)

    def _generate_moderator_closing(self) -> str:
        """生成主持人总结点评（支持流式输出）"""
        # 获取辩论摘要（最近的几轮对话）
        recent_messages = self.messages[-10:] if len(self.messages) > 10 else self.messages
        debate_summary = "\n\n".join([
            f"{msg.speaker}: {msg.content[:200]}..."
            for msg in recent_messages
        ])

        prompt = self.prompter.get_moderator_closing(
            character1_name=self.character1.name,
            character2_name=self.character2.name,
            topic=self.topic,
            debate_summary=debate_summary
        )

        messages = [{"role": "user", "content": prompt}]
        # 主持人使用稍高的 max_tokens
        moderator_tokens = max(self.style_config.max_tokens * 2, 800)

        # Use streaming if enabled
        if self.enable_streaming and self._stream_callback:
            partial_content = [""]

            def on_token(token: str):
                partial_content[0] += token
                try:
                    self._stream_callback({
                        "type": "partial_message",
                        "data": {
                            "speaker": "主持人" if self.language == "zh" else "Moderator",
                            "role": "moderator",
                            "content": partial_content[0],
                            "is_complete": False
                        }
                    })
                except:
                    pass

            response = self.ai_client.generate_text_stream(
                messages, max_tokens=moderator_tokens, temperature=0.8, on_token=on_token
            )

            # Emit complete event
            try:
                self._stream_callback({
                    "type": "message",
                    "data": {
                        "speaker": "主持人" if self.language == "zh" else "Moderator",
                        "role": "moderator",
                        "content": response,
                        "is_complete": True
                    }
                })
            except:
                pass

            return response
        else:
            return self.ai_client.generate_text(messages, max_tokens=moderator_tokens, temperature=0.8)

    def _generate_character_speech(
        self,
        character: Character,
        prompt_content: str,
        is_character1: bool
    ) -> str:
        """
        生成角色发言（支持流式输出）

        Args:
            character: 角色对象
            prompt_content: prompt内容
            is_character1: 是否是角色1

        Returns:
            生成的发言内容
        """
        # 选择对应的上下文
        context = self.character1_context if is_character1 else self.character2_context

        # 添加新的user消息
        context.append({"role": "user", "content": prompt_content})

        # Prepare streaming callback if enabled
        if self.enable_streaming and self._stream_callback:
            # Use list to allow mutation in nested function
            partial_content = [""]

            def on_token(token: str):
                """Token callback for streaming"""
                partial_content[0] += token
                # Emit partial message event
                try:
                    self._stream_callback({
                        "type": "partial_message",
                        "data": {
                            "speaker": character.name,
                            "role": "character1" if is_character1 else "character2",
                            "content": partial_content[0],
                            "is_complete": False
                        }
                    })
                except Exception as e:
                    # Don't let callback errors break generation
                    print(f"⚠ Error in stream callback: {e}")

            # Generate with streaming
            response = self.ai_client.generate_text_stream(
                messages=context,
                system=character.system_prompt,
                max_tokens=self.style_config.max_tokens,
                temperature=self.style_config.temperature,
                on_token=on_token
            )

            # Emit final complete message event
            try:
                self._stream_callback({
                    "type": "message",
                    "data": {
                        "speaker": character.name,
                        "role": "character1" if is_character1 else "character2",
                        "content": response,
                        "is_complete": True
                    }
                })
            except Exception as e:
                print(f"⚠ Error in stream callback: {e}")

        else:
            # Non-streaming mode (existing behavior)
            response = self.ai_client.generate_text(
                messages=context,
                system=character.system_prompt,
                max_tokens=self.style_config.max_tokens,
                temperature=self.style_config.temperature
            )

        # 将assistant回复也加入上下文
        context.append({"role": "assistant", "content": response})

        return response

    def _get_debate_history_text(self) -> str:
        """获取格式化的辩论历史文本"""
        history_lines = []
        for msg in self.messages:
            history_lines.append(f"{msg.speaker}：{msg.content}\n")
        return "\n".join(history_lines)

    # ===== Comedy-Duo 特殊流程 =====

    def _run_collaborative_performance(self, progress_callback: Optional[Callable[[str], None]] = None) -> List[DebateMessage]:
        """
        运行捧哏模式的特殊流程（合作模式）

        Args:
            progress_callback: 进度回调函数

        Returns:
            完整的表演消息列表
        """
        total_steps = 2 + 2 + self.rounds * 2 + 1 + 1
        current_step = 3

        # 1. 主持人开场（comedy 专用）
        if progress_callback:
            progress_callback(f"[{current_step}/{total_steps}] 生成主持人开场...")
        current_step += 1

        moderator_opening = self._generate_comedy_moderator_opening()
        self.messages.append(DebateMessage("主持人" if self.language == "zh" else "Host", "moderator", moderator_opening))

        # 2. 逗哏开场
        if progress_callback:
            progress_callback(f"[{current_step}/{total_steps}] {self.character1.name} 开场...")
        current_step += 1

        lead_opening = self._generate_character_speech(
            self.character1,
            self.prompter.get_comedy_lead_opening(),
            True
        )
        self.messages.append(DebateMessage(self.character1.name, "character1", lead_opening))

        # 3. 捧哏配合
        if progress_callback:
            progress_callback(f"[{current_step}/{total_steps}] {self.character2.name} 配合...")
        current_step += 1

        support_opening = self._generate_character_speech(
            self.character2,
            self.prompter.get_comedy_support_response(lead_opening),
            False
        )
        self.messages.append(DebateMessage(self.character2.name, "character2", support_opening))

        # 4. 交替表演（N 轮）
        for round_num in range(1, self.rounds + 1):
            # 逗哏表演
            if progress_callback:
                progress_callback(f"[{current_step}/{total_steps}] 第{round_num}轮 - {self.character1.name} 表演...")
            current_step += 1

            lead_prompt = self.prompter.get_comedy_exchange_prompt(
                round_num, self.rounds, True, self.messages[-1].content
            )
            lead_statement = self._generate_character_speech(self.character1, lead_prompt, True)
            self.messages.append(DebateMessage(self.character1.name, "character1", lead_statement))

            # 捧哏配合
            if progress_callback:
                progress_callback(f"[{current_step}/{total_steps}] 第{round_num}轮 - {self.character2.name} 配合...")
            current_step += 1

            support_prompt = self.prompter.get_comedy_exchange_prompt(
                round_num, self.rounds, False, lead_statement
            )
            support_statement = self._generate_character_speech(self.character2, support_prompt, False)
            self.messages.append(DebateMessage(self.character2.name, "character2", support_statement))

        # 5. 共同收尾（与标准流程不同）
        if progress_callback:
            progress_callback(f"[{current_step}/{total_steps}] 生成共同收尾...")
        current_step += 1

        joint_closing_prompt = self.prompter.get_comedy_joint_closing(
            self.character1.name, self.character2.name
        )
        joint_closing = self._generate_character_speech(
            self.character1, joint_closing_prompt, True
        )
        self.messages.append(DebateMessage(
            f"{self.character1.name} & {self.character2.name}",
            "both",
            joint_closing
        ))

        # 6. 主持人点评
        if progress_callback:
            progress_callback(f"[{current_step}/{total_steps}] 生成主持人点评...")

        moderator_closing = self._generate_comedy_moderator_closing()
        self.messages.append(DebateMessage("主持人" if self.language == "zh" else "Host", "moderator", moderator_closing))

        return self.messages

    def _generate_comedy_moderator_opening(self) -> str:
        """生成捧哏模式的主持人开场"""
        prompt = self.prompter.get_comedy_duo_opening(
            self.character1.name, self.character2.name, self.topic,
            self.character1.profile, self.character2.profile
        )
        messages = [{"role": "user", "content": prompt}]
        moderator_tokens = max(self.style_config.max_tokens * 2, 800)
        return self.ai_client.generate_text(messages, max_tokens=moderator_tokens, temperature=0.8)

    def _generate_comedy_moderator_closing(self) -> str:
        """生成捧哏模式的主持人总结点评"""
        recent_messages = self.messages[-8:] if len(self.messages) > 8 else self.messages
        debate_summary = "\n\n".join([f"{msg.speaker}: {msg.content}" for msg in recent_messages])

        prompt = self.prompter.get_comedy_moderator_closing(
            self.character1.name, self.character2.name, debate_summary
        )
        messages = [{"role": "user", "content": prompt}]
        moderator_tokens = max(self.style_config.max_tokens * 2, 800)
        return self.ai_client.generate_text(messages, max_tokens=moderator_tokens, temperature=0.8)
