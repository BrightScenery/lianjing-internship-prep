# 第5周学习总结：大模型 API + Agent

> 日期：2026.05.20 - 2026.05.26

## 本周目标
掌握大模型 API 调用，理解 System Prompt vs User Prompt，搭建简单 Agent。

## 学习内容

### 核心概念

| 概念 | 我的理解 |
|------|---------|
| System Prompt vs User Prompt | System Prompt 是给模型设定"人设"和行为规则的（比如"你是 GPU 诊断助手"），User Prompt 是用户的具体问题。System Prompt 影响回答风格、格式、深度，不直接回答问题。同一个问题换不同 System Prompt，回答截然不同。 |
| Function Calling | 让大模型从"只会说话"变成"能调用工具"。核心三步：①定义工具列表（tools）告诉模型有哪些函数可用+参数描述；②模型判断是否需要调用，返回函数名+参数（tool_calls）；③我执行函数，把结果回传给模型生成最终回答。模型看不到函数实现，只看得到描述。 |
| Agent 范式（ReAct / Tool Use） | Agent = Function Calling + while 循环。核心是 ReAct 循环：Thought（模型思考下一步查什么）→ Action（调用工具）→ Observation（看工具返回结果）→ 重复直到信息够了给出 Final Answer。和 Function Calling 的本质区别：流程控制权从代码转移到模型手里。 |
| 本地模型 vs 云端 API | 本地模型（Ollama qwen2.5:7b）：免费、离线可用、速度慢、模型规模小。云端 API（通义千问/DeepSeek）：响应快、模型更强、按 token 计费、需要网络。RAG 用本地模型更合适（数据不离开本机），复杂推理用云端 API。 |
| Prompt Engineering | 通过精心设计输入来引导模型输出更好结果。技巧：①System Prompt 设定角色和工作流程；②User Prompt 清晰具体；③few-shot 示例（给模型看"好回答"的样例）；④格式约束（"用表格回答"、"3句话以内"）。 |

### API 调用测试（目标 20+）

| 场景 | 使用的模型 | 效果 |
|------|-----------|------|
| 首次调通 API（列表/元组问题） | qwen-plus | ✅ 成功，理解 messages 结构 |
| 对比通义 vs DeepSeek 回答 | qwen-plus vs deepseek-chat | ✅ 成功，同问题回答风格不同 |
| System Prompt 4组对比实验 | qwen-plus | ✅ 成功，验证"人设"效果 |
| 多轮对话（User Prompt 实验） | qwen-plus | ✅ 成功，messages 历史累积 |
| Function Calling（时间+天气） | qwen-plus | ✅ 成功，模型自主选工具 |
| GPU 运维 Function Calling | qwen-plus | ✅ 成功，多工具组合诊断 |
| GPU 诊断 Agent 循环 | qwen-plus | ✅ 成功，ReAct 自主决策 |
| 联网搜索 Agent | qwen-plus + DuckDuckGo | ✅ 成功，真实搜索引擎数据 |
| Agent 容器化 | qwen-plus（容器内） | ✅ 成功，镜像构建+运行 |

## 本周产出
- `api_test.py` — 首次调通通义千问 API（多轮对话示例）
- `deepseek_test.py` — 调通 DeepSeek API（OpenAI 兼容接口）
- `compare_models.py` — 双模型同问题对比
- `system_prompt_experiment.py` — 4 组 System Prompt 对比实验
- `user_prompt_experiment.py` — 多轮对话实验
- `function_calling_experiment.py` — Function Calling 入门（时间+天气）
- `gpu_tool_calling.py` — GPU 运维场景 Function Calling
- `toy_agent.py` — 手写最小 Agent（GPU 诊断，模拟数据）
- `agent.py` — 完整搜索 Agent（联网搜索 + 交互模式）
- `Dockerfile` — Agent 容器化
- `docs/agent-concepts.md` — Agent 范式概念笔记

## 量化数据
| 指标 | 目标 | 实际 |
|------|------|------|
| commit 次数 | 7 | 7 |
| 学习时长 | 12h | 15.5h |
| API 调用次数 | 20 | ~45 |
| 代码行数 | 150 | 260+ |

## 重点场景（结合运维能力）

### 场景 1：后台运行 Agent 服务
Agent 服务需要长期运行，SSH 窗口一关进程就挂了。用 `tmux` 管理会话，网络波动也不怕。`nohup python agent.py &` 适合简单后台运行，但 `tmux` 可以随时回来看到实时输出。

### 场景 2：进程管理与僵尸进程
用 Python Multiprocessing 开多进程处理数据时，主程序挂了子进程没退干净，产生 defunct 进程。僵尸进程 kill 不掉，要杀父进程。这是经典面试题。

### 场景 3：容器化交付 Agent
Agent 容器化的关键是 API Key 不能打包进镜像，必须通过环境变量注入：`docker run -e DASHSCOPE_API_KEY=xxx`。Dockerfile 分层缓存优化：先 COPY requirements.txt → pip install → 再 COPY 代码，代码改了不重装依赖。

## 知识进阶链路

```
Day 1-2：调 API → 理解 "大模型是对话引擎，messages 是完整历史"
         ↓
Day 3-4：Function Calling → 理解 "模型能看到工具描述，自己选工具"
         ↓
Day 5-6：Agent 循环 → 理解 "while 循环 + ReAct = 模型自主决策"
         ↓
Day 7：容器化 → 理解 "不管什么服务器，镜像跑起来效果一样"
```

## 反思与下周计划

### 做得好的地方
- 学习路径清晰：从 API 调用 → Function Calling → Agent 循环 → 容器化，每一步都建立在前一步基础上
- 结合公司场景：GPU 诊断 Agent 直接关联联旌 EaaS 平台的运维需求
- 容器化意识：每个应用都考虑了 Docker 打包，5 周技能形成了完整链路

### 需要改进的地方
- Agent 的工具还是模拟数据（toy_agent.py 的 GPU 数据是写死的字典），没有真正执行 `nvidia-smi` 等系统命令
- 联网搜索 Agent 用了 DuckDuckGo 摘要，没有真正用 requests + BeautifulSoup 抓取网页全文
- 实验代码没有写单元测试，主要靠手动运行验证
- week5-llm.md 的表格拖到周最后一天才填，应该边学边记

### 下周（第6周）重点：简历 + 发邮件
- 全面回顾 6 周学习，提炼亮点
- 确保每个产出都有清晰的量化数据
- 写简历、模拟面试、准备邮件
- 部署 GitHub Pages 个人站点
