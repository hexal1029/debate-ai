# 🎭 AI历史人物辩论生成器

一个基于AI的历史人物辩论生成器，**核心特点是完全动态化**：用户可以输入任意两个人物名称和一个辩论话题，系统自动研究这两个人物的背景、思想、风格，构建符合其历史形象的角色设定，并生成一场真实可信的辩论对话。

## ✨ 核心特性

### 🎯 支持任意历史人物

- **完全动态化**：不预设任何人物信息，一切基于用户输入动态生成
- **广泛适用**：支持中文、英文及其他语言的人物名称
- **智能适配**：自动处理知名度不同的历史人物，甚至虚构人物

### 🧠 深度角色构建

- **AI驱动研究**：使用Claude AI深入分析人物的历史背景、核心思想、性格特点和论证风格
- **真实还原**：基于人物的时代背景和思想体系构建角色设定
- **个性化表达**：每个角色都有独特的说话方式和论证风格

### 💬 多轮深度辩论

- **开场陈述**：双方清晰阐述各自立场
- **多轮交锋**：针对性回应和反驳，避免重复论点
- **总结陈词**：升华观点，展现思想深度
- **主持人点评**：客观总结辩论亮点和意义

### 🎨 精美格式输出

- **终端美化**：使用Rich库提供彩色、分栏的终端输出
- **Markdown文件**：自动保存为格式优美的Markdown文档
- **完整记录**：包含元信息、辩论内容、时间戳等

## 📋 项目价值与应用场景

- **教育启发**：模拟历史人物观点碰撞，帮助理解不同思想流派
- **创意写作**：为小说、剧本提供对话素材和灵感
- **学术研究**：快速了解不同学者在特定议题上的可能立场
- **娱乐探索**：满足好奇心，看看不同时代、领域的人物会如何辩论

## 🛠️ 安装配置

### 环境要求

- Python 3.8 或更高版本
- Anthropic API 密钥（Claude API）

### 步骤 1: 克隆或下载项目

```bash
cd ~/Desktop/debate-ai
```

### 步骤 2: 安装依赖

```bash
pip install -r requirements.txt
```

依赖包说明：
- `anthropic>=0.18.0` - Anthropic官方SDK
- `python-dotenv>=1.0.0` - 环境变量管理
- `rich>=13.0.0` - 终端美化（可选但强烈推荐）

### 步骤 3: 配置API密钥

1. 在 [Anthropic Console](https://console.anthropic.com/) 获取你的API密钥

2. 复制 `.env.example` 为 `.env`：
   ```bash
   cp .env.example .env
   ```

3. 编辑 `.env` 文件，填入你的API密钥：
   ```
   ANTHROPIC_API_KEY=sk-ant-your-actual-api-key-here
   ```

或者，直接在命令行使用 `--api-key` 参数传入。

## 🎨 辩论风格

本工具支持多种辩论风格，适应不同场景和需求：

### Academic（学术风格）- 默认

- **特点**：严谨、深入、论证充分
- **发言长度**：250-400字
- **建议轮数**：5轮
- **适用场景**：深度探讨、学术交流、哲学辩论
- **示例**：
  ```bash
  python debate.py --p1 "牛顿" --p2 "爱因斯坦" --topic "时间的本质" --style academic
  ```

### Casual-Chat（轻松对话）

- **特点**：口语化、简洁、快速来回
- **发言长度**：30-50字（1-2句话）
- **建议轮数**：10轮
- **适用场景**：快速交流、日常对话、轻松讨论
- **示例**：
  ```bash
  python debate.py --p1 "李白" --p2 "杜甫" --topic "什么是好诗" --style casual-chat --rounds 10
  ```

### Heated-Debate（激烈争论）

- **特点**：犀利、直接、针锋相对
- **发言长度**：40-60字（2-3句话）
- **建议轮数**：8轮
- **适用场景**：对立观点、激烈交锋、政治议题
- **示例**：
  ```bash
  python debate.py --p1 "马克思" --p2 "哈耶克" --topic "市场与计划" --style heated-debate
  ```

### Comedy-Duo（捧哏）

- **特点**：幽默、配合、娱乐性强
- **发言长度**：30-50字（1-2句话）
- **建议轮数**：12轮
- **模式**：**双簧式配合演绎，不是对立辩论**
- **说明**：两人配合演绎一个主题，一个"逗哏"一个"捧哏"
- **适用场景**：娱乐节目、轻松表演、创意写作
- **示例**：
  ```bash
  python debate.py --p1 "李白" --p2 "杜甫" --topic "喝酒的艺术" --style comedy-duo --rounds 12
  ```

### 风格对比

| 风格 | 长度 | 轮数 | 语气 | 模式 | 成本 |
|------|------|------|------|------|------|
| academic | 长（250-400字）| 5 | 严谨学术 | 对抗 | 较高 |
| casual-chat | 短（30-50字）| 10 | 轻松口语 | 对抗 | 较低 |
| heated-debate | 短（40-60字）| 8 | 激烈犀利 | 对抗 | 较低 |
| comedy-duo | 短（30-50字）| 12 | 幽默配合 | **合作** | 中等 |

## 🚀 使用示例

### 基础用法

```bash
python debate.py --p1 "牛顿" --p2 "莱布尼茨" --topic "微积分的发明权"
```

### 指定风格

```bash
# 轻松对话风格
python debate.py --p1 "李白" --p2 "杜甫" --topic "诗歌" --style casual-chat --rounds 10

# 激烈争论风格
python debate.py --p1 "韩非" --p2 "孟子" --topic "法治" --style heated-debate --rounds 8

# 捧哏风格（双簧配合）
python debate.py --p1 "庄子" --p2 "惠子" --topic "逍遥游" --style comedy-duo --rounds 12
```

### 西方历史人物辩论

```bash
# 物理学家：时间的本质
python debate.py --p1 "牛顿" --p2 "爱因斯坦" --topic "时间的本质"

# 哲学家：知识的来源
python debate.py --p1 "柏拉图" --p2 "亚里士多德" --topic "知识的来源"

# 经济学家：市场与政府
python debate.py --p1 "亚当·斯密" --p2 "凯恩斯" --topic "市场的自我调节能力"
```

### 中国历史人物辩论

```bash
# 先秦诸子：治国之道
python debate.py --p1 "孔子" --p2 "老子" --topic "治国之道"

# 文学大家：诗歌的最高境界
python debate.py --p1 "李白" --p2 "杜甫" --topic "什么是好诗"

# 思想家：人性本善还是本恶
python debate.py --p1 "孟子" --p2 "荀子" --topic "人性的本质"
```

### 跨文化辩论

```bash
# 东西方哲学家
python debate.py --p1 "孔子" --p2 "苏格拉底" --topic "美德的含义"

# 革命思想家
python debate.py --p1 "马克思" --p2 "孙中山" --topic "革命的道路"

# 科学与哲学
python debate.py --p1 "爱因斯坦" --p2 "维特根斯坦" --topic "科学与哲学的关系"
```

### 不同领域辩论

```bash
# 艺术形式之争
python debate.py --p1 "莎士比亚" --p2 "贝多芬" --topic "艺术的最高形式"

# 数学与物理
python debate.py --p1 "欧拉" --p2 "牛顿" --topic "数学与物理的关系"
```

### 自定义参数

```bash
# 指定辩论轮数（默认5轮）
python debate.py --p1 "孔子" --p2 "老子" --topic "道与德" --rounds 3

# 选择辩论风格
python debate.py --p1 "马克思" --p2 "哈耶克" --topic "市场与计划" --style heated

# 使用英文输出
python debate.py --p1 "Newton" --p2 "Einstein" --topic "The Nature of Time" --lang en

# 仅终端输出，不保存文件
python debate.py --p1 "李白" --p2 "杜甫" --topic "诗歌" --no-save

# 自定义输出目录
python debate.py --p1 "牛顿" --p2 "莱布尼茨" --topic "微积分" --output-dir my_debates
```

### 自定义发言长度

使用 `--word-limit` 参数可以精确控制每次发言的字数：

```bash
# 超短对话（20字）
python debate.py --p1 "李白" --p2 "杜甫" --topic "月亮" --style casual-chat --word-limit 20 --rounds 10

# 短对话（50字）
python debate.py --p1 "孔子" --p2 "老子" --topic "道" --style casual-chat --word-limit 50 --rounds 8

# 中等长度（100字）
python debate.py --p1 "苏轼" --p2 "陶渊明" --topic "隐居" --word-limit 100 --rounds 5

# 详细论述（300字）
python debate.py --p1 "康德" --p2 "黑格尔" --topic "哲学" --style academic --word-limit 300 --rounds 3
```

**说明**：
- `--word-limit` 会自动计算合适的 max_tokens（约为字数的 2.5 倍）
- 可以在任何风格下使用，会覆盖该风格的默认字数设置
- 推荐范围：20-500 字

### 完整参数说明

```
必填参数:
  --p1 <人物名称>      第一个辩论者名称
  --p2 <人物名称>      第二个辩论者名称
  --topic <话题>       辩论话题

可选参数:
  --rounds <数字>      辩论轮数（默认: 5，根据风格有不同建议）
  --style <风格>       辩论风格（默认: academic）
                       可选: academic/casual-chat/heated-debate/comedy-duo
  --word-limit <字数>  每次发言的字数限制（如: 50, 100, 300）
                       会自动调整max_tokens，覆盖风格默认设置
  --lang <语言>        输出语言：zh/en（默认: zh）
  --output-dir <目录>  输出目录（默认: outputs）
  --no-save           不保存到文件，仅终端输出
  --api-key <密钥>    Anthropic API密钥（可选，优先级高于环境变量）
```

## 💰 API成本估算

基于Claude Sonnet 4.5模型的定价（具体请查看[Anthropic定价页面](https://www.anthropic.com/pricing)）：

### Token消耗估算

一场典型的5轮辩论：

- **角色构建**（2次）：约 2,000 input + 2,000 output tokens
- **主持人开场/结尾**（2次）：约 1,000 input + 1,000 output tokens
- **开场陈述**（2次）：约 1,000 input + 1,500 output tokens
- **辩论交锋**（10次）：约 8,000 input + 6,000 output tokens
- **总结陈词**（2次）：约 2,000 input + 1,500 output tokens

**总计估算**：约 14,000 input tokens + 12,000 output tokens

### 成本估算

按Claude Sonnet 4.5的价格（假设 $3/MTok input, $15/MTok output）：

- 单次辩论成本：约 $0.04 - $0.25（取决于辩论长度和轮数）
- 100次辩论成本：约 $4 - $25

**注意**：实际成本会根据辩论复杂度、轮数、人物知名度等因素波动。

### 节省成本建议

- 减少辩论轮数（`--rounds 3`）
- 使用更便宜的模型（需修改代码中的模型名称）
- 批量生成辩论时考虑API使用限制

## ⚙️ 项目结构

```
debate-ai/
├── debate.py                    # 主程序入口
├── src/
│   ├── __init__.py
│   ├── ai_client.py            # Anthropic API封装
│   ├── character_builder.py    # 动态角色构建（核心模块）
│   ├── debate_engine.py        # 辩论逻辑控制
│   ├── prompter.py             # Prompt模板管理
│   ├── formatter.py            # 输出格式化
│   └── style_config.py         # 风格配置管理（新增）
├── outputs/                     # 生成的辩论文件目录
├── examples/                    # 示例输出
├── requirements.txt             # Python依赖包
├── .env.example                # 环境变量示例
├── README.md                   # 项目说明文档
├── QUICKSTART.md               # 快速开始指南
└── PROJECT_OVERVIEW.md         # 项目概览
```

## 🔍 工作原理

### 完整流程

1. **角色研究**（动态）
   - 接收用户输入的人物名称
   - 使用Claude AI深入研究该人物的背景、思想、风格
   - 生成详细的角色profile

2. **角色构建**（动态）
   - 将research结果转化为AI角色扮演的system prompt
   - 确保角色的一致性和真实性

3. **辩论生成**
   - 主持人开场白（介绍双方背景）
   - 双方开场陈述
   - 多轮交锋辩论（维护上下文，确保真实交锋）
   - 双方总结陈词
   - 主持人总结点评

4. **输出展示**
   - 终端实时显示（带颜色和格式）
   - 保存为Markdown文件

### 核心技术

- **零硬编码**：代码中不包含任何预设的人物信息
- **动态研究**：每个人物都是实时通过AI研究生成
- **上下文管理**：为每个角色维护独立的对话历史，确保辩论连贯性
- **Prompt工程**：精心设计的prompt模板确保高质量输出

## ⚠️ 限制与说明

### 依赖AI知识库

- 生成质量依赖于Claude AI的知识库（截止到2025年1月）
- 对于非常冷门或现代的人物，信息可能不够充分
- 虚构人物会基于其特点进行合理推断

### 历史准确性

- AI生成的内容并非100%历史准确
- 人物的观点是基于其思想体系的合理推断
- 建议将本工具用于启发和娱乐，而非学术引用

### 适用场景

✅ **推荐用于**：
- 教育启发和思想碰撞
- 创意写作和内容生成
- 了解不同思想流派
- 娱乐和探索

❌ **不建议用于**：
- 严肃的学术研究（需要引用原始文献）
- 历史考证
- 作为权威观点的来源

### API依赖

- 需要稳定的网络连接
- 需要有效的Anthropic API密钥
- 受API速率限制和配额限制

## 🎯 未来扩展可能

- [x] ~~添加更多辩论风格~~ ✅ 已实现（academic/casual-chat/heated-debate/comedy-duo）
- [x] ~~自定义发言长度~~ ✅ 已实现（--word-limit 参数）
- [ ] 支持3人或多人辩论
- [ ] 添加更多风格（诗意对话、苏格拉底式问答等）
- [ ] 提供Web界面
- [ ] 支持语音输出（TTS）
- [ ] 多语言支持扩展
- [ ] 辩论质量评分系统
- [ ] 风格混合（如：开始学术，中期激烈，结尾回归理性）
- [ ] 动态调整风格

## 📝 示例输出

生成的Markdown文件格式示例：

```markdown
# 牛顿 vs 莱布尼茨：微积分的发明权

## 辩论信息

- **辩论话题**: 微积分的发明权
- **辩论双方**: 牛顿 vs 莱布尼茨
- **生成时间**: 2025-01-31 12:00:00
- **使用模型**: claude-sonnet-4-5-20250929
- **辩论轮数**: 5

---

## 辩论实录

### 🎤 主持人

女士们，先生们，欢迎来到这场跨越时空的伟大辩论...

---

### 🔵 牛顿

我是艾萨克·牛顿，剑桥大学的卢卡斯数学教授...

---

[更多内容...]
```

完整示例请查看 `examples/` 目录。

## 🤝 贡献与反馈

欢迎提出问题、建议或贡献代码！

## 📄 许可证

本项目仅供学习和研究使用。

## 🙏 致谢

- 感谢 [Anthropic](https://www.anthropic.com/) 提供强大的Claude AI
- 感谢所有伟大的历史人物，为人类留下宝贵的思想遗产

---

**让历史人物跨越时空，在AI的世界里继续思想的交锋！** 🎭✨
