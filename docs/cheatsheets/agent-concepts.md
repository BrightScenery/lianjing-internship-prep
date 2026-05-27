# Agent 范式 — 概念笔记

## 一、Agent 是什么

Agent = 大模型 + 工具 + **自主决策循环**

大模型自己只能"说话"，不能"做事"。通过 Function Calling 可以让模型调用外部工具，但流程是固定的（调一次 → 拿结果 → 回答）。

**Agent 的不同之处在于**：模型在一个循环里自主决定：
- 下一步该调哪个工具
- 需要调几个工具
- 什么时候信息够了、可以给出最终回答

## 二、Function Calling vs Agent

| 维度 | Function Calling | Agent |
|------|-----------------|-------|
| 流程控制 | 代码写死 | 模型自主决策 |
| 调用次数 | 固定一次 | 循环多次，模型决定停止时机 |
| 适合场景 | 简单查询（"几点了"） | 复杂任务（"诊断问题"、"规划方案"） |
| 核心代码 | if-else | while 循环 |
| 类比 | 服务员帮你点一个菜 | 朋友帮你查攻略、规划整趟旅行 |

## 三、ReAct 范式（Reasoning + Acting）

Agent 最经典的范式是 **ReAct**：

```
Thought（思考）: 我需要知道什么？
Action（行动）: 调用工具收集信息
Observation（观察）: 工具返回了什么？
→ 重复上述三步 →
Final Answer（最终回答）: 信息够了，给出答案
```

每一轮的 Thought + Action + Observation 都记录在 messages 中，所以模型知道"我已经查过什么了"。

## 四、Agent 的核心代码结构

```python
messages = [system_prompt, user_input]

while True:
    # 1. 让模型思考
    response = llm(messages, tools)

    # 2. 模型决定：继续查 vs 直接回答
    if not response.tool_calls:
        return response.content  # 有足够信息了，退出循环

    # 3. 执行工具
    for tool_call in response.tool_calls:
        result = execute_tool(tool_call)
        messages.append(tool_call_result)

    # 4. 回到步骤1，模型基于新信息再次思考
```

**关键细节**：
- `max_turns`：必须设置上限，防止无限循环
- 每轮都要传 `tools`，否则模型"忘记"可用工具
- 完整的 messages 历史必须传递，模型需要知道"之前查过什么"
- system prompt 设定 Agent 的行为模式和工作流程

## 五、Agent 在联旌场景中的应用

联旌的 EaaS 平台运维场景中，Agent 可以用于：

1. **GPU 故障诊断**：用户报告"GPU-2 很慢"，Agent 自主查使用率、进程、告警
2. **资源调度建议**：Agent 分析各节点负载，建议如何分配任务
3. **客户问题排查**：用户报告某个容器挂了，Agent 查日志、资源、网络

Function Calling 是 Agent 的**基础组件**，Agent 是 Function Calling 的**循环升级版**。

## 六、容易踩的坑

1. **模型不停调用工具**：必须设 `max_turns` 上限
2. **忘记传 tools**：每轮都要传，否则模型无法调用工具
3. **丢失对话历史**：每轮的工具结果必须追加到 messages，否则模型"失忆"
4. **工具描述不清晰**：和 Function Calling 一样，tools 的 description 决定了模型能不能找到正确的工具
5. **system prompt 不明确**：Agent 需要明确的 workflow 指引，否则可能调错工具或过早结束
