# 第5周学习总结：大模型 API + Agent

> 日期：2026.05.20 - 2026.05.26

## 本周目标
掌握大模型 API 调用，理解 System Prompt vs User Prompt，搭建简单 Agent。

## 学习内容

### 核心概念

| 概念 | 我的理解 |
|------|---------|
| System Prompt vs User Prompt | |
| Function Calling | |
| Agent 范式（ReAct / Tool Use） | |
| 本地模型 vs 云端 API | |
| Prompt Engineering | |

### API 调用测试（目标 20+）

| 场景 | 使用的模型 | 效果 |
|------|-----------|------|
| | | |

## 本周产出
- 代码：[Agent 模块](../../projects/rag-knowledge-base/agent.py)

## 量化数据
| 指标 | 目标 | 实际 |
|------|------|------|
| commit 次数 | 7 | |
| 学习时长 | 12h | |
| API 调用次数 | 20 | |
| 代码行数 | 150 | |

## 重点场景（结合运维能力）

### 场景 1：后台运行 Agent 服务
Agent 服务需要长期运行，SSH 窗口一关进程就挂了。用 `tmux` 管理会话，网络波动也不怕。`nohup python agent.py &` 适合简单后台运行，但 `tmux` 可以随时回来看到实时输出。

### 场景 2：进程管理与僵尸进程
用 Python Multiprocessing 开多进程处理数据时，主程序挂了子进程没退干净，产生 defunct 进程。僵尸进程 kill 不掉，要杀父进程。这是文章提到的经典面试题。

## 反思与下周计划

### 做得好的地方

### 需要改进的地方

### 下周（第6周）重点：简历 + 发邮件
- 全面回顾 6 周学习，提炼亮点
- 确保每个产出都有清晰的量化数据
- 写简历、模拟面试、准备邮件
