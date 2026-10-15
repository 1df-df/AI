"""
DeepEval HallucinationMetric 最小示例

运行（在项目根目录）：
    /Users/Zhuanz/miniconda3/bin/python learn-deepeval/src/hallucination_demo.py

或激活 conda base 后：
    python learn-deepeval/src/hallucination_demo.py

需要 OPENAI_API_KEY（或其他 LLM provider key）在环境变量中。
"""

from deepeval.metrics import HallucinationMetric
from deepeval.test_case import LLMTestCase


def make_case(name: str, input_text: str, output: str, context: list[str]) -> LLMTestCase:
    return LLMTestCase(
        input=input_text,
        actual_output=output,
        retrieval_context=context,
    )


# 检索到的真实上下文（模型回答应当只基于这些内容）
context = [
    "Qoder 是一款桌面端 AI 编程助手，支持 macOS、Windows 和 Linux。",
    "Qoder 内置 MCP 协议，可连接浏览器、知识库、站点托管等外部工具。",
    "Qoder 支持 Skills 机制，用户可通过斜杠命令调用预置技能。",
]

cases = [
    # ✅ 忠实于上下文 → 不应判为幻觉
    make_case(
        name="faithful",
        input_text="Qoder 支持哪些平台？",
        output="Qoder 支持 macOS、Windows 和 Linux 三个平台。",
        context=context,
    ),
    # ❌ 编造了上下文中不存在的事实 → 应判为幻觉
    make_case(
        name="hallucinated",
        input_text="Qoder 支持哪些平台？",
        output="Qoder 支持 macOS、Windows、Linux 以及 iOS 和 Android 移动端。",
        context=context,
    ),
    # ⚠️ 部分正确 + 部分捏造
    make_case(
        name="partial",
        input_text="Qoder 有哪些核心能力？",
        output="Qoder 支持 MCP 协议、Skills 技能系统，并且自带向量数据库 RAG 引擎。",
        context=context,
    ),
]


def main() -> None:
    metric = HallucinationMetric(threshold=0.5)

    print(f"{'case':<14} {'score':>6} {'pass':>6}  reason")
    print("-" * 90)

    for case in cases:
        metric.measure(case)
        status = "✅" if case.score >= metric.threshold else "❌"
        reason = (metric.reason or "")[:60]
        print(f"{case.name:<14} {case.score:>6.2f} {status:>6}  {reason}")


if __name__ == "__main__":
    main()
