"""
5.22 Function Calling 实验（增强版）

目标：让大模型能够调用外部函数

新增改进：
1. 错误处理：工具函数执行失败时，将错误信息返回给模型而非崩溃
2. 多轮对话：用户可连续提问，模型保持上下文并继续调用工具

原理：
1. 定义一些函数（比如查天气、查时间），并写出每个函数的"描述"
2. 把这些函数的描述告诉模型（模型并不知道函数的具体实现）
3. 用户提问后，模型判断是否需要调用某个函数
4. 如果需要，模型返回：函数名 + 参数
5. 你在代码中执行这个函数，把结果返回给模型
6. 模型根据结果生成最终回答

关键概念：
- tools: 工具列表，告诉模型有哪些函数可用
- tool_call: 模型返回的"函数调用请求"（函数名 + 参数）
- tool_output: 你执行函数后的结果
"""

import os
import sys
import json
from dotenv import load_dotenv
import dashscope
from dashscope import Generation

# 确保终端输出 UTF-8 编码（Windows 终端默认 GBK）
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ====== 第1步：加载 API Key ======
load_dotenv()
dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

# ====== 第2步：定义"工具"（函数 + 描述） ======
# 这些是模型可以调用的工具。注意：模型只能看到"描述"，看不到具体代码实现。

# 工具1：查询 GPU 状态
def get_gpu_status(gpu_id):
    """查询某张 GPU 的利用率、显存、温度"""
    # 实际项目中这里会调用 GPU 监控 API
    # 模拟可能发生的异常：如果 gpu_id 是空字符串，抛出异常演示错误处理
    if gpu_id == "":
        raise ValueError("GPU ID 不能为空")
    
    gpu_map = {
        "0": "GPU 0: 正在运行，温度 65°C，使用率 75%",
        "1": "GPU 1: 空闲，温度 45°C，使用率 10%",
    }
    return gpu_map.get(gpu_id, f"抱歉，我还没有 GPU {gpu_id} 的信息")

# 工具2：查询服务器负载
def get_server_load(server_name):
    """查询某台服务器的 CPU 和内存负载"""
    server_map = {
        "server-A": "CPU: 75%, 内存: 60%",
        "server-B": "CPU: 45%, 内存: 80%",
    }
    return server_map.get(server_name, f"抱歉，我还没有 {server_name} 的负载信息")

# ====== 第3步：把函数描述成模型能理解的格式 ======
# 这是 Function Calling 的核心——你必须清晰地描述每个函数
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_gpu_status",
            "description": "查询某张 GPU 的利用率、显存、温度",
            "parameters": {
                "type": "object",
                "properties": {
                    "gpu_id": {
                        "type": "string",
                        "description": "GPU ID，例如：0、1"
                    }
                },
                "required": ["gpu_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_server_load",
            "description": "查询某台服务器的 CPU 和内存负载",
            "parameters": {
                "type": "object",
                "properties": {
                    "server_name": {
                        "type": "string",
                        "description": "服务器名称，例如：server-A、server-B"
                    }
                },
                "required": ["server_name"]
            }
        }
    }
]

# 工具名到实际函数的映射表
# 模型返回的是字符串函数名，你需要通过这个映射表找到对应的 Python 函数
function_map = {
    "get_gpu_status": get_gpu_status,
    "get_server_load": get_server_load,
}

# ====== 辅助函数：处理一轮对话（自动处理工具调用） ======
def process_turn(messages, tools, function_map):
    """
    处理一轮对话：调用模型，如果模型请求工具则执行并再次调用，最终返回模型的最终回复。
    同时会更新 messages 历史（添加 assistant 回复和可能的 tool 消息）。
    
    参数:
        messages: 对话历史列表
        tools: 工具描述列表
        function_map: 函数名到实际函数的映射
    
    返回:
        final_content: 模型最终回答的文本内容
    """
    # 第一次调用模型（让模型决定是否调用工具）
    response = Generation.call(
        model="qwen-plus",
        messages=messages,
        tools=tools,
        result_format="message"
    )
    
    message = response.output.choices[0].message
    
    # 情况1：模型直接回答（不调用工具）
    if not message.get("tool_calls"):
        print("\n=== 模型直接回答 ===")
        final_content = message.get("content", "无内容")
        # 将模型的直接回答添加到历史中
        messages.append({"role": "assistant", "content": final_content})
        return final_content
    
    # 情况2：模型请求调用工具
    print("\n=== 模型请求调用工具 ===")
    # 将模型的工具调用请求添加到历史中（role=assistant, 含 tool_calls）
    messages.append(message)
    
    for tool_call in message["tool_calls"]:
        func_name = tool_call["function"]["name"]
        func_args = json.loads(tool_call["function"]["arguments"])
        print(f"函数名: {func_name}")
        print(f"参数: {func_args}")
        
        # ====== 改进1：错误处理 ======
        # 调用工具函数时加 try/except，避免程序崩溃
        try:
            result = function_map[func_name](**func_args)
            print(f"执行结果: {result}")
        except Exception as e:
            # 工具执行失败，将错误信息作为 tool 结果返回给模型
            error_msg = f"工具执行失败: {type(e).__name__}: {str(e)}"
            print(f"执行出错: {error_msg}")
            result = error_msg
        
        # 把工具结果添加到历史中（role=tool）
        messages.append({
            "role": "tool",
            "content": str(result),
            "tool_call_id": tool_call["id"]
        })
    
    # 第二次调用模型：将工具结果喂给模型，生成最终回答
    print("\n=== 把工具结果返回给模型，生成最终回答 ===")
    final_response = Generation.call(
        model="qwen-plus",
        messages=messages,
        tools=tools,
        result_format="message"
    )
    
    final_message = final_response.output.choices[0].message
    final_content = final_message.get("content", "无内容")
    print(f"最终回答: {final_content}")
    
    # 将模型的最终回答添加到历史中
    messages.append({"role": "assistant", "content": final_content})
    
    return final_content

# ====== 第4步：初始化对话历史 ======
messages = []

# ====== 第5步：第一轮对话 ======
print("=" * 50)
print("第一轮对话")
print("=" * 50)

user_input1 = "GPU-0 现在负载高吗？server-A 的内存够用吗？"
print(f"用户: {user_input1}")
messages.append({"role": "user", "content": user_input1})

final_answer1 = process_turn(messages, tools, function_map)
print(f"\n助手最终回复: {final_answer1}")

print("\n" + "=" * 50)
print("第二轮对话（多轮连续）")
print("=" * 50)

# ====== 第6步：第二轮对话（模拟用户继续提问） ======
user_input2 = "那 GPU-1 呢？"
print(f"用户: {user_input2}")
messages.append({"role": "user", "content": user_input2})

final_answer2 = process_turn(messages, tools, function_map)
print(f"\n助手最终回复: {final_answer2}")

# 可选：展示完整对话历史
print("\n" + "=" * 50)
print("完整对话历史")
print("=" * 50)
for msg in messages:
    role = msg["role"]
    if role == "user":
        print(f"用户: {msg['content']}")
    elif role == "assistant":
        print(f"助手: {msg['content']}")
    elif role == "tool":
        print(f"工具结果: {msg['content']}")
    else:
        print(f"{role}: {msg}")