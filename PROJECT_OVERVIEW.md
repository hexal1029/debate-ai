# 项目概览

## 📁 项目结构

```
debate-ai/
├── debate.py                    # 主程序入口（可执行）
├── src/                         # 源代码目录
│   ├── __init__.py             # 包初始化文件
│   ├── ai_client.py            # Anthropic API封装
│   ├── character_builder.py    # 动态角色构建器（核心模块）
│   ├── debate_engine.py        # 辩论引擎
│   ├── prompter.py             # Prompt模板管理
│   ├── formatter.py            # 输出格式化
│   └── style_config.py         # 风格配置管理（新增）
├── outputs/                     # 输出目录（自动生成的辩论文件）
│   └── .gitkeep                # Git占位文件
├── examples/                    # 示例辩论文件
│   └── 孔子_vs_老子_治国之道_示例.md
├── requirements.txt             # Python依赖
├── .env.example                # 环境变量模板
├── .gitignore                  # Git忽略配置
├── README.md                   # 详细文档
├── QUICKSTART.md               # 快速开始指南
└── PROJECT_OVERVIEW.md         # 本文件
```

## 🔧 核心模块说明

### 1. ai_client.py - AI客户端
- 封装Anthropic Claude API调用
- 提供角色profile生成
- 管理API错误处理
- 根据风格调整system prompt

### 2. character_builder.py - 动态角色构建器 ⭐核心⭐
- **完全动态化**：不预设任何人物信息
- 使用AI研究人物背景、思想、风格
- 生成角色扮演的system prompt
- 支持任意人物名称输入
- 传递风格参数到角色设定

### 3. debate_engine.py - 辩论引擎
- 控制完整辩论流程
- 管理角色对话上下文
- 协调主持人和两位辩手
- 维护辩论历史记录
- 支持多种辩论模式（对抗/合作）
- 动态调整API参数（max_tokens、temperature）

### 4. prompter.py - Prompt管理
- 提供各阶段的prompt模板
- 支持中英文双语
- 模板化管理，便于扩展
- 支持多种风格的prompt
- 为comedy-duo提供专用方法

### 5. formatter.py - 输出格式化
- 终端美化输出（使用Rich库）
- Markdown文件生成
- 多颜色区分角色

### 6. style_config.py - 风格配置管理 ⭐新增⭐
- 使用数据类管理风格配置
- 定义四种风格的参数（max_tokens、temperature等）
- 支持自定义字数限制
- 动态计算max_tokens

## 🎯 核心特性

### ✨ 完全动态化
- 零硬编码人物信息
- 一切基于AI实时生成
- 支持任意历史人物

### 🧠 深度角色构建
- AI驱动的人物研究
- 真实的思想体系还原
- 个性化的表达风格

### 💬 真实辩论交锋
- 多轮深度对话
- 针对性回应反驳
- 避免重复论点

### 🎨 多种辩论风格
- **Academic**（学术）：深度、严谨、250-400字
- **Casual-Chat**（轻松对话）：简短、口语、30-50字
- **Heated-Debate**（激烈争论）：犀利、直接、40-60字
- **Comedy-Duo**（捧哏）：幽默、配合、双簧式演绎

### 🎛️ 灵活参数控制
- 自定义发言长度（--word-limit）
- 自定义轮数（--rounds）
- 动态调整max_tokens和temperature
- 支持中英文输出

## 📊 技术架构

```
用户输入 (人物名称 + 话题)
    ↓
AI研究角色 (并行构建两个角色)
    ↓
生成System Prompt
    ↓
辩论引擎执行流程
    ├── 主持人开场
    ├── 角色1开场
    ├── 角色2开场
    ├── 多轮交锋
    ├── 角色1总结
    ├── 角色2总结
    └── 主持人总结
    ↓
格式化输出 (终端 + Markdown文件)
```

## 🚀 使用流程

1. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

2. **配置API密钥**
   ```bash
   cp .env.example .env
   # 编辑 .env，填入 ANTHROPIC_API_KEY
   ```

3. **运行辩论**
   ```bash
   python debate.py --p1 "人物1" --p2 "人物2" --topic "话题"
   ```

4. **查看输出**
   - 终端：实时彩色输出
   - 文件：`outputs/` 目录下的 `.md` 文件

## 💡 设计原则

1. **零硬编码**：不预设任何人物信息
2. **完全动态**：一切基于AI实时生成
3. **高质量角色**：深入准确的角色构建
4. **真实交锋**：有实质性的论点碰撞
5. **可扩展性**：便于未来功能扩展

## 📝 代码质量

- ✅ 清晰的模块划分
- ✅ Python类型提示
- ✅ 详细的文档字符串
- ✅ 完整的错误处理
- ✅ 遵循PEP 8规范

## 🔄 扩展方向

- [x] ~~添加更多辩论风格~~ ✅ 已实现
- [x] ~~自定义发言长度~~ ✅ 已实现
- [ ] 支持3人或多人辩论
- [ ] 添加更多风格（诗意对话、苏格拉底式等）
- [ ] Web界面
- [ ] 语音输出（TTS）
- [ ] 自定义角色设定
- [ ] 辩论质量评分
- [ ] 风格混合和动态切换

## 📚 相关文档

- **快速开始**：查看 `QUICKSTART.md`
- **详细文档**：查看 `README.md`
- **示例输出**：查看 `examples/` 目录

## 🎓 学习资源

- [Anthropic API文档](https://docs.anthropic.com/)
- [Claude API定价](https://www.anthropic.com/pricing)
- [Rich库文档](https://rich.readthedocs.io/)

---

**项目状态**：✅ 完整可运行，已测试通过

**建议第一次测试**：

1. **学术风格**（传统深度辩论）：
```bash
python debate.py --p1 "孔子" --p2 "老子" --topic "治国之道" --rounds 3
```

2. **轻松对话**（快速简短）：
```bash
python debate.py --p1 "李白" --p2 "杜甫" --topic "诗" --style casual-chat --rounds 6
```

3. **捧哏风格**（双簧配合，最有特色）：
```bash
python debate.py --p1 "庄子" --p2 "惠子" --topic "逍遥游" --style comedy-duo --rounds 5
```

这些测试将展示系统的多样化能力！
