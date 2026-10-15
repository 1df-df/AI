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

（待补充）

## 环境

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U deepeval
```

需要配置模型 API Key（如 `OPENAI_API_KEY`），放在仓库根目录 `.env`（已被 gitignore）。
