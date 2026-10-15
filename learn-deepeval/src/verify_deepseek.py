"""
验证 DeepSeek 接入是否成功。

运行（在项目根目录，确保 .env 已填好）：
    /Users/Zhuanz/miniconda3/bin/python learn-deepeval/src/verify_deepseek.py
"""

import os
from pathlib import Path

# 让 deepeval 加载项目根的 .env
os.chdir(Path(__file__).resolve().parents[2])

from deepeval.models.llms.deepseek_model import DeepSeekModel


def main() -> None:
    print(f"cwd: {Path.cwd()}")
    print(f".env exists: {(Path.cwd() / '.env').exists()}")

    model = DeepSeekModel()
    print(f"model: {model.get_model_name()}")
    print(f"base_url: {model.base_url}")

    prompt = "用一句话介绍你自己。"
    print(f"\nprompt: {prompt}")
    output, cost = model.generate(prompt)
    print(f"output: {output}")
    print(f"cost: {cost}")
    print("\n✅ DeepSeek 接入成功！")


if __name__ == "__main__":
    main()
