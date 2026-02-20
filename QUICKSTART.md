# 快速开始指南

## 三步快速体验

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置API密钥

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填入你的API密钥
# ANTHROPIC_API_KEY=sk-ant-your-actual-api-key
```

获取API密钥：访问 https://console.anthropic.com/

### 3. 运行第一场辩论

```bash
python debate.py --p1 "孔子" --p2 "老子" --topic "治国之道"
```

## 常用命令示例

### 基础用法

```bash
# 默认学术风格
python3 debate.py --p1 "牛顿" --p2 "爱因斯坦" --topic "时间的本质"

# 中国历史人物
python3 debate.py --p1 "李白" --p2 "杜甫" --topic "什么是好诗"

# 跨文化辩论
python3 debate.py --p1 "孔子" --p2 "苏格拉底" --topic "美德的含义"
```

### 不同风格

```bash
# 轻松对话（短而快）
python3 debate.py --p1 "李白" --p2 "杜甫" --topic "诗" --style casual-chat --rounds 10

# 激烈争论（犀利直接）
python3 debate.py --p1 "马克思" --p2 "哈耶克" --topic "市场与计划" --style heated-debate --rounds 8

# 捧哏（双簧配合）
python3 debate.py --p1 "庄子" --p2 "惠子" --topic "逍遥游" --style comedy-duo --rounds 12
```

### 自定义长度

```bash
# 超短对话（20字）
python3 debate.py --p1 "孔子" --p2 "老子" --topic "道" --word-limit 20 --rounds 10

# 中等长度（100字）
python3 debate.py --p1 "苏轼" --p2 "陶渊明" --topic "隐居" --word-limit 100 --rounds 5

# 详细论述（300字）
python3 debate.py --p1 "康德" --p2 "黑格尔" --topic "哲学" --word-limit 300 --rounds 3
```

### 其他选项

```bash
# 英文输出
python3 debate.py --p1 "Newton" --p2 "Einstein" --topic "Time" --lang en

# 不保存文件
python3 debate.py --p1 "李白" --p2 "杜甫" --topic "诗" --no-save
```

## 输出位置

- **终端**：实时显示带颜色的辩论内容
- **文件**：自动保存在 `outputs/` 目录，格式为Markdown

## 风格选择指南

| 需求 | 推荐风格 | 示例命令 |
|------|---------|---------|
| 深度哲学讨论 | academic | `--style academic --rounds 5` |
| 快速问答 | casual-chat | `--style casual-chat --rounds 10` |
| 政治议题争论 | heated-debate | `--style heated-debate --rounds 8` |
| 娱乐节目 | comedy-duo | `--style comedy-duo --rounds 12` |
| 超短对话 | 任意 + word-limit | `--word-limit 20 --rounds 10` |

## 常见问题

### Q: API密钥配置失败？
A: 确保在 `.env` 文件中正确填写了 `ANTHROPIC_API_KEY`，或使用 `--api-key` 参数传入。

### Q: 安装rich库失败？
A: rich库是可选的，用于美化终端输出。如果安装失败，程序仍可运行，只是输出效果简单些。

### Q: 如何查看生成的辩论文件？
A: 查看 `outputs/` 目录，使用任何Markdown阅读器打开 `.md` 文件。

### Q: 如何选择合适的风格？
A:
- **学术讨论** → academic（深度、严谨）
- **日常聊天** → casual-chat（轻松、简短）
- **辩论赛** → heated-debate（激烈、犀利）
- **娱乐节目** → comedy-duo（幽默、配合）

### Q: comedy-duo 和其他风格有什么区别？
A: comedy-duo 是**配合演绎**而非对立辩论，两人像相声一样配合表演，而不是互相反驳。

### Q: 如何控制发言长度？
A: 使用 `--word-limit` 参数：
- 超短：`--word-limit 20`
- 短：`--word-limit 50`
- 中等：`--word-limit 100`
- 长：`--word-limit 300`

### Q: 如何节省API成本？
A:
- 使用短对话风格：`--style casual-chat`
- 减少辩论轮数：`--rounds 3`
- 限制字数：`--word-limit 50`
- 先用短话题测试

## 更多信息

详细文档请查看 [README.md](README.md)

## 示例输出

查看 `examples/` 目录中的示例辩论文件。
