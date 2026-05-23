"""
5.23 手写最小 Agent — toy_agent.py

目标：理解 Agent 的核心循环（ReAct 范式）
场景：联旌 GPU 集群诊断助手

Agent 和 Function Calling 的区别：
- Function Calling：单次调用，流程由代码控制
- Agent：循环自主决策，模型自己决定调什么工具、调几次、什么时候停止

核心循环：Thought → Action → Observation → 重复 → Final Answer
"""

import os
import sys
import json
from dotenv import load_dotenv
import dashscope
from dashscope import Generation

# Windows 终端 UTF-8
if sys.stdout.encoding != 'utf-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ====== 第1步：加载 API Key ======
load_dotenv()
dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

# ====== 第2步：定义工具（Agent 可以调用的"手脚"） ======
# 注意：Agent 模式下，模型会自主决定调哪个工具、什么时候调

def get_gpu_usage(gpu_id):
    """获取指定 GPU 的使用率、温度、显存占用"""
    gpu_data = {
        "GPU-0": {"usage": "15%", "temp": "42°C", "memory": "2.1GB / 24GB"},
        "GPU-1": {"usage": "98%", "temp": "87°C", "memory": "23.5GB / 24GB"},
        "GPU-2": {"usage": "95%", "temp": "85°C", "memory": "22.8GB / 24GB"},
        "GPU-3": {"usage": "5%",  "temp": "38°C", "memory": "0.5GB / 24GB"},
    }
    return gpu_data.get(gpu_id, f"找不到 {gpu_id} 的信息")

def get_running_processes(gpu_id):
    """获取指定 GPU 上正在运行的进程"""
    process_data = {
        "GPU-0": [{"pid": 1234, "name": "python", "user": "zhangsan", "memory": "2.1GB"}],
        "GPU-1": [
            {"pid": 5678, "name": "python", "user": "lisi", "memory": "12.0GB"},
            {"pid": 5690, "name": "python", "user": "lisi", "memory": "11.5GB"},
        ],
        "GPU-2": [
            {"pid": 9012, "name": "python", "user": "wangwu", "memory": "15.0GB"},
            {"pid": 9034, "name": "python", "user": "wangwu", "memory": "7.8GB"},
        ],
        "GPU-3": [],
    }
    return process_data.get(gpu_id, [])

def get_disk_usage(node):
    """获取指定计算节点的磁盘使用情况"""
    disk_data = {
        "node-1": {"total": "500GB", "used": "420GB", "available": "80GB", "usage_pct": "84%"},
        "node-2": {"total": "500GB", "used": "490GB", "available": "10GB", "usage_pct": "98%"},
        "node-3": {"total": "1TB",  "used": "300GB", "available": "700GB", "usage_pct": "30%"},
    }
    return disk_data.get(node, f"找不到 {node} 的磁盘信息")

def get_cluster_alerts():
    """获取集群最近的告警信息"""
    return [
        {"time": "2026-05-23 08:15", "level": "WARNING", "message": "GPU-1 温度超过 85°C"},
        {"time": "2026-05-23 09:30", "level": "CRITICAL", "message": "node-2 磁盘使用率 98%"},
        {"time": "2026-05-23 10:00", "level": "WARNING", "message": "GPU-2 显存占用超过 90%"},
    ]

# ====== 第3步：工具描述（Agent 的"眼睛"——模型靠这个决定调哪个工具） ======
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_gpu_usage",
            "description": "获取指定 GPU 的使用率、温度和显存占用情况",
            "parameters": {
                "type": "object",
                "properties": {
                    "gpu_id": {
                        "type": "string",
                        "description": "GPU 编号，例如：GPU-0、GPU-1、GPU-2"
                    }
                },
                "required": ["gpu_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_running_processes",
            "description": "获取指定 GPU 上正在运行的进程列表，包括进程名、用户和显存占用",
            "parameters": {
                "type": "object",
                "properties": {
                    "gpu_id": {
                        "type": "string",
                        "description": "GPU 编号，例如：GPU-0、GPU-1、GPU-2"
                    }
                },
                "required": ["gpu_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_disk_usage",
            "description": "获取指定计算节点的磁盘使用情况",
            "parameters": {
                "type": "object",
                "properties": {
                    "node": {
                        "type": "string",
                        "description": "计算节点名称，例如：node-1、node-2、node-3"
                    }
                },
                "required": ["node"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_cluster_alerts",
            "description": "获取集群最近的告警信息，包括时间、级别和描述",
            "parameters": {
                "type": "object",
                "properties": {},
            }
        }
    },
]

# 工具名 → 函数映射
function_map = {
    "get_gpu_usage": get_gpu_usage,
    "get_running_processes": get_running_processes,
    "get_disk_usage": get_disk_usage,
    "get_cluster_alerts": get_cluster_alerts,
}

# ====== 第4步：System Prompt（给 Agent 设定行为模式） ======
system_prompt = """你是一个 GPU 集群诊断助手。你的任务是根据用户的问题，使用可用的工具来收集信息，然后给出诊断建议。

工作流程：
1. 先理解用户的问题
2. 使用工具收集相关数据
3. 根据收集到的信息分析原因
4. 给出诊断建议和解决方案

注意：
- 不要一次性调用所有工具，要根据问题有选择地调用
- 如果一个问题需要多个角度的信息，可以分多次调用工具
- 最后一定要给出具体的诊断建议和解决方案"""

# ====== 第5步：Agent 核心循环 ======

def run_agent(user_input):
    """
    Agent 核心循环

    原理：
    1. 把用户输入 + system prompt + 工具描述发给模型
    2. 模型有两种返回：
       A) 直接给出最终回答（content 有内容）→ 任务完成
       B) 请求调用工具（tool_calls 有内容）→ 执行工具，把结果加到对话历史，回到步骤1
    3. 循环直到模型给出最终回答

    这就是 ReAct 范式：Reasoning（模型思考下一步）+ Acting（执行工具）
    循环中的每一步都记录在 messages 中，所以模型知道"我已经查了什么"
    """

    # 初始化对话历史
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input},
    ]

    print(f"=== 用户输入 ===")
    print(user_input)
    print()

    max_turns = 10  # 防止无限循环，最多 10 轮
    turn = 0

    while turn < max_turns:
        turn += 1
        print(f"--- 第 {turn} 轮思考 ---")

        # 调用模型（每次都传入完整的对话历史 + 工具列表）
        response = Generation.call(
            model="qwen-plus",
            messages=messages,
            tools=tools,
            result_format="message",
        )

        message = response.output.choices[0].message

        # 情况A：模型给出了最终回答（没有请求调用工具）
        if "tool_calls" not in message or not message["tool_calls"]:
            final_answer = message.get("content", "无内容")
            print(f"=== 最终回答 ===")
            print(final_answer)
            return final_answer

        # 情况B：模型请求调用工具
        print(f"模型请求调用 {len(message['tool_calls'])} 个工具：")
        for tool_call in message["tool_calls"]:
            func_name = tool_call["function"]["name"]
            func_args = json.loads(tool_call["function"]["arguments"])
            print(f"  → {func_name}({json.dumps(func_args, ensure_ascii=False)})")

            # 执行工具
            if func_name in function_map:
                func = function_map[func_name]
                try:
                    result = func(**func_args)
                    result_str = json.dumps(result, ensure_ascii=False) if isinstance(result, (dict, list)) else str(result)
                except Exception as e:
                    result_str = f"执行出错：{e}"

                print(f"  ← 结果: {result_str[:200]}")

                # 把模型的 tool_calls 和执行结果加入对话历史
                messages.append(message)
                messages.append({
                    "role": "tool",
                    "content": result_str,
                    "tool_call_id": tool_call["id"],
                })

        print()  # 空行分隔

    # 超过最大轮数
    print(f"⚠️ 超过最大轮数 ({max_turns})，强制结束")
    messages.append({
        "role": "user",
        "content": "请用已有的信息给出最终回答。"
    })
    response = Generation.call(
        model="qwen-plus",
        messages=messages,
        tools=tools,
        result_format="message",
    )
    final_message = response.output.choices[0].message
    print(f"=== 最终回答 ===")
    print(final_message.get("content", "无内容"))
    return final_message.get("content", "")

# ====== 第6步：运行 Agent ======
if __name__ == "__main__":
    # 测试场景 1：单个 GPU 问题
    print("=" * 60)
    print("测试 1：单个 GPU 性能问题")
    print("=" * 60)
    run_agent("GPU-1 最近跑得很慢，帮我查一下原因")

    print("\n" + "=" * 60)
    print("测试 2：集群整体状况")
    print("=" * 60)
    run_agent("帮我看看整个集群有什么问题")
