#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
产品可行性分析 Agent - 命令行入口

Usage:
    python cli.py --file product_info.txt
    python cli.py --text "产品名称：AI智能陪伴机器人..."
    python cli.py --interactive
"""

import argparse
import json
import os
import sys
from pathlib import Path

# 添加 tools 到路径
sys.path.insert(0, str(Path(__file__).parent / "tools"))

from feasibility_agent import FeasibilityAgent


def print_banner():
    print("=" * 60)
    print("产品可行性分析 Agent v3.0")
    print("募资平台可行性分析工具")
    print("=" * 60)
    print()


def analyze_from_text(text: str, llm_provider: str = "auto") -> dict:
    """从文本运行分析"""
    agent = FeasibilityAgent(llm_provider=llm_provider)
    report = agent.process_from_raw(text)
    return report


def analyze_from_file(filepath: str, llm_provider: str = "auto") -> dict:
    """从文件运行分析（支持 txt、pdf）"""
    path = Path(filepath)
    ext = path.suffix.lower()

    if ext == '.pdf':
        # PDF文件：用pdfplumber提取文字
        try:
            import pdfplumber
        except ImportError:
            print("错误：读取PDF需要安装 pdfplumber，请运行：pip install pdfplumber")
            sys.exit(1)
        text_parts = []
        try:
            with pdfplumber.open(filepath) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text_parts.append(page_text)
        except Exception as e:
            print(f"错误：无法读取PDF文件: {e}")
            sys.exit(1)
        text = '\n\n'.join(text_parts)
        if not text.strip():
            print("错误：PDF中没有提取到文字内容")
            sys.exit(1)
        print(f"已从PDF提取 {len(text)} 字符")
    elif ext in ('.txt', '.md', '.text'):
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
    else:
        # 尝试作为文本文件读取
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
        except UnicodeDecodeError:
            print(f"错误：无法读取文件 {filepath}（不支持的格式）")
            print("支持格式：.txt .md .pdf")
            sys.exit(1)

    return analyze_from_text(text, llm_provider)


def interactive_mode(llm_provider: str = "auto"):
    """交互模式"""
    print_banner()
    print("交互模式：请粘贴项目资料（产品介绍、目标用户、商业模式等）")
    print("输入完成后，请单独输入一行 END 结束：")
    print("-" * 40)

    lines = []
    while True:
        try:
            line = input()
            if line.strip().upper() == "END":
                break
            lines.append(line)
        except EOFError:
            break

    text = "\n".join(lines)
    if not text.strip():
        print("错误：未输入任何内容")
        return

    print("\n正在分析，请稍候...")
    report = analyze_from_text(text, llm_provider)
    print_results(report)


def print_results(report: dict):
    """打印分析结果"""
    scoring = report.get('scoring', {})
    product = report.get('product', {})
    saved = report.get('saved_files', {})

    print("\n" + "=" * 60)
    print("分析完成！")
    print("=" * 60)

    print(f"\n📦 产品名称: {product.get('name', '未命名')}")
    print(f"🏷️  识别品类: {report.get('category', '未知')}")
    print(f"📊 可行性评分: {scoring.get('total_score', 0)}/100")
    print(f"🎯 评级: {scoring.get('grade', '?')} - {scoring.get('rating', '未知')}")
    print(f"💡 建议: {scoring.get('recommendation', '无')}")

    strengths = scoring.get('strengths', [])
    weaknesses = scoring.get('weaknesses', [])

    if strengths:
        print(f"\n✅ 优势: {', '.join(strengths[:3])}")
    if weaknesses:
        print(f"⚠️  短板: {', '.join(weaknesses[:3])}")

    print(f"\n📁 报告已保存:")
    if saved.get('json_report'):
        print(f"   JSON: {saved['json_report']}")
    if saved.get('markdown_report'):
        print(f"   Markdown: {saved['markdown_report']}")
    if saved.get('html_report'):
        print(f"   HTML: {saved['html_report']}")
    if saved.get('pdf_report'):
        print(f"   PDF: {saved['pdf_report']}")

    print("\n" + "=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="产品可行性分析 Agent - 判断任何产品/项目是否可行",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python cli.py --file product_info.txt
  python cli.py --text "产品名称：AI陪伴机器人，目标用户：独居老人..."
  python cli.py --interactive
  python cli.py --file info.txt --llm deepseek
        """
    )

    parser.add_argument("--file", "-f", help="从文件读取产品资料")
    parser.add_argument("--text", "-t", help="直接从命令行传入产品资料")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互模式")
    parser.add_argument("--llm", "-l", default="auto",
                        choices=["auto", "openai", "claude", "deepseek", "qwen", "local"],
                        help="选择LLM提供商 (默认: auto)")
    parser.add_argument("--version", "-v", action="version", version="%(prog)s 2.0")

    args = parser.parse_args()

    if args.file:
        print_banner()
        print(f"正在从文件分析: {args.file}")
        report = analyze_from_file(args.file, args.llm)
        print_results(report)
    elif args.text:
        print_banner()
        print("正在分析文本...")
        report = analyze_from_text(args.text, args.llm)
        print_results(report)
    elif args.interactive:
        interactive_mode(args.llm)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
