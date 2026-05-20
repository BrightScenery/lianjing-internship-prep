from openai import OpenAI
import os
from dotenv import load_dotenv

# 加载 .env 文件中的 API Key
load_dotenv()

# 创建客户端，注意 base_url 指向 DeepSeek 的服务器
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

# 构造消息
messages = [
    {"role": "system", "content": "你是一个技术助手。"},
    {"role": "user", "content": "用一句话解释什么是 Agent。"}
]

# 调用 API
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=messages
)

# 提取回答——注意路径不同：choices[0].message.content
print(response.choices[0].message.content)