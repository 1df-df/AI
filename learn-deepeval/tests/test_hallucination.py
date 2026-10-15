"""
用 pytest + deepeval 做幻觉评测（CI / 批量跑推荐方式）

运行（在项目根目录，确保 .env 已配好 DeepSeek）：
    cd /Users/Zhuanz/Desktop/Code/AI
    /Users/Zhuanz/miniconda3/bin/python -m pytest learn-deepeval/tests/test_hallucination.py -v

LLM provider 由 .env 中的 USE_DEEPSEEK_MODEL / DEEPSEEK_API_KEY 控制。
"""

import os
from pathlib import Path

# 让 deepeval 加载项目根的 .env（pytest 从项目根运行时生效）
os.chdir(Path(__file__).resolve().parents[2])

import pytest
from deepeval import assert_test
from deepeval.metrics import HallucinationMetric
from deepeval.test_case import LLMTestCase

# 复用 src 目录下的中文 prompt 模板子类
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from hallucination_demo import ChineseHallucinationTemplate


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
    """验证模型回答不超出 context 的范围。"""
    case = LLMTestCase(
        input=input_text,
        actual_output=output,
        context=CONTEXT,
    )
    # 新版 deepeval：score 1=无幻觉，threshold 是最低通过分；用中文模板让 reason 输出中文
    metric = HallucinationMetric(
        threshold=0.8, evaluation_template=ChineseHallucinationTemplate
    )

    if expected_pass:
        assert_test(case, [metric])
    else:
        # 预期失败的用例：直接 measure，避免 assert_test 内部重复调用导致状态异常
        metric.measure(case)
        assert metric.score < metric.threshold, (
            f"case={name} 本应被判为幻觉，但 score={metric.score:.2f}"
        )
