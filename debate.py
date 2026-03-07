#!/usr/bin/env python3
"""
AI历史人物辩论生成器 - 主程序入口
支持任意历史人物的动态辩论生成

使用示例:
    python debate.py --p1 "牛顿" --p2 "莱布尼茨" --topic "微积分的发明权"
    python debate.py --p1 "孔子" --p2 "老子" --topic "治国之道" --rounds 3
"""

import argparse
import sys
import os
from dotenv import load_dotenv

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.ai_client import AIClient
from src.character_builder import CharacterBuilder
from src.debate_engine import DebateEngine
from src.formatter import DebateFormatter
from src.cache_manager import CharacterCacheManager


def parse_arguments():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="AI历史人物辩论生成器 - 支持任意历史人物的动态辩论",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  python debate.py --p1 "牛顿" --p2 "爱因斯坦" --topic "时间的本质"
  python debate.py --p1 "孔子" --p2 "老子" --topic "治国之道" --rounds 3
  python debate.py --p1 "马克思" --p2 "哈耶克" --topic "市场与计划" --lang en
        """
    )

    # 必填参数
    parser.add_argument(
        "--p1",
        required=True,
        help="第一个辩论者名称（必填）"
    )
    parser.add_argument(
        "--p2",
        required=True,
        help="第二个辩论者名称（必填）"
    )
    parser.add_argument(
        "--topic",
        required=True,
        help="辩论话题（必填）"
    )

    # 可选参数
    parser.add_argument(
        "--rounds",
        type=int,
        default=5,
        help="辩论轮数（默认: 5）"
    )
    parser.add_argument(
        "--style",
        choices=["academic", "casual-chat", "heated-debate", "comedy-duo"],
        default="academic",
        help="辩论风格：academic(学术)/casual-chat(轻松对话)/heated-debate(激烈争论)/comedy-duo(捧哏)"
    )
    parser.add_argument(
        "--lang",
        choices=["zh", "en"],
        default="zh",
        help="输出语言（默认: zh 中文）"
    )
    parser.add_argument(
        "--output-dir",
        default="outputs",
        help="输出目录（默认: outputs）"
    )
    parser.add_argument(
        "--no-save",
        action="store_true",
        help="不保存到文件，仅终端输出"
    )
    parser.add_argument(
        "--api-key",
        help="Anthropic API密钥（可选，也可通过环境变量ANTHROPIC_API_KEY设置）"
    )
    parser.add_argument(
        "--word-limit",
        type=int,
        help="每次发言的字数限制（如: 50, 100, 300），会自动调整max_tokens"
    )
    parser.add_argument(
        "--language-style",
        choices=["文言", "半文半白", "现代口语"],
        default="现代口语",
        help="语言风格（默认: 现代口语）。文言=完全古文；半文半白=文言+现代；现代口语=现代汉语但保持人物特点"
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="禁用角色缓存，强制重新研究角色（默认: 启用缓存）"
    )
    parser.add_argument(
        "--clear-cache",
        metavar="CHARACTER",
        help="清除指定角色的缓存，然后退出。格式: \"角色名称\" 或 \"角色名称:语言\" (如: \"孔子:zh\")"
    )

    return parser.parse_args()


def main():
    """主函数"""
    # 加载环境变量
    load_dotenv()

    # 解析参数
    args = parse_arguments()

    # Handle --clear-cache flag (exit after clearing)
    if args.clear_cache:
        cache_manager = CharacterCacheManager()

        # Parse character name and language
        if ":" in args.clear_cache:
            character_name, language = args.clear_cache.split(":", 1)
        else:
            # Default to both languages
            character_name = args.clear_cache
            language = None

        if language:
            # Clear specific language
            if cache_manager.invalidate(character_name, language):
                print(f"✓ 已清除缓存: {character_name} ({language})")
            else:
                print(f"✗ 未找到缓存: {character_name} ({language})")
        else:
            # Clear both languages
            cleared_zh = cache_manager.invalidate(character_name, "zh")
            cleared_en = cache_manager.invalidate(character_name, "en")

            if cleared_zh or cleared_en:
                langs_cleared = []
                if cleared_zh:
                    langs_cleared.append("zh")
                if cleared_en:
                    langs_cleared.append("en")
                print(f"✓ 已清除缓存: {character_name} ({', '.join(langs_cleared)})")
            else:
                print(f"✗ 未找到缓存: {character_name}")

        sys.exit(0)

    # 打印欢迎信息
    print("\n" + "=" * 70)
    print("🎭 AI历史人物辩论生成器")
    print("=" * 70)
    print(f"\n辩论话题: {args.topic}")
    print(f"辩论双方: {args.p1} vs {args.p2}")
    print(f"辩论轮数: {args.rounds}")
    print(f"辩论风格: {args.style}")
    print(f"输出语言: {'中文' if args.lang == 'zh' else 'English'}")
    print(f"语言风格: {args.language_style}")

    # 显示风格特点和建议
    from src.style_config import get_style_config, create_custom_style_config

    # 如果用户指定了字数限制，使用自定义配置
    if args.word_limit:
        style_config = create_custom_style_config(args.style, args.word_limit)
        print(f"风格特点: {style_config.tone_description}")
        print(f"自定义字数限制: {args.word_limit}字 (max_tokens: {style_config.max_tokens})")
    else:
        style_config = get_style_config(args.style)
        print(f"风格特点: {style_config.tone_description}")
        print(f"默认字数限制: {style_config.word_limit}")

    if args.rounds != style_config.default_rounds:
        print(f"建议轮数: {style_config.default_rounds} (当前: {args.rounds})")

    print("\n" + "=" * 70 + "\n")

    try:
        # 1. 初始化AI客户端
        print("[1/7] 初始化AI客户端...")
        ai_client = AIClient(api_key=args.api_key)

        # 2. 构建角色
        character_builder = CharacterBuilder(
            ai_client,
            language=args.lang,
            use_cache=not args.no_cache  # Enable cache unless --no-cache flag is set
        )

        print(f"[2/7] 正在研究 {args.p1} 的背景和思想...")
        character1 = character_builder.build_character(args.p1, args.topic, style=args.style, language_style=args.language_style)

        print(f"[3/7] 正在研究 {args.p2} 的背景和思想...")
        character2 = character_builder.build_character(args.p2, args.topic, style=args.style, language_style=args.language_style)

        # 3. 创建辩论引擎（传递自定义配置如果有的话）
        debate_engine = DebateEngine(
            ai_client=ai_client,
            character1=character1,
            character2=character2,
            topic=args.topic,
            language=args.lang,
            rounds=args.rounds,
            style=args.style,
            style_config=style_config if args.word_limit else None
        )

        # 4. 运行辩论
        formatter = DebateFormatter(use_rich=True)

        def progress_callback(msg):
            formatter.print_progress(msg)

        print("\n" + "=" * 70)
        print("开始生成辩论...")
        print("=" * 70 + "\n")

        messages = debate_engine.run_debate(progress_callback=progress_callback)

        # 5. 输出辩论内容到终端
        print("\n" + "=" * 70)
        print("辩论完整内容")
        print("=" * 70 + "\n")

        for message in messages:
            formatter.print_message(message)

        # 6. 保存到文件（如果需要）
        if not args.no_save:
            print("=" * 70)
            print("正在保存辩论到文件...")

            metadata = {
                "model": ai_client.model,
                "rounds": args.rounds,
                "style": args.style,
                "language": args.lang
            }

            filepath = formatter.save_to_file(
                messages=messages,
                character1_name=args.p1,
                character2_name=args.p2,
                topic=args.topic,
                output_dir=args.output_dir,
                metadata=metadata
            )

            print(f"✅ 辩论已保存到: {filepath}")
            print("=" * 70 + "\n")

        # 7. 完成
        print("\n🎉 辩论生成完成！\n")

    except ValueError as e:
        print(f"\n❌ 配置错误: {e}")
        print("\n请确保已设置ANTHROPIC_API_KEY环境变量，或使用--api-key参数提供API密钥。")
        print("详情请参考README.md中的配置说明。\n")
        sys.exit(1)

    except Exception as e:
        print(f"\n❌ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
