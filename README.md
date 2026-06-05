# 📚 联旌智能实习准备 - 学习记录

> 福建农林大学 · 数据科学与大数据技术 · 2024级
>
> 目标公司：**联旌智能科技（上海）有限公司**
>
> 准备周期：2026.04.22 — 2026.06.05

---

## 🎯 为什么是这个计划？

联旌智能的核心产品是 **EaaS（Environment as a Service）高性能计算云平台**，本质上做一件事：**把异构算力（CPU/GPU/NPU）通过容器化和调度技术，变成用户开箱即用的服务**。

客户群体主要是**高校和科研院所**，典型场景包括：
- 为高校部署 HPC 集群，跑科研计算任务
- 为学校本地化部署 DeepSeek 等大模型（32B/70B/671B）
- 帮科研机构搭建 AI + HPC 混合算力平台

了解公司的业务方向后，我明确了学习路径需要**从基础设施层开始，而不是从应用层开始**——因为联旌的价值在于"让大模型跑起来"的底层能力。

### 能力画像

基于公司技术栈和岗位需求，我提取出需要掌握的技能路线：

```
底层能力：Linux 系统操作 + Shell 脚本
            ↓
中间层：Docker 容器化 + K8s 调度（容器引擎的基础）
            ↓
应用层：大模型部署 + RAG 知识库 + Agent（客户最常提的需求）
```

### 为什么自下而上学习？

作为大二实习生，短期内不可能参与核心调度算法开发，但如果能展现出"理解容器调度原理 + 能独立完成大模型部署交付"的能力，就能在实习阶段提供实际价值。同时这些能力本身也是行业内通用的，无论去哪里都用得上。

### 学习内容与业务场景的映射

| 我学的 | 对应的业务场景 |
|--------|---------------|
| Linux + Shell | HPC 集群运维、客户现场实施部署 |
| Docker 容器化 | EaaS 平台底层就是容器化架构 |
| K8s 调度原理 | 公司自研多级调度技术的理论基础 |
| RAG 知识库 | 高校/企业最常见的 AI 落地场景 |
| 大模型部署 | 帮客户本地化部署 DeepSeek 等模型 |
| Agent | AI 应用发展方向 |

---

## 📊 进度总览

| 指标 | 数值 |
|------|------|
| 📅 日历天数 | 45 / 45 |
| 🔥 有 commit 的天数 | 45 |
| 📝 总提交次数 | 45 |
| 💻 累计代码行数 | 3500+ |
| 📦 完成项目 | 5 / 5 |
| 📖 学习笔记 | 45 / 45 |

## 🗓️ 6 周学习路线

| 周次 | 日期 | 主题 | 状态 |
|------|------|------|------|
| 第1周 | 4.22 - 4.28 | Linux 生存训练 | ✅ 已完成 |
| 第2周 | 4.29 - 5.5 | Docker 速通 | ✅ 已完成 |
| 第3周 | 5.6 - 5.12 | K8s 名词扫盲 | ✅ 已完成 |
| 第4周 | 5.13 - 5.19 | RAG 实战（核心项目） | ✅ 已完成 |
| 第5周 | 5.20 - 5.26 | 大模型 API + Agent | ✅ 已完成 |
| 第6周 | 5.27 - 6.5 | 简历梳理 + 发邮件 | 🔥 进行中 |

## 🛠️ 技术栈掌握情况

- [x] Linux 基础（35+ 命令）— ping/curl/wget/ssh/ps/top/free/df/du/chmod/chown/grep/sed/awk 等
- [x] Shell 脚本编程 — 已编写 5 个脚本（check-system.sh / text-process.sh / file-practice.sh / net-api-check.sh / batch-rename.sh）
- [x] Linux 进阶概念 — 环境变量/PATH/软链接/硬链接
- [x] Docker 容器化 — 镜像/容器/分层/多阶段构建/.dockerignore/缓存优化
- [x] Kubernetes 基础 — Pod/Deployment/Service/IngressRoute 概念与实操
- [x] RAG 知识库搭建（LangChain + ChromaDB + DashScope + Gradio）
- [x] 大模型 API 调用
- [x] Agent 开发（ReAct 范式 + toy_agent.py）

## 📁 项目展示

1. [系统状态检查脚本](projects/hello-shell/) — Linux + Shell
2. [Flask Web 服务容器化](projects/docker-python-app/) — Docker
3. [K8s k3s 部署实战](projects/k8s-k3s-demo/) — Kubernetes
4. [本地 RAG 知识库](projects/rag-knowledge-base/) — LangChain + ChromaDB + DashScope + Gradio
5. [大模型 API + Agent](projects/llm-agent/) — DashScope + ReAct + DuckDuckGo + Docker

## 📰 学习记录

### 每日日志
- [第1周 (4.22-4.28)](docs/daily-log/week01/)
- [第2周 (4.29-5.5)](docs/daily-log/week02/)
- [第3周 (5.6-5.12)](docs/daily-log/week03/)
- [第4周 (5.13-5.19)](docs/daily-log/week04/)
- [第5周 (5.20-5.26)](docs/daily-log/week05/)
- [第6周 (5.27-6.5)](docs/daily-log/week06/)

### 周总结
- [Linux](docs/weekly/week1-linux.md) · [Docker](docs/weekly/week2-docker.md) · [K8s](docs/weekly/week3-k8s.md) · [RAG](docs/weekly/week4-rag.md) · [LLM+Agent](docs/weekly/week5-llm.md)

### 速查笔记
- [Linux 命令指南](docs/cheatsheets/linux-commands-guide.md)
- [GPU 命令速查](docs/cheatsheets/gpu-commands-cheatsheet.md)
- [GPU 管理笔记](docs/cheatsheets/gpu-management-notes.md)
- [Docker/K8s/Helm 总结](docs/cheatsheets/docker-k8s-helm-summary.md)
- [Agent 范式概念](docs/cheatsheets/agent-concepts.md)
- [Agent 知识卡片](docs/cheatsheets/agent-knowledge-cards.md) ← 面试复习用
- [RAG 知识速查](docs/cheatsheets/week4-knowledge-cheatsheet.md)

---

*本仓库每日自动记录 commit，所有学习笔记和项目代码均公开可查。*
