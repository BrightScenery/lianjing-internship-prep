"""
第一个大模型 API 调用实验
目标：调通 DashScope（通义千问）API，理解请求-响应流程
"""

import os
from dotenv import load_dotenv
import dashscope
from dashscope import Generation

# 1. 加载 .env 文件中的 API Key
load_dotenv()
dashscope_api_key = os.getenv("DASHSCOPE_API_KEY")
dashscope.api_key = dashscope_api_key

# 2. 构造消息 —— messages 是一个列表，每个消息有 role 和 content
#    system: 设定模型的角色/行为（"人设"）
#    user: 用户的实际提问
messages = [
    {"role": "system", "content": "你是一个技术助手。"},
    {"role": "user", "content": "Python 的列表和元组有什么区别？"},
    {"role": "assistant", "content": "列表用 [] 表示，可变；元组用 () 表示，不可变。"},
    {"role": "user", "content": "那我什么时候该用元组？"},
]

# 3. 调用 API
#    model: 使用的模型名称（qwen-plus 是通义千问的中等规模模型，性价比高）
#    messages: 对话消息列表
response = Generation.call(
    model="qwen-plus",
    messages=messages
)

# 4. 解析返回结果
if response.status_code == 200:
    print("=== 模型回答 ===")
    print(response.output.text)
    print("\n=== 元数据 ===")
    print(f"请求 ID: {response.request_id}")
    print(f"使用了多少 token: {response.usage.total_tokens}")
else:
    print(f"调用失败！状态码: {response.status_code}")
    print(f"错误信息: {response.message}")
  
