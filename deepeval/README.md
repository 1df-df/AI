# DeepEval 学习笔记

> 分支：`deepeval` · 状态：进行中

## 目录

```
deepeval/
├── README.md      # 本文件：笔记与进度
├── src/           # 实践代码
├── tests/         # 评测用例
└── data/          # 示例数据
```

## 学习清单

- [ ] 安装与环境搭建（`pip install -U deepeval`）
- [ ] 核心概念：LLMTestCase、metric、dataset、evaluation
- [ ] 内置指标：G-Eval、Answer Relevancy、Faithfulness、Hallucination 等
- [ ] 自定义指标（Custom Metric）
- [ ] 数据集管理与批量评测（`EvaluationDataset` / `evaluate()`）
- [ ] Pytest 集成
- [ ] CI 集成

## 笔记

（待补充）

## 环境

```bash
python -m venv .venv
source .venv/bin/activate
pip install -U deepeval
```

需要配置模型 API Key（如 `OPENAI_API_KEY`），放在仓库根目录 `.env`（已被 gitignore）。
