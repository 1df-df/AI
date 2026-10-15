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
# 使用 conda base（Python 3.13）
/Users/Zhuanz/miniconda3/bin/python -m pip install -U deepeval
```

### DeepSeek 配置

1. 复制模板：`cp .env.example .env`（`.env` 已被 gitignore）
2. 编辑 `.env`，填入 `DEEPSEEK_API_KEY`
3. 验证接入：`/Users/Zhuanz/miniconda3/bin/python learn-deepeval/src/verify_deepseek.py`

deepeval 会自动读取项目根目录的 `.env`，无需手动 export。
