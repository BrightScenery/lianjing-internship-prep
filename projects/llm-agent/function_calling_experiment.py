"""
5.22 Function Calling 实验

目标：让大模型能够调用外部函数

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

# 工具1：查询当前时间
def get_current_time(city):
    """返回指定城市的当前时间（模拟）"""
    # 实际项目中这里会调用时区 API
    time_map = {
        "北京": "2026-05-22 20:30 (UTC+8)",
        "上海": "2026-05-22 20:30 (UTC+8)",
        "纽约": "2026-05-22 08:30 (UTC-5)",
        "伦敦": "2026-05-22 13:30 (UTC+1)",
        "东京": "2026-05-22 21:30 (UTC+9)",
    }
    return time_map.get(city, f"抱歉，我还没有 {city} 的时区信息")

# 工具2：查询天气
def get_weather(city):
    """返回指定城市的当前天气（模拟）"""
    weather_map = {
        "北京": "晴天，25°C，空气质量良",
        "上海": "多云，28°C，湿度65%",
        "广州": "雷阵雨，32°C，湿度85%",
        "深圳": "晴天，30°C，紫外线强",
    }
    return weather_map.get(city, f"抱歉，我还没有 {city} 的天气信息")

# ====== 第3步：把函数描述成模型能理解的格式 ======
# 这是 Function Calling 的核心——你必须清晰地描述每个函数
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "获取指定城市的当前时间",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，例如：北京、上海、纽约"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的当前天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，例如：北京、上海、广州"
                    }
                },
                "required": ["city"]
            }
        }
    }
]

# 工具名到实际函数的映射表
# 模型返回的是字符串函数名，你需要通过这个映射表找到对应的 Python 函数
function_map = {
    "get_current_time": get_current_time,
    "get_weather": get_weather,
}

# ====== 第4步：构造对话 ======
# 注意：这里没有 system prompt，让模型自由判断是否需要调用工具
messages = [
    {"role": "user", "content": "上海现在几点了？天气怎么样？"}
]

print("=== 用户提问 ===")
print(messages[0]["content"])
print()

# ====== 第5步：第一次调用模型（让模型决定是否调用工具） ======
response = Generation.call(
    model="qwen-plus",
    messages=messages,
    tools=tools,  # 把工具列表告诉模型
    result_format="message"  # 返回格式为 message，方便后续处理
)

print("=== 模型的第一轮回复 ===")
print(f"完整回复: {json.dumps(response.output, ensure_ascii=False, indent=2)}")

# ====== 第6步：解析模型的回复 ======
# 模型可能返回两种情况：
# A) 直接回答（不调用工具）→ content 有内容
# B) 请求调用工具 → tool_calls 有内容

message = response.output.choices[0].message

if "tool_calls" in message and message["tool_calls"]:
    print("\n=== 模型请求调用工具 ===")
    for tool_call in message["tool_calls"]:
        func_name = tool_call["function"]["name"]
        func_args = json.loads(tool_call["function"]["arguments"])
        print(f"函数名: {func_name}")
        print(f"参数: {func_args}")

        # 执行函数
        if func_name in function_map:
            result = function_map[func_name](**func_args)
            print(f"执行结果: {result}")

            # 把结果返回给模型
            messages.append(message)  # 添加模型的回复
            messages.append({
                "role": "tool",
                "content": str(result),
                "tool_call_id": tool_call["id"]
            })

    # ====== 第7步：第二次调用模型（用工具结果生成最终回答） ======
    print("\n=== 把工具结果返回给模型，生成最终回答 ===")
    final_response = Generation.call(
        model="qwen-plus",
        messages=messages,
        tools=tools,
        result_format="message"
    )

    final_message = final_response.output.choices[0].message
    print(f"最终回答: {final_message.get('content', '无内容')}")
else:
    print("\n模型选择了直接回答（没有调用工具）")
    print(f"回答内容: {message.get('content', '无内容')}")
