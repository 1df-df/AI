"""
用 pytest + deepeval 做幻觉评测（CI / 批量跑推荐方式）

运行：
    cd /Users/Zhuanz/Desktop/Code/AI
    /Users/Zhuanz/miniconda3/bin/python -m pytest learn-deepeval/tests/test_hallucination.py -v
"""

import pytest
from deepeval import assert_test
from deepeval.metrics import HallucinationMetric
from deepeval.test_case import LLMTestCase


CONTEXT = [
    "Qoder 是一款桌面端 AI 编程助手，支持 macOS、Windows 和 Linux。",
    "Qoder 内置 MCP 协议，可连接浏览器、知识库、站点托管等外部工具。",
    "Qoder 支持 Skills 机制，用户可通过斜杠命令调用预置技能。",
]


@pytest.mark.parametrize(
    "name,input_text,output,expected_pass",
    [
        (
            "faithful",
            "Qoder 支持哪些平台？",
            "Qoder 支持 macOS、Windows 和 Linux 三个平台。",
            True,
        ),
        (
            "hallucinated",
            "Qoder 支持哪些平台？",
            "Qoder 支持 macOS、Windows、Linux 以及 iOS 和 Android 移动端。",
            False,
        ),
        (
            "partial",
            "Qoder 有哪些核心能力？",
            "Qoder 支持 MCP 协议、Skills 技能系统，并且自带向量数据库 RAG 引擎。",
            False,
        ),
    ],
    ids=["faithful", "hallucinated", "partial"],
)
def test_no_hallucination(name, input_text, output, expected_pass):
    """验证模型回答不超出 retrieval_context 的范围。"""
    case = LLMTestCase(
        input=input_text,
        actual_output=output,
        retrieval_context=CONTEXT,
    )
    metric = HallucinationMetric(threshold=0.5)

    if expected_pass:
        assert_test(case, [metric])
    else:
        # 预期会失败的用例：确认 metric 确实能抓到幻觉
        metric.measure(case)
        assert case.score < metric.threshold, (
            f"case={name} 本应被判为幻觉，但 score={case.score:.2f}"
        )
