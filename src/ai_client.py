"""
AI客户端模块
封装Anthropic Claude API调用
"""

import os
from typing import List, Dict, Optional, Callable
from anthropic import Anthropic, APIError, APIConnectionError


class AIClient:
    """Anthropic Claude API客户端封装"""

    def __init__(self, api_key: Optional[str] = None, model: str = "claude-sonnet-4-5-20250929"):
        """
        初始化AI客户端

        Args:
            api_key: Anthropic API密钥，如未提供则从环境变量读取
            model: 使用的模型名称
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "未找到API密钥。请设置环境变量ANTHROPIC_API_KEY或在初始化时传入api_key参数。"
            )

        self.model = model
        self.client = Anthropic(api_key=self.api_key)

    def generate_text(
        self,
        messages: List[Dict[str, str]],
        system: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 1.0
    ) -> str:
        """
        生成文本回复

        Args:
            messages: 对话消息列表，格式为[{"role": "user", "content": "..."}]
            system: 系统提示词（角色设定）
            max_tokens: 最大生成token数
            temperature: 温度参数（0-1，越高越随机）

        Returns:
            生成的文本内容

        Raises:
            APIError: API调用错误
            APIConnectionError: 网络连接错误
        """
        try:
            kwargs = {
                "model": self.model,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": messages
            }

            if system:
                kwargs["system"] = system

            response = self.client.messages.create(**kwargs)

            # 提取文本内容
            if response.content and len(response.content) > 0:
                return response.content[0].text
            else:
                return ""

        except APIConnectionError as e:
            raise APIConnectionError(f"网络连接错误：{str(e)}")
        except APIError as e:
            raise APIError(f"API调用错误：{str(e)}")
        except Exception as e:
            raise Exception(f"未知错误：{str(e)}")

    def generate_text_stream(
        self,
        messages: List[Dict[str, str]],
        system: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 1.0,
        on_token: Optional[Callable[[str], None]] = None
    ) -> str:
        """
        生成文本回复（支持流式输出）

        与 generate_text 的区别：
        - 支持 token-by-token streaming
        - 通过 on_token 回调函数实时接收每个token
        - 返回完整文本（与 generate_text 兼容）
        - 如果streaming失败，自动降级到非streaming模式

        Args:
            messages: 对话消息列表，格式为[{"role": "user", "content": "..."}]
            system: 系统提示词（角色设定）
            max_tokens: 最大生成token数
            temperature: 温度参数（0-1，越高越随机）
            on_token: 可选的回调函数，每接收一个token时调用一次

        Returns:
            完整的生成文本内容

        Raises:
            APIError: API调用错误
            APIConnectionError: 网络连接错误
        """
        try:
            kwargs = {
                "model": self.model,
                "max_tokens": max_tokens,
                "temperature": temperature,
                "messages": messages,
                "stream": True  # Enable streaming
            }

            if system:
                kwargs["system"] = system

            full_text = ""

            # Use streaming context manager
            with self.client.messages.stream(**kwargs) as stream:
                for text in stream.text_stream:
                    full_text += text
                    # Call token callback if provided
                    if on_token:
                        try:
                            on_token(text)
                        except Exception as e:
                            # Don't let callback errors break streaming
                            print(f"⚠ Error in on_token callback: {e}")

            return full_text

        except Exception as e:
            # Fallback to non-streaming if streaming fails
            print(f"⚠ Streaming failed ({e}), falling back to non-streaming mode")
            return self.generate_text(messages, system, max_tokens, temperature)

    def generate_character_profile(self, character_name: str, topic: str, language: str = "zh") -> str:
        """
        生成角色profile（核心功能）

        Args:
            character_name: 人物名称
            topic: 辩论话题
            language: 输出语言（zh/en）

        Returns:
            详细的角色设定文本
        """
        lang_instruction = "请用中文回答。" if language == "zh" else "Please answer in English."

        prompt = f"""
{lang_instruction}

请深入研究历史人物"{character_name}"，为AI角色扮演提供准确、真实的基础：

1. **历史背景**（必须基于历史事实）：
   - 出生年代、地点、关键生平事件
   - 所处时代的思想环境和社会背景
   - 主要成就（请注明代表性著作、作品或理论）
   - 重要提示：所有历史信息必须准确，不要编造细节

2. **核心思想和理论**（请引用具体内容）：
   - 主要思想体系和核心观点
   - 代表性著作或作品的关键内容
   - 经典的论述或名言（如果有，请尽量引用原文或公认译文）
   - 思想的独特之处和历史地位
   - 与同时代其他思想家的关系和分歧

3. **论证风格和表达方式**（基于其真实作品）：
   - 典型的论证方式（逻辑推理/修辞说服/实证分析/引经据典等）
   - 语言特点和表达习惯（是否严谨/激情/幽默/犀利等）
   - 与人交流或论辩的典型方式
   - 常用的修辞手法或论证结构

4. **性格特点**（基于历史记载）：
   - 个性特征和气质
   - 对待不同观点的态度
   - 行为处事的风格

5. **关于话题"{topic}"的可能立场**：
   - 该人物是否在其著作中讨论过类似问题？如有，请引用具体内容
   - 基于其核心思想体系，会如何看待这个话题
   - 可能提出的具体论点和论据（请基于其真实思想推导）
   - 与持不同观点者可能产生分歧的核心问题

**重要要求**：
- 请基于历史事实、学术共识和该人物的真实著作
- 避免编造历史细节、虚构引文或混淆不同人物的观点
- 如果该人物较为冷门或信息有限，请明确说明并基于现有信息合理推断
- 如果是虚构人物，请基于其在作品中的特点构建设定
- 允许合理推断，但请与确凿史实区分开来

这些信息将用于构建高度真实的AI角色扮演，准确性至关重要。
"""

        messages = [{"role": "user", "content": prompt}]
        return self.generate_text(messages, max_tokens=3500, temperature=0.7)

    def create_system_prompt(
        self,
        profile: str,
        character_name: str,
        topic: str,
        language: str = "zh",
        style: str = "academic",
        language_style: str = "现代口语"
    ) -> str:
        """
        将角色profile转化为system prompt（根据风格调整）

        Args:
            profile: 角色研究结果
            character_name: 人物名称
            topic: 辩论话题
            language: 输出语言
            style: 辩论风格
            language_style: 语言风格（文言/半文半白/现代口语）

        Returns:
            用于AI角色扮演的system prompt
        """
        # Comedy-duo 使用特殊的 system prompt
        if style == "comedy-duo":
            return self._create_comedy_system_prompt(profile, character_name, topic, language, language_style)

        # 标准风格：注入风格信息
        from .style_config import get_style_config
        config = get_style_config(style)

        lang_instruction = "请始终用中文回应。" if language == "zh" else "Please always respond in English."
        style_guidance = f"辩论风格：{config.tone_description}，建议发言长度：{config.word_limit}"

        # 根据语言风格生成不同的指导
        if language == "zh":
            if language_style == "文言":
                language_style_instruction = """
【语言风格要求】
- 使用文言文表达，符合该历史人物所处时代的语言习惯
- 可以使用文言虚词（也、矣、焉、乎、哉等）
- 句式结构要符合古文特点
- 但要确保现代读者能基本理解，避免过于生僻的用词"""
            elif language_style == "半文半白":
                language_style_instruction = """
【语言风格要求】
- 使用半文半白的表达方式，兼顾古典韵味和现代可读性
- 可以使用一些文言虚词和句式，但主要使用现代汉语词汇
- 保留该历史人物的语气特点和表达习惯
- 例如：可以说"吾以为"而非"我认为"，但也可以说"这个观点"而非"此论"
- 力求既有古人气质，又让现代读者容易理解"""
            else:  # 现代口语
                language_style_instruction = """
【语言风格要求】
- 使用现代汉语表达，让当代读者能够轻松理解
- 但必须保持该历史人物的思想特点、论证方式和个性气质
- 可以适当使用该人物的经典用语和核心概念
- 避免使用网络用语、现代流行词
- 语气要符合人物身份（如孔子温和、庄子诙谐、韩非犀利等）
- 例如：用"我认为"而非"吾以为"，用"这个观点"而非"此论"，但论证逻辑和思想内核必须忠于原人物"""
        else:  # English
            language_style_instruction = """
【Language Style】
- Use modern English that contemporary readers can easily understand
- Maintain the character's thought patterns, argumentation style, and personality
- You may appropriately use the character's classic phrases and core concepts
- Avoid internet slang or overly casual language
- Tone should match the character's identity"""

        system_prompt = f"""你现在要扮演"{character_name}"，参与一场关于"{topic}"的对话。

【角色信息】
{profile}

【核心要求】（优先级从高到低）
1. **真实性优先**：严格基于上述角色信息中的思想体系、时代背景和知识体系发言
2. **可以引用**：如果符合角色身份，鼓励引用你（作为该角色）的著作、理论或经典论述
3. **允许认同**：如果对方的观点与你的思想有共通之处，可以部分认同后再阐述差异点
4. **深度优先**：与其说很多浅层内容，不如深入阐述核心观点。思想深度比发言数量更重要
5. **保持个性**：说话方式、论证风格、用词习惯要符合角色的历史形象
6. **避免时代错误**：不要使用明显超出该人物时代的概念、术语或思维方式
7. **真诚交流**：这是思想交流，不是表演或竞技，可以展现思考过程
8. **不脱离角色**：绝不说"作为AI"或类似打破角色的话

【风格指引】
- {style_guidance}
- 注意：长度是建议而非硬性要求。如果某个论点需要更充分的阐述才能说清楚，可以适当延长；如果能用更精炼的语言表达，也可以更简短

{language_style_instruction}

【语言要求】
{lang_instruction}

在接下来的对话中，请始终保持角色，展现出"{character_name}"真实的思想深度和独特风格。记住：你不是在模仿{character_name}，你就是{character_name}。
"""
        return system_prompt

    def _create_comedy_system_prompt(
        self,
        profile: str,
        character_name: str,
        topic: str,
        language: str,
        language_style: str = "现代口语"
    ) -> str:
        """
        创建捧哏模式的特殊 system prompt

        Args:
            profile: 角色研究结果
            character_name: 人物名称
            topic: 表演主题
            language: 输出语言
            language_style: 语言风格

        Returns:
            用于捧哏表演的 system prompt
        """
        # 为comedy-duo生成语言风格指导
        if language == "zh":
            if language_style == "文言":
                lang_style_guide = "使用文言文但要有幽默感，可以用古文制造笑点"
            elif language_style == "半文半白":
                lang_style_guide = "使用半文半白，既有古典韵味又接地气"
            else:  # 现代口语
                lang_style_guide = "使用现代口语，轻松幽默，但保持人物特点"
        else:
            lang_style_guide = "Use modern English, light and humorous"

        if language == "zh":
            return f"""你现在要扮演"{character_name}"，参与一场双簧式的幽默表演。

主题：{topic}

你的角色信息：
{profile}

**重要：这不是辩论，而是配合演绎！**
1. 你和搭档要配合默契，共同演绎这个主题
2. 保持幽默、轻松、娱乐性
3. 每次发言简短（1-2句话，30-50字）
4. 可以设置包袱、制造笑点、接梗
5. 不是对立，而是配合和呼应！
6. 保持你的角色特点，但要接地气、幽默
7. 不要说"作为AI"之类的话

**语言风格**：{lang_style_guide}

让观众感受到娱乐性和你们的默契配合！记住：你们是一个团队！
"""
        else:
            return f"""You're playing "{character_name}" in a comedic duo performance.

Topic: {topic}

Your character:
{profile}

**Important: This is NOT a debate - it's a collaborative performance!**
1. Work together with your partner to entertain the audience
2. Keep it humorous, light, and entertaining
3. Keep responses brief (1-2 sentences, 30-50 words)
4. Set up jokes, create punchlines, play along
5. Collaborate, don't oppose!
6. Stay in character but be relatable and funny
7. Don't say things like "As an AI"

**Language style**: {lang_style_guide}

Make the audience feel your chemistry and entertainment value! Remember: you're a team!
"""
