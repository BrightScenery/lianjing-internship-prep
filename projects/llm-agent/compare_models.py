# compare_models.py
import os
from dotenv import load_dotenv
import dashscope
from dashscope import Generation
from openai import OpenAI

# 加载 .env 文件中的 API Key
load_dotenv()

# ==================== 通义千问调用函数 ====================
def call_qwen(prompt: str) -> str:
    """
    复用 api_test.py 的 dashscope 调用逻辑
    支持多轮对话（这里为了简单，只传单条 user 消息，但可扩展）
    """
    dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")
    
    messages = [
        {"role": "system", "content": "你是一个技术助手。"},
        {"role": "user", "content": prompt}
    ]
    
    response = Generation.call(
        model="qwen-plus",
        messages=messages
    )
    
    if response.status_code == 200:
        return response.output.text
    else:
        return f"调用失败！状态码: {response.status_code}, 错误: {response.message}"

# ==================== DeepSeek 调用函数 ====================
def call_deepseek(prompt: str) -> str:
    """
    复用 deepseek_test.py 的 OpenAI 兼容接口调用逻辑
    """
    client = OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com"          # 注意：没有 /v1 后缀，与你原文件一致
    )
    
    messages = [
        {"role": "system", "content": "你是一个技术助手。"},
        {"role": "user", "content": prompt}
    ]
    
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages
    )
    
    return response.choices[0].message.content

# ==================== 主程序 ====================
if __name__ == "__main__":
    # 定义同一个问题
    question = "用一句话解释什么是 Agent。"
    
    print("=" * 50)
    print(f"问题：{question}\n")
    
    print("【通义千问】回答：")
    qwen_answer = call_qwen(question)
    print(qwen_answer)
    
    print("\n" + "-" * 40)
    
    print("【DeepSeek】回答：")
    deepseek_answer = call_deepseek(question)
    print(deepseek_answer)
    
    print("\n" + "=" * 50)