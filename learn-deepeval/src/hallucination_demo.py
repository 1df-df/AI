"""
DeepEval HallucinationMetric 最小示例

运行（在项目根目录，确保 .env 已配好 DeepSeek）：
    /Users/Zhuanz/miniconda3/bin/python learn-deepeval/src/hallucination_demo.py

或激活 conda base 后：
    python learn-deepeval/src/hallucination_demo.py

LLM provider 由 .env 中的 USE_DEEPSEEK_MODEL / DEEPSEEK_API_KEY 控制。
"""

import os
from pathlib import Path
from typing import List

# 让 deepeval 加载项目根的 .env
os.chdir(Path(__file__).resolve().parents[2])

from deepeval.metrics import HallucinationMetric
from deepeval.metrics.hallucination.hallucination import HallucinationTemplate
from deepeval.test_case import LLMTestCase


class ChineseHallucinationTemplate(HallucinationTemplate):
    """覆盖默认英文 prompt，让 judge 模型用中文输出 reason。"""

    @staticmethod
    def generate_verdicts(
        contexts: List[str], actual_output: str, contexts_count: int
    ) -> str:
        return f"""对 contexts（字符串列表）中的每一条上下文，判断给定的 'actual output' 是否与之一致，输出一组 JSON 对象，每个包含 'verdict' 和 'reason' 两个字段。

'verdict' 字段的值必须严格为 'yes' 或 'no'，表示文本是否与该条上下文一致。
'reason' 字段用**中文**给出判定理由；当 verdict 为 'no' 时，请在 reason 中给出纠正说明。

**
重要：请只返回 JSON 格式，顶层 key 为 'verdicts'，值为 JSON 对象列表。
示例 contexts：["爱因斯坦因发现光电效应获得诺贝尔奖。", "爱因斯坦于 1968 年获得诺贝尔奖。"]
示例 actual output："爱因斯坦在 1969 年因发现光电效应获得诺贝尔奖。"

示例：
{{
  "verdicts": [
    {{
      "reason": "实际输出与提供的上下文一致，上下文明确指出爱因斯坦因发现光电效应获得诺贝尔奖。",
      "verdict": "yes"
    }},
    {{
      "reason": "实际输出与提供的上下文矛盾，上下文说的是 1968 年而非 1969 年。",
      "verdict": "no"
    }}
  ]
}}

请不要使用任何先验知识，仅依据每条上下文本身进行判断。由于要为每条上下文生成一个 verdict，'verdicts' 的数量必须严格等于 {contexts_count}。

判定规则（按优先级）：
1. **矛盾 → no**：actual output 与上下文直接冲突（数字、名称、属性不一致）。
2. **无中生有 → no**：actual output 引入了上下文中**完全不存在的新事实**（新的平台、功能、组件、产品等），即便与上下文不直接矛盾，也应判 no，因为这类信息无法由上下文支撑。
3. **缺少细节 → yes**：actual output 只是没有提及某条上下文的内容，并未与之冲突或添加新事实，应判 yes（宽容处理）。
**

Contexts:
{contexts}

Actual Output:
{actual_output}

JSON:
"""

    @staticmethod
    def generate_reason(
        factual_alignments: List[str],
        contradictions: List[str],
        score: str,
    ) -> str:
        return f"""给定一组事实一致项（factual alignments）和矛盾项（contradictions），它们标明了 `actual output` 与 `contexts` 之间的吻合/冲突情况，请据此**用中文**简明扼要地解释幻觉得分的原因。注意幻觉得分范围为 0~1，衡量 `actual output` 与 `contexts` 的吻合程度，越高越好。

**
重要：请只返回 JSON 格式，顶层 key 为 'reason'，值用中文书写。
示例 JSON：
{{
  "reason": "得分 <hallucination_score> 的原因是 <你的中文解释>。"
}}
**

Factual Alignments:
{factual_alignments}

Contradictions:
{contradictions}

Hallucination Score:
{score}

JSON:
"""


def make_case(input_text: str, output: str, context: list[str]) -> LLMTestCase:
    return LLMTestCase(
        input=input_text,
        actual_output=output,
        context=context,
    )


# 检索到的真实上下文（模型回答应当只基于这些内容）
context = [
    "Qoder 是一款桌面端 AI 编程助手，支持 macOS、Windows 和 Linux。",
    "Qoder 内置 MCP 协议，可连接浏览器、知识库、站点托管等外部工具。",
    "Qoder 支持 Skills 机制，用户可通过斜杠命令调用预置技能。",
]

cases = [
    # ✅ 忠实于上下文 → 不应判为幻觉
    (
        "faithful",
        make_case(
            input_text="Qoder 支持哪些平台？",
            output="Qoder 支持 macOS、Windows 和 Linux 三个平台。",
            context=context,
        ),
    ),
    # ❌ 编造了上下文中不存在的事实 → 应判为幻觉
    (
        "hallucinated",
        make_case(
            input_text="Qoder 支持哪些平台？",
            output="Qoder 支持 macOS、Windows、Linux 以及 iOS 和 Android 移动端。",
            context=context,
        ),
    ),
    # ⚠️ 部分正确 + 部分捏造
    (
        "partial",
        make_case(
            input_text="Qoder 有哪些核心能力？",
            output="Qoder 支持 MCP 协议、Skills 技能系统，并且自带向量数据库 RAG 引擎。",
            context=context,
        ),
    ),
]


def main() -> None:
    # 新版 deepeval：score 1=无幻觉（通过），0=有幻觉；threshold 是最低通过分
    # evaluation_template 传入中文模板子类，让 judge 用中文输出 reason
    metric = HallucinationMetric(
        threshold=0.8, evaluation_template=ChineseHallucinationTemplate
    )

    print(f"{'case':<14} {'score':>6} {'pass':>6}  reason")
    print("-" * 90)

    for name, case in cases:
        metric.measure(case)
        status = "✅" if metric.score >= metric.threshold else "❌"
        reason = (metric.reason or "")[:60]
        print(f"{name:<14} {metric.score:>6.2f} {status:>6}  {reason}")


if __name__ == "__main__":
    main()
