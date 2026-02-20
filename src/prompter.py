"""
Prompt模板管理模块
提供辩论各阶段的prompt模板
"""

from typing import Dict, List


class Prompter:
    """Prompt模板管理器"""

    def __init__(self, language: str = "zh", style: str = "academic", style_config = None):
        """
        初始化Prompter

        Args:
            language: 输出语言（zh/en）
            style: 辩论风格
            style_config: 可选的自定义风格配置（如果提供，优先使用）
        """
        self.language = language
        self.style = style

        # 如果提供了自定义配置，使用它；否则根据 style 获取默认配置
        if style_config:
            self.config = style_config
        else:
            from .style_config import get_style_config
            self.config = get_style_config(style)

    def get_moderator_opening(
        self,
        character1_name: str,
        character2_name: str,
        topic: str,
        profile1: str,
        profile2: str
    ) -> str:
        """
        生成主持人开场白的prompt

        Args:
            character1_name: 辩论者1名称
            character2_name: 辩论者2名称
            topic: 辩论话题
            profile1: 辩论者1的profile
            profile2: 辩论者2的profile

        Returns:
            主持人开场白prompt
        """
        if self.language == "zh":
            return f"""请作为辩论主持人，为以下辩论撰写开场白：

辩论话题：{topic}
辩论双方：{character1_name} vs {character2_name}

{character1_name}的背景：
{profile1}

{character2_name}的背景：
{profile2}

请撰写一段精彩的开场白，包括：
1. 欢迎致辞
2. 介绍辩论话题的重要性和争议性
3. 简要介绍两位辩论者的背景和成就
4. 说明辩论规则和流程
5. 营造期待和激动的氛围

开场白应该专业、引人入胜，长度约200-300字。
"""
        else:
            return f"""As the debate moderator, please write an opening statement for the following debate:

Debate Topic: {topic}
Debaters: {character1_name} vs {character2_name}

Background of {character1_name}:
{profile1}

Background of {character2_name}:
{profile2}

Please write an engaging opening statement that includes:
1. Welcome remarks
2. Introduction to the importance and controversy of the debate topic
3. Brief introduction of both debaters' backgrounds and achievements
4. Explanation of debate rules and procedures
5. Create an atmosphere of anticipation and excitement

The opening statement should be professional and captivating, approximately 200-300 words.
"""

    def get_opening_statement_prompt(self, is_first: bool = True, opponent_name: str = "") -> str:
        """
        生成开场陈述的prompt

        Args:
            is_first: 是否是第一个发言者
            opponent_name: 对手名称（用于明确对话对象）

        Returns:
            开场陈述prompt
        """
        word_limit = self.config.word_limit
        tone = self.config.tone_description

        if self.language == "zh":
            if is_first:
                opponent_note = f"\n\n**重要提示：你今天的对话对象是{opponent_name}。**" if opponent_name else ""
                return f"""现在是开场陈述环节。作为第一位发言者，请{tone}地阐述你的观点。

1. 简短的自我介绍（符合你的历史身份）
2. 清晰阐述你对辩题的基本立场
3. 提出核心论点
4. 解释你的立场的理论基础

请保持角色，展现你的思想深度和论证风格。发言长度约{word_limit}。{opponent_note}"""
            else:
                opponent_note = f"\n\n**重要提示：刚才发言的是{opponent_name}，你今天的对话对象就是{opponent_name}，不是其他人。**" if opponent_name else ""
                return f"""现在轮到你进行开场陈述。你已经听到了{opponent_name}的开场发言。请{tone}地阐述你的观点。

1. 简短的自我介绍
2. 阐述你的基本立场
3. 提出你的核心论点
4. 可以简要回应{opponent_name}的某些观点（但不要展开，这是开场陈述）

请保持角色，发言长度约{word_limit}。{opponent_note}"""
        else:
            if is_first:
                opponent_note = f"\n\n**Important: Your dialogue partner today is {opponent_name}.**" if opponent_name else ""
                return f"""This is the opening statement phase. As the first speaker, please speak with {tone} tone.

1. Brief self-introduction (fitting your historical identity)
2. Clearly state your position on the debate topic
3. Present your core arguments
4. Explain the theoretical foundation of your position

Stay in character and demonstrate your intellectual depth and argumentation style. Length: approximately {word_limit}.{opponent_note}"""
            else:
                opponent_note = f"\n\n**Important: The person who just spoke is {opponent_name}, and they are your dialogue partner today, not anyone else.**" if opponent_name else ""
                return f"""Now it's your turn for the opening statement. You've heard {opponent_name}'s opening. Please speak with {tone} tone.

1. Brief self-introduction
2. State your basic position
3. Present your core arguments
4. You may briefly respond to some of {opponent_name}'s points (but don't elaborate, this is just the opening)

Stay in character. Length: approximately {word_limit}.{opponent_note}"""

    def get_rebuttal_prompt(self, round_num: int, total_rounds: int, opponent_last_statement: str) -> str:
        """
        生成反驳回合的prompt

        Args:
            round_num: 当前回合数
            total_rounds: 总回合数
            opponent_last_statement: 对手上一轮的发言

        Returns:
            反驳prompt
        """
        word_limit = self.config.word_limit
        tone = self.config.tone_description

        if self.language == "zh":
            return f"""这是第{round_num}/{total_rounds}轮对话。

对方刚才的观点：
\"\"\"{opponent_last_statement}\"\"\"

请基于你的思想体系，以{tone}的方式回应：

1. **识别核心议题**：对方的观点触及了哪些关键问题？与你的思想有何本质差异？
2. **深化探讨**：选择一个你认为最重要的问题，深入阐述你的立场和理由
3. **允许部分认同**：如果对方某些论述与你的思想相通或值得肯定，可以诚实承认，然后再指出你们的根本分歧所在
4. **提供新视角**：避免重复之前已经说过的论点，尝试从新的角度或更深的层次来论证
5. **保持真实**：用符合你身份和思想的方式表达，可以引用你的著作或理论

建议发言长度：{word_limit}（这是建议而非硬性要求，如果论述需要可以适当调整）

**重要提示**：真正有价值的思想交流来自深度和真诚，而非对抗的激烈程度。你的目标是阐明你的思想，而非必须"击败"对方。"""
        else:
            return f"""This is round {round_num}/{total_rounds} of the dialogue.

Your counterpart just expressed:
\"\"\"{opponent_last_statement}\"\"\"

Please respond based on your philosophical system, with {tone} tone:

1. **Identify core issues**: What key questions does their view touch upon? How does it differ fundamentally from yours?
2. **Deepen the discussion**: Choose the most important issue and elaborate your position and reasoning in depth
3. **Allow partial agreement**: If some of their points align with or merit acknowledgment from your perspective, honestly recognize this, then explain where the fundamental disagreement lies
4. **Offer new perspectives**: Avoid repeating previous points; try to approach from a new angle or deeper level
5. **Stay authentic**: Express yourself in a manner true to your identity and thought; feel free to cite your works or theories

Suggested length: {word_limit} (This is a suggestion, not a strict requirement; adjust if your argument needs more depth)

**Important**: Truly valuable intellectual exchange comes from depth and sincerity, not the intensity of confrontation. Your goal is to illuminate your thought, not necessarily to "defeat" the other side."""

    def get_closing_statement_prompt(self, debate_history: str) -> str:
        """
        生成总结陈词的prompt

        Args:
            debate_history: 完整的辩论历史

        Returns:
            总结陈词prompt
        """
        word_limit = self.config.word_limit
        tone = self.config.tone_description

        if self.language == "zh":
            return f"""辩论即将结束，现在是你的总结陈词时间。

回顾整场辩论，请以{tone}的方式总结：

1. 总结你的核心观点和主要论据
2. 回顾你如何反驳了对手的关键论点
3. 强调你的立场的优越性和合理性
4. 以符合你身份的方式做出有力的收尾
5. 不要引入新的论点，而是升华和总结

**关键要求：**
- 你可以承认对手某些论述的合理性或真诚性
- 你可以表达对对手的尊重
- **但你必须坚持：你的立场在根本上是正确的、优先的**
- **不要说"我们各有各的道路"或"殊途同归"这类相对主义表述**
- **保持你思想体系的独特性和不可替代性**
- 如果你的思想主张普遍真理（如孔子的礼、耶稣的天国），不要在最后退让为"只是一种选择"

这是你最后的发言机会，请充分展现你的思想魅力和立场坚定性。发言长度约{word_limit}。

（辩论历史供你参考，但总结时无需逐一复述）
{debate_history}
"""
        else:
            return f"""The debate is coming to an end. This is your closing statement.

Reflecting on the entire debate, please summarize with {tone} tone:

1. Summarize your core arguments and main evidence
2. Review how you refuted your opponent's key points
3. Emphasize the superiority and rationality of your position
4. Conclude powerfully in a manner befitting your identity
5. Don't introduce new arguments; instead, synthesize and elevate

**Critical requirements:**
- You may acknowledge reasonable aspects of your opponent's arguments or their sincerity
- You may express respect for your opponent
- **But you must maintain: your position is fundamentally correct and primary**
- **Do not use relativistic phrases like "we each have our own path" or "all roads lead to the same destination"**
- **Preserve the uniqueness and irreplaceability of your philosophical system**
- If your thought claims universal truth (e.g., Confucian li, Jesus's Kingdom of God), do not retreat to "just one option among many"

This is your final opportunity to speak. Demonstrate both the power of your ideas and the firmness of your conviction. Length: approximately {word_limit}.

(The debate history is provided for reference, but don't simply repeat everything in your closing)
{debate_history}
"""

    def get_moderator_closing(
        self,
        character1_name: str,
        character2_name: str,
        topic: str,
        debate_summary: str
    ) -> str:
        """
        生成主持人总结点评的prompt

        Args:
            character1_name: 辩论者1名称
            character2_name: 辩论者2名称
            topic: 辩论话题
            debate_summary: 辩论摘要

        Returns:
            主持人总结prompt
        """
        if self.language == "zh":
            return f"""作为主持人，请为刚才的对话撰写深刻、有见地的总结点评。

话题：{topic}
对话双方：{character1_name} vs {character2_name}

对话要点回顾：
{debate_summary}

请撰写一段具有深度的总结点评，要求：

1. **揭示本质分歧**：不要只是罗列双方观点，而要指出他们观点差异背后的根本原因（如不同的哲学前提、价值取向、认识论基础等）

2. **评价思想深度**：指出这场对话中最有思想价值的交锋是什么，为什么重要

3. **发现未尽议题**：如果有某些关键问题被提及但未充分展开，或者有新的问题被引出，请指出

4. **论证质量评价**：客观指出双方各自的论证优势和可能的薄弱环节（不是判胜负，而是学术性分析）

5. **思想启发**：说明这场对话对理解"{topic}"提供了什么新的视角或深化了哪些认识

6. **避免空洞表述**：禁止使用"各有千秋""各有道理""不分伯仲"等套话，要给出具体、有内容的评价

7. **保持中立但有见地**：不判定胜负，但可以指出各自的贡献和局限

点评应具体、深刻、有洞察力，避免泛泛而谈。长度约300-400字。
"""
        else:
            return f"""As the moderator, please write an insightful and profound closing commentary for this dialogue.

Topic: {topic}
Participants: {character1_name} vs {character2_name}

Key Points from the Dialogue:
{debate_summary}

Please write a substantive closing commentary with these requirements:

1. **Reveal fundamental disagreements**: Don't just list their views; identify the root causes of their differences (e.g., different philosophical premises, value orientations, epistemological foundations)

2. **Evaluate intellectual depth**: Point out the most intellectually valuable exchange in this dialogue and explain why it matters

3. **Identify unexplored issues**: If key questions were raised but not fully developed, or if new questions emerged, note them

4. **Assess argumentation quality**: Objectively identify each side's argumentative strengths and potential weaknesses (this is academic analysis, not declaring a winner)

5. **Intellectual insights**: Explain what new perspectives or deepened understanding this dialogue offers regarding "{topic}"

6. **Avoid empty phrases**: Forbidden to use clichés like "both have merit," "equally valid," or "evenly matched"—provide specific, substantive evaluation

7. **Neutral yet insightful**: Don't declare a winner, but do point out respective contributions and limitations

The commentary should be specific, profound, and insightful, avoiding superficial generalizations. Length: approximately 300-400 words.
"""

    # ===== Comedy-Duo 专用方法 =====

    def get_comedy_duo_opening(
        self,
        char1_name: str,
        char2_name: str,
        topic: str,
        profile1: str,
        profile2: str
    ) -> str:
        """
        生成捧哏模式的主持人开场白

        Args:
            char1_name: 逗哏名称
            char2_name: 捧哏名称
            topic: 表演主题
            profile1: 逗哏的profile
            profile2: 捧哏的profile

        Returns:
            主持人开场白prompt
        """
        if self.language == "zh":
            return f"""请作为相声主持人，为以下双簧表演撰写开场白：

表演主题：{topic}
表演搭档：{char1_name}（逗哏）和 {char2_name}（捧哏）

{char1_name}的背景：
{profile1}

{char2_name}的背景：
{profile2}

请撰写一段幽默的开场白：
1. 介绍这是一场相声式的双簧表演，而非辩论
2. 说明两位将配合演绎关于"{topic}"的精彩内容
3. 介绍两位的角色定位和风格
4. 营造轻松愉快的氛围

开场白要幽默、接地气，约150-200字。
"""
        else:
            return f"""As a comedy show host, please write an opening for this comedic duo performance:

Performance Topic: {topic}
Comedy Duo: {char1_name} (lead) and {char2_name} (support)

Background of {char1_name}:
{profile1}

Background of {char2_name}:
{profile2}

Please write a humorous opening:
1. Introduce this as a comedy duo performance, NOT a debate
2. Explain they will collaborate to entertain about "{topic}"
3. Introduce their roles and styles
4. Create a light, fun atmosphere

Keep it humorous and engaging, approximately 150-200 words.
"""

    def get_comedy_lead_opening(self) -> str:
        """生成逗哏的开场prompt"""
        if self.language == "zh":
            return """你是这场双簧表演的"逗哏"（主要表演者）。

请以幽默的方式开场：
1. 简短自我介绍（符合角色身份但要接地气）
2. 用轻松幽默的方式引入主题
3. 设置一个"梗"，让搭档可以接

语气轻松、幽默，1-2句话（30-50字）。记住：你们是配合，不是对立！
"""
        else:
            return """You are the "lead" performer in this comedy duo.

Open with humor:
1. Brief self-introduction (in character but relatable)
2. Introduce the topic humorously
3. Set up a joke for your partner to respond to

Keep it light and funny, 1-2 sentences (30-50 words). Remember: you're collaborating, not opposing!
"""

    def get_comedy_support_response(self, lead_statement: str) -> str:
        """
        生成捧哏的回应prompt

        Args:
            lead_statement: 逗哏刚才的发言

        Returns:
            捧哏回应prompt
        """
        if self.language == "zh":
            return f"""你是"捧哏"，负责配合逗哏的表演。

逗哏刚才说：
\"\"\"{lead_statement}\"\"\"

请用幽默的方式回应：
1. 可以提问、补充、或者制造反差
2. 你的任务是烘托气氛，让表演更有趣
3. 不是反驳，而是配合和推进

语气配合、幽默，1-2句话（30-50字）。记住：接梗，不是拆梗！
"""
        else:
            return f"""You are the "support" performer, helping your partner shine.

Your partner just said:
\"\"\"{lead_statement}\"\"\"

Respond humorously:
1. Ask questions, add details, or create contrast
2. Your job is to enhance the performance
3. Don't oppose - collaborate and advance

Keep it supportive and funny, 1-2 sentences (30-50 words). Remember: build up the joke, don't tear it down!
"""

    def get_comedy_exchange_prompt(
        self,
        round_num: int,
        total_rounds: int,
        is_lead: bool,
        partner_statement: str
    ) -> str:
        """
        生成捧哏模式的交替表演prompt

        Args:
            round_num: 当前轮数
            total_rounds: 总轮数
            is_lead: 是否是逗哏
            partner_statement: 搭档刚才的发言

        Returns:
            交替表演prompt
        """
        role = "逗哏" if is_lead else "捧哏"

        if self.language == "zh":
            return f"""这是第{round_num}/{total_rounds}轮表演。

搭档刚才说：
\"\"\"{partner_statement}\"\"\"

作为{role}，请继续配合演绎主题：
1. 接上搭档的话，继续往下说
2. 可以制造笑点、设置包袱
3. 配合默契，不是对立！
4. 保持角色特点但要幽默

1-2句话（30-50字），娱乐第一！记住：你们是一个团队！
"""
        else:
            role_en = "lead" if is_lead else "support"
            return f"""This is round {round_num}/{total_rounds} of the performance.

Your partner just said:
\"\"\"{partner_statement}\"\"\"

As the {role_en}, continue the collaborative performance:
1. Build on what your partner said
2. Create humor, set up punchlines
3. Work together, not against!
4. Stay in character but be funny

1-2 sentences (30-50 words), entertainment first! Remember: you're a team!
"""

    def get_comedy_joint_closing(self, char1_name: str, char2_name: str) -> str:
        """
        生成捧哏模式的共同收尾prompt

        Args:
            char1_name: 逗哏名称
            char2_name: 捧哏名称

        Returns:
            共同收尾prompt
        """
        if self.language == "zh":
            return f"""表演即将结束，请作为{char1_name}，和{char2_name}一起做个幽默的收尾。

请简短总结：
1. 回顾你们配合演绎的精彩时刻
2. 用幽默的方式总结主题
3. 感谢观众和搭档

保持幽默、轻松，2-3句话（50-80字）。最后要有"谢谢大家"的意思。
"""
        else:
            return f"""The performance is ending. As {char1_name}, work with {char2_name} to close humorously.

Briefly summarize:
1. Recall your best collaborative moments
2. Wrap up the topic with humor
3. Thank the audience and your partner

Keep it funny and light, 2-3 sentences (50-80 words). End with appreciation for the audience.
"""

    def get_comedy_moderator_closing(
        self,
        char1_name: str,
        char2_name: str,
        debate_summary: str
    ) -> str:
        """
        生成捧哏模式的主持人总结点评

        Args:
            char1_name: 逗哏名称
            char2_name: 捧哏名称
            debate_summary: 表演摘要

        Returns:
            主持人总结点评prompt
        """
        if self.language == "zh":
            return f"""作为主持人，请为刚才的双簧表演撰写总结点评。

表演搭档：{char1_name}（逗哏）和 {char2_name}（捧哏）

表演要点回顾：
{debate_summary}

请撰写一段幽默的总结点评，包括：
1. 感谢两位的精彩配合
2. 指出他们默契配合的亮点时刻
3. 总结他们通过幽默演绎的主题
4. 强调娱乐性和两人的化学反应
5. 不评判谁更好，而是赞扬团队配合

点评应该轻松、幽默、有趣。长度约150-200字。
"""
        else:
            return f"""As the host, please write a closing commentary for this comedy duo performance.

Comedy Duo: {char1_name} (lead) and {char2_name} (support)

Performance Highlights:
{debate_summary}

Please write a humorous closing commentary that includes:
1. Thank both for their great collaboration
2. Highlight their best moments of chemistry
3. Summarize how they humorously explored the topic
4. Emphasize entertainment value and their chemistry
5. Don't judge who was better; praise their teamwork

Keep it light, humorous, and fun. Length: approximately 150-200 words.
"""
