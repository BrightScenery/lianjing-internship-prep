"""
System Prompt vs User Prompt 对比实验
目标：验证不同的 User Prompt 对模型回答风格的影响
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
# 同一个问题，不同的 User Prompt
experiments = [
    {
        "name": "实验1：模糊提问",
        "system": "你是一个 Linux教学助教，负责解答学生的 Linux 问题。",  
        "user": "怎么查看文件大小？",
    },
    {
        "name": "实验2：详细提问",
        "system": "你是一个 Linux教学助教，负责解答学生的 Linux 问题。",
        "user": "我在 Linux 终端里，想查看当前目录下所有文件和子目录的大小，并按大小排序，应该用什么命令？",
    },
    {
        "name": "实验3：指定输出格式",
        "system": "你是一个 Linux教学助教，负责解答学生的 Linux 问题。回答时请只给出命令，不要任何解释。",
        "user": "请用表格形式列出 3 种查看文件大小的 Linux 命令，分别说明它们的区别和适用场景。",
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
