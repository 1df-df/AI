# DeepEval 学习笔记

> 分支：`deepeval` · 状态：进行中

## 目录

```
learn-deepeval/
├── README.md      # 本文件：笔记与进度
├── src/           # 实践代码
└── tests/         # 评测用例（pytest + deepeval）
```

> ⚠️ 目录名用 `learn-deepeval` 而不是 `deepeval`，避免与 Python 包 `deepeval` 同名导致 import 失败。

## 学习清单

- [x] 安装与环境搭建（conda base + `pip install -U deepeval`）
- [ ] 核心概念：LLMTestCase、metric、dataset、evaluation
- [x] 内置指标：HallucinationMetric（见 `src/hallucination_demo.py`）
- [ ] 自定义指标（Custom Metric）
- [ ] 数据集管理与批量评测（`EvaluationDataset` / `evaluate()`）
- [x] Pytest 集成（见 `tests/test_hallucination.py`）
- [ ] CI 集成

## 已完成的示例

| 文件 | 说明 |
| --- | --- |
| `src/hallucination_demo.py` | HallucinationMetric 最小可跑 demo，3 条用例对比忠实/幻觉/部分捏造 |
| `tests/test_hallucination.py` | pytest + assert_test 写法，可直接接入 CI |

## 笔记

### 新版 deepeval API 变化（2026-10）

- `LLMTestCase` 字段：幻觉评测用 `context`（不再是 `retrieval_context`）；`context` 为 None 会抛 `MissingTestCaseParamsError`
- 评分方向反转：score 1 = 通过、0 = 失败，threshold 是**最低通过分**。旧版 threshold=0.5 现在应写 0.8
- `.score` 在 `metric` 对象上读取，不在 `case` 上
- `LLMTestCase` 没有 `name` 字段，用例标签需用外部配对管理
- 未注册模型（如 `deepseek-flash`）不会报错，但必须手动设 `DEEPSEEK_COST_PER_INPUT_TOKEN` / `DEEPSEEK_COST_PER_OUTPUT_TOKEN`，否则 cost=None

### 中文 reason 输出

默认 prompt 是英文，judge 返回的 `reason` 也是英文。要中文化需子类化 `HallucinationTemplate`，覆盖 `generate_verdicts` 和 `generate_reason` 两个静态方法，再通过 `HallucinationMetric(evaluation_template=...)` 传入。见 `src/hallucination_demo.py::ChineseHallucinationTemplate`。

### LLM judge 的非确定性 ⚠️

同一用例多次运行分数可能不同（实测 faithful 用例 demo 跑 1.00、pytest 跑 0.33）。原因：
- DeepSeek 等生成式 judge 本身有随机性（即使 temperature=0 也可能漂移）
- `assert_test` 内部走 async 路径，与直接 `metric.measure()` 行为略有差异

应对：
- CI 里对关键用例设置重试或取 N 次平均分
- prompt 设计要明确"缺少细节 → yes"的宽容规则，减少边界 case 的抖动
- 不要期望单次评测分数绝对稳定，趋势比单点更重要

## 环境

```bash
# 使用 conda base（Python 3.13）
/Users/Zhuanz/miniconda3/bin/python -m pip install -U deepeval
```

### DeepSeek 配置

1. 复制模板：`cp .env.example .env`（`.env` 已被 gitignore）
2. 编辑 `.env`，填入 `DEEPSEEK_API_KEY`
3. 验证接入：`/Users/Zhuanz/miniconda3/bin/python learn-deepeval/src/verify_deepseek.py`

deepeval 会自动读取项目根目录的 `.env`，无需手动 export。
