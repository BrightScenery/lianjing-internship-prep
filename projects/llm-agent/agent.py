"""
5.24 搜索 Agent — agent.py

目标：搭建一个能联网搜索 + 总结的完整 Agent
场景：通用知识问答（用户提问 → Agent 搜索 → 总结回答）

和昨天 toy_agent.py 的区别：
- 昨天：工具是写死的模拟数据（GPU 状态字典）
- 今天：工具是真实的搜索引擎（ddgs 包）

核心流程不变：Thought → Action → Observation → 重复 → Final Answer
"""

import sys
import io
import os
import json
from dotenv import load_dotenv
import dashscope
from dashscope import Generation
from ddgs import DDGS

# Windows UTF-8 输出
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# ====== 第1步：加载 API Key ======
load_dotenv()
dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

# ====== 第2步：定义工具 ======

def web_search(query, max_results=5):
    """
    联网搜索，返回搜索结果摘要。

    原理：
    1. DDGS().text() 会向 DuckDuckGo 发送搜索请求
    2. 返回一个列表，每项包含 title（标题）、body（摘要）、href（链接）
    3. 模型只看 title + body，看不到完整网页内容——这就像"看搜索引擎的摘要页面"

    为什么要限制 max_results？
    - 搜索结果太多，模型的上下文会被塞满
    - 5条足够覆盖主要信息，再多边际效益递减
    - 这也是联旌实际场景：客户问"GPU 调度怎么做"，你搜索 top 5 结果就够总结了
    """
    try:
        results = DDGS().text(query, max_results=max_results)
        if not results:
            return "没有找到相关搜索结果"

        # 把搜索结果格式化成模型容易理解的文本
        output = []
        for i, item in enumerate(results, 1):
            output.append(f"[{i}] {item['title']}\n    {item['body']}\n    链接: {item['href']}")
        return "\n\n".join(output)
    except Exception as e:
        return f"搜索出错: {e}"


def read_url_summary(url):
    """
    获取某个网页的简要摘要（用标题+摘要模拟，不真正抓取全文）。

    为什么不全抓网页？
    - 完整抓取需要 requests + BeautifulSoup，对初学者太重
    - 搜索结果里的 body（摘要）已经包含了网页核心信息
    - 这个工具的存在是教模型"可以进一步深入某个链接"，实际返回摘要即可

    联旌场景类比：客户让你"查一下 NVIDIA 最新的 MIG 技术"，
    你先搜关键词（web_search），然后可能需要点进具体文章看详情（read_url_summary）。
    """
    return f"这是 {url} 的摘要页面。（实际项目中这里会用 requests 抓取网页全文并提取正文）"


# ====== 第3步：工具描述（告诉模型有哪些工具可用） ======

tools = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "联网搜索给定关键词，返回搜索结果摘要。当你需要查找信息、回答问题时使用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "搜索关键词，应该简洁明确，例如：'Kubernetes 是什么'、'GPU MIG 技术'"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "返回结果数量，默认 5，最多 10"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_url_summary",
            "description": "获取某个网页的摘要。当你已经通过搜索找到了相关链接，想要更详细信息时使用。",
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "网页 URL，例如：https://example.com/article"
                    }
                },
                "required": ["url"]
            }
        }
    },
]

# 工具名 → 函数映射
function_map = {
    "web_search": web_search,
    "read_url_summary": read_url_summary,
}

# ====== 第4步：System Prompt ======

system_prompt = """你是一个智能搜索助手。你的任务是帮助用户回答问题。

你有一个搜索工具（web_search），可以联网搜索信息。还有一个网页摘要工具（read_url_summary）可以查看具体链接的内容。

工作流程：
1. 理解用户的问题
2. 使用 web_search 搜索相关信息（可以搜索多次，用不同的关键词）
3. 如果需要更详细信息，使用 read_url_summary 查看具体网页
4. 根据搜索结果总结并回答问题

注意：
- 搜索时使用简洁明确的关键词
- 可以多次搜索来覆盖不同角度的信息
- 最后一定要基于搜索结果给出具体的回答
- 如果搜索结果为空，尝试换关键词重新搜索"""

# ====== 第5步：Agent 核心循环 ======

def run_agent(user_input, max_turns=10):
    """
    Agent 核心循环（和昨天 toy_agent.py 完全一样的结构，只是工具换了）

    1. 把用户输入 + system prompt + 工具描述发给模型
    2. 模型返回：
       A) 直接回答（content 有内容）→ 任务完成
       B) 请求调工具（tool_calls 有内容）→ 执行工具，把结果加到历史，回到1
    3. 循环直到模型给出最终回答
    """

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input},
    ]

    print(f"{'='*60}")
    print(f"用户问题: {user_input}")
    print(f"{'='*60}\n")

    turn = 0
    while turn < max_turns:
        turn += 1
        print(f"--- 第 {turn} 轮 ---")

        response = Generation.call(
            model="qwen-plus",
            messages=messages,
            tools=tools,
            result_format="message",
        )

        message = response.output.choices[0].message

        # 情况A：模型直接回答（不调工具）
        if not message.get("tool_calls"):
            final_answer = message.get("content", "无内容")
            print(f"\n{'='*60}")
            print(f"最终回答:")
            print(f"{'='*60}")
            print(final_answer)
            return final_answer

        # 情况B：模型请求调工具
        for tool_call in message["tool_calls"]:
            func_name = tool_call["function"]["name"]
            func_args = json.loads(tool_call["function"]["arguments"])
            print(f"模型请求调用: {func_name}({json.dumps(func_args, ensure_ascii=False)})")

            # 执行工具
            if func_name in function_map:
                func = function_map[func_name]
                try:
                    result = func(**func_args)
                except Exception as e:
                    result = f"执行出错: {e}"

                # 结果太长时截断（搜索可能返回大量文本）
                result_str = result if isinstance(result, str) else json.dumps(result, ensure_ascii=False)
                if len(result_str) > 2000:
                    result_str = result_str[:2000] + "\n...（结果已截断）"

                print(f"工具返回结果（前200字）: {result_str[:200]}...\n")

                messages.append(message)
                messages.append({
                    "role": "tool",
                    "content": result_str,
                    "tool_call_id": tool_call["id"],
                })

    # 超过最大轮数
    print(f"\n⚠️ 超过最大轮数 ({max_turns})，强制结束")
    messages.append({"role": "user", "content": "请用已有信息给出最终回答"})
    response = Generation.call(
        model="qwen-plus",
        messages=messages,
        tools=tools,
        result_format="message",
    )
    final = response.output.choices[0].message.get("content", "无内容")
    print(f"\n最终回答:\n{final}")
    return final

# ====== 交互式模式 ======

def interactive_mode():
    """
    交互模式：用户可以连续提问，Agent 保持对话。

    为什么要交互模式？
    - 方便测试不同的问题
    - 模拟真实的对话场景
    - 可以观察 Agent 在多轮对话中的行为
    """
    print("搜索 Agent 已启动！（输入 'quit' 或 'exit' 退出）")
    print("示例问题：")
    print("  1. Kubernetes 是什么？")
    print("  2. GPU 的 MIG 技术有什么用？")
    print("  3. Docker 和虚拟机的区别是什么？\n")

    messages = [
        {"role": "system", "content": system_prompt},
    ]

    while True:
        user_input = input("\n你: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ["quit", "exit", "q"]:
            print("再见！")
            break

        messages.append({"role": "user", "content": user_input})

        response = Generation.call(
            model="qwen-plus",
            messages=messages,
            tools=tools,
            result_format="message",
        )

        message = response.output.choices[0].message

        max_turns = 10
        turn = 0
        while turn < max_turns and message.get("tool_calls"):
            turn += 1
            print(f"\n--- 第 {turn} 轮 ---")

            for tool_call in message["tool_calls"]:
                func_name = tool_call["function"]["name"]
                func_args = json.loads(tool_call["function"]["arguments"])
                print(f"搜索: {func_args.get('query', '无关键词')}")

                if func_name in function_map:
                    func = function_map[func_name]
                    try:
                        result = func(**func_args)
                    except Exception as e:
                        result = f"执行出错: {e}"

                    result_str = result if isinstance(result, str) else json.dumps(result, ensure_ascii=False)
                    if len(result_str) > 2000:
                        result_str = result_str[:2000] + "\n...（截断）"

                    messages.append(message)
                    messages.append({
                        "role": "tool",
                        "content": result_str,
                        "tool_call_id": tool_call["id"],
                    })

            response = Generation.call(
                model="qwen-plus",
                messages=messages,
                tools=tools,
                result_format="message",
            )
            message = response.output.choices[0].message

        answer = message.get("content", "无内容")
        print(f"\n助手: {answer}")
        messages.append({"role": "assistant", "content": answer})


# ====== 运行 ======
if __name__ == "__main__":
    # 模式选择：改这里切换
    MODE = "interactive"  # "test" 或 "interactive"

    if MODE == "test":
        # 测试模式：跑几个预定义问题
        run_agent("Kubernetes 是什么？")
        print("\n\n")
        run_agent("GPU 的 MIG 技术有什么用？")

    elif MODE == "interactive":
        # 交互模式：连续提问
        interactive_mode()
