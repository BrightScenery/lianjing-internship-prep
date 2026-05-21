"""
System Prompt vs User Prompt 对比实验
目标：验证不同的 System Prompt 对模型回答风格的影响
实验日期：2026-05-21
"""

import os
from dotenv import load_dotenv
import dashscope
from dashscope import Generation

# 加载 .env 文件
load_dotenv()
dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")


# ==================== 实验配置 ====================
# 同一个问题，不同的 System Prompt
experiments = [
    {
        "name": "实验1：无 System Prompt（基线对照）",
        "system": None,  # 不设置 system
        "user": "解释一下什么是 Docker",
    },
    {
        "name": "实验2：老师人设",
        "system": "你是一个耐心的老师，擅长用生活中的例子解释技术概念。说话语气亲切，喜欢用比喻。",
        "user": "解释一下什么是 Docker",
    },
    {
        "name": "实验3：面试官人设",
        "system": "你是一个严格的技术面试官。回答要简洁专业，每次回答结束后追问一个思考题让候选人思考。",
        "user": "解释一下什么是 Docker",
    },
    {
        "name": "实验4：极端格式约束",
        "system": "你只能用 3 句话回答，每句话不超过 20 个字。不要多于一句，不要少于一句。",
        "user": "解释一下什么是 Docker",
    },
]


# ==================== 调用函数 ====================
def call_qwen(messages):
    """调用通义千问 API，返回文本"""
    response = Generation.call(
        model="qwen-plus",
        messages=messages,
    )
    if response.status_code == 200:
        return response.output.text, response.usage.total_tokens
    else:
        return f"调用失败: {response.message}", 0


# ==================== 主程序 ====================
if __name__ == "__main__":
    print("=" * 60)
    print("System Prompt vs User Prompt 对比实验")
    print("=" * 60)

    total_tokens = 0

    for exp in experiments:
        print(f"\n{'=' * 60}")
        print(f"【{exp['name']}】")
        print(f"{'=' * 60}")

        # 构造 messages —— 注意：如果 system 为 None，就不加 system 消息
        messages = []
        if exp["system"]:
            messages.append({"role": "system", "content": exp["system"]})
        messages.append({"role": "user", "content": exp["user"]})

        # 打印本次的 prompt 配置
        print(f"\n  System Prompt: {exp['system'] if exp['system'] else '(无)'}")
        print(f"  User Prompt:   {exp['user']}")
        print(f"\n  --- 模型回答 ---")

        # 调用 API
        answer, tokens = call_qwen(messages)
        total_tokens += tokens

        print(f"\n  {answer}")
        print(f"\n  [消耗 Token: {tokens}]")

    print(f"\n{'=' * 60}")
    print(f"实验完成！总消耗 Token: {total_tokens}")
    print(f"{'=' * 60}")
