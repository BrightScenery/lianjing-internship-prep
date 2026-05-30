# Agent 知识卡片

## 卡片 1：Agent 是什么

**一句话**：Agent = 大模型 + 工具 + **循环自主决策**。

大模型只能"说话"，不能"做事"。Function Calling 让它能调一次工具，但流程是代码写死的。**Agent 的不同在于**：模型在一个 while 循环里自己决定——下一步调哪个工具、调几个、什么时候信息够了可以回答。

**类比**：
- Function Calling = 服务员帮你点一个菜，流程固定
- Agent = 运维工程师帮你排查问题，自己决定查什么、查几次

## 卡片 2：ReAct 范式（Reasoning + Acting）

Agent 最经典的思维模式：

```
Thought（思考）: 我现在知道什么？还需要知道什么？
Action（行动）: 调用工具收集信息
Observation（观察）: 工具返回了什么？
→ 回到 Thought →
... 循环直到信息够了 →
Final Answer: 给出最终回答
```

**关键**：每一轮的 Thought/Action/Observation 都存在 `messages` 对话历史里，模型知道自己"之前查过什么"，不会重复查。这就是"有记忆"。

## 卡片 3：Agent 核心代码结构

```python
messages = [system_prompt, user_input]

while turn < max_turns:
    # 1. 让模型思考（每次都要传完整的 messages + tools）
    response = llm(messages, tools)

    # 2. 模型决定：直接回答 vs 调工具
    if not response.tool_calls:
        return response.content  # 信息够了，退出循环

    # 3. 执行工具
    for tool_call in response.tool_calls:
        result = execute_tool(tool_call)
        # 4. 把 tool_calls 请求和结果都追加到 messages
        messages.append(message)        # 模型的调用请求
        messages.append(tool_result)    # 工具返回的结果

    # 5. 回到步骤1，模型基于新信息再次思考
```

**为什么是这个结构**：
- `max_turns`：防止无限循环（模型可能"卡住"反复调同一个工具）
- 每轮都要传 `tools`：API 无状态，每次都要声明可用工具
- 追加完整的 message + tool_result：模型需要"记忆"，否则第二轮和第一轮状态一样，会重复调用

## 卡片 4：Function Calling vs Agent 对比

| 维度 | Function Calling | Agent |
|------|-----------------|-------|
| 流程控制 | 代码写死（if-else） | 模型自主决策（while 循环） |
| 调用次数 | 固定一次 | 模型决定，循环多次 |
| 适合场景 | 简单查询（"几点了"） | 复杂任务（"诊断GPU问题"） |
| 停止条件 | 代码写死 | 模型判断"信息够了"时不调工具 |

## 卡片 5：Tool 描述的重要性

工具描述（`tools` 数组里每个函数的 `description` 和 `parameters`）是 Agent 的"眼睛"——模型全靠这个决定调哪个工具、传什么参数。

**写工具描述的要点**：
- `description` 要说明"这个工具能做什么，什么时候用"
- `parameters` 里每个参数的 `description` 要给出具体例子
- 如果描述模糊，模型可能调错工具或传错参数

**和 Function Calling 一样**：工具描述的质量直接决定模型表现。

## 卡片 6：System Prompt 的作用

System Prompt 设定 Agent 的行为模式和工作流程。它不是"角色设定"，而是**告诉模型怎么用工具、什么时候停止**。

好的 system prompt 应该包含：
- 你是谁（角色）
- 你有哪些工具（能力边界）
- 工作流程（先做什么、再做什么）
- 注意事项（不要一次性调所有工具、信息够了就回答等）

## 卡片 7：Agent 在联旌场景中的应用

联旌的 EaaS 平台运维场景中，Agent 可以用于：

1. **GPU 故障诊断**：用户报告"GPU-2 很慢"，Agent 自主查使用率、进程、告警
2. **资源调度建议**：Agent 分析各节点负载，建议如何分配任务
3. **客户问题排查**：用户报告某个容器挂了，Agent 查日志、资源、网络

这些场景的共同点：问题复杂、需要多角度信息、没有固定流程——正是 Agent 擅长的。

## 卡片 8：toy_agent.py vs agent.py 的区别

| 维度 | toy_agent.py | agent.py |
|------|-------------|----------|
| 工具来源 | 硬编码的模拟数据（GPU 状态字典） | DuckDuckGo 真实搜索（DDGS 包） |
| 场景 | GPU 集群诊断教学示例 | 通用联网搜索问答 |
| 工具数量 | 4个（GPU/进程/磁盘/告警） | 2个（搜索 + 网页摘要） |
| 核心循环 | 完全一样 | 完全一样 |

**关键结论**：Agent 框架和工具来源无关。换了工具，核心 while 循环不用改。这就是框架的价值。

## 卡片 9：容易踩的坑

1. **不传 tools**：每轮都要传，否则模型"忘记"可用工具
2. **丢失对话历史**：tool_calls 和 tool_result 必须都追加到 messages，否则模型"失忆"
3. **不设 max_turns**：模型可能无限循环，永远不回答
4. **工具描述不清晰**：模型不知道什么时候用、怎么用
5. **system prompt 不明确**：Agent 可能调错工具或过早结束循环
6. **工具结果太长**：需要截断（如 `agent.py` 里的 2000 字符限制），否则塞满上下文

## 卡片 10：Agent 和联旌技术的关联

```
前5周技能链：
Linux → Docker → K8s → RAG → Agent
  ↓        ↓        ↓      ↓      ↓
运维基础  容器打包  集群调度  知识问答  自主诊断

串联起来的故事线：
"我理解了一个 AI 应用从开发到运维的全流程：
 用 Linux + Docker 打包部署（基础设施）
 用 K8s 管理集群（调度运维）
 用 RAG 搭建知识库问答（应用层）
 用 Agent 实现智能诊断（智能化运维）"
```

这个完整的技能链就是面试时可以讲的"项目故事"。
