# 第4周学习总结：RAG 实战（核心项目）

> 日期：2026.05.13 - 2026.05.19

## 本周目标
搭建完整的 RAG 知识库系统，上传文档实现问答，用 Docker 打包。

## 学习内容

### 核心概念

| 概念 | 我的理解 |
|------|---------|
| RAG 原理 | 两阶段流程：用户提问 → 向量检索相关文档片段 → 拼接到 Prompt → LLM 生成回答。核心是检索质量决定回答质量。类比：开卷考试 vs 闭卷考试 |
| 向量数据库（ChromaDB） | 存储和检索"向量"的数据库。向量 = 文本通过 Embedding 模型转换成的高维数字数组。语义相近的文本向量在空间中距离近。ChromaDB 底层是 SQLite（存原文）+ HNSW 索引文件（存向量关系图） |
| 文本分块（Chunking） | RecursiveCharacterTextSplitter 按段落→句子→词逐级切分，chunk_size=800 + chunk_overlap=150，避免语义断裂。overlap 防止边界处的内容被拦腰截断 |
| Embedding（文本向量化） | 使用 DashScope text-embedding-v3 模型（1024 维）或 Ollama bge-m3。同一个项目入库和检索必须用同一个 Embedding 模型，否则维度不一致 |
| 本地模型部署（Ollama） | Ollama 是一键部署本地 LLM 的工具，拉取 qwen2.5:7b 后直接对话 |
| LangChain 框架 | 用 LCEL 管道语法串联组件：`retriever | prompt | llm | parser`，声明式写法，把数据处理流程比作"传送带"，每一步加工半成品 |
| Docker 密钥安全 | 密钥永远不写进镜像（镜像分层可被反编译），只通过运行时环境变量注入（docker-compose 的 env_file） |

### 上传的文档

1. `lianjing-business.md` — 联旌智能业务资料
2. `tech-concepts.md` — 技术概念速查（RAG、向量数据库、Docker、K8s、GPU MIG）
3. `data/reference/` 目录下还有 5 个参考文档（周总结等）

### 测试问答

| 问题 | 关键词命中 | 结果 |
|------|-----------|------|
| 联旌智能的核心产品是什么？ | 3/3 | ✅ |
| Mini EaaS 的免费策略是什么？ | 3/3 | ✅ |
| 什么是 RAG？ | 3/3 | ✅ |
| GPU MIG 切分是什么？ | 4/4 | ✅ |
| 联旌智能的主要客户是谁？ | 4/4 | ✅ |
| Docker 容器和虚拟机有什么区别？ | 3/4 | ✅ |
| Kubernetes 的 Pod 是什么？ | 3/3 | ✅ |

## 本周产出
- 项目：[本地 RAG 知识库](../../projects/rag-knowledge-base/)
  - `gradio_app.py` — RAG Web 界面（支持多轮对话）
  - `langchain_rag.py` — LangChain LCEL 链版本
  - `simple_rag.py` — 纯本地 jieba + TF-IDF 检索演示
  - `evaluate_rag.py` — 检索质量评估脚本
  - `manage_docs.py` — 文档管理工具（增/删/列/重建）
  - `Dockerfile` + `docker-compose.yml` — 容器化方案
  - `chroma_db_gradio/` — 向量数据库（持久化）

## 量化数据
| 指标 | 目标 | 实际 |
|------|------|------|
| commit 次数 | 7 | 7 |
| 学习时长 | 15h | 18h |
| 代码行数 | 200 | 300+ |
| 上传文档数 | 3 | 7（含 reference 目录） |
| 成功问答次数 | 10 | 20+ |

## 为什么这个项目重要？

联旌智能帮高校部署 DeepSeek 等大模型，而 RAG 知识库是企业/高校落地 AI 最常见的需求。作为实习生，能独立完成 RAG 系统搭建，就能在实施/支持环节提供实际价值。

## 重点场景（结合运维能力）

### 场景 1：用 Shell 处理 RAG 服务日志
100GB 日志文件中统计报错最多的模块：
```bash
grep "Error" rag-service.log | awk '{print $5}' | sort | uniq -c | sort -nr | head -10
```

### 场景 2：性能排查——为什么检索很慢？
- 查 CPU Load（`htop`）：Load 高说明 CPU 瓶颈（embedding 计算慢）
- 查 iowait（`top` 里的 wa 列）：高说明磁盘 IO 瓶颈（ChromaDB 读向量文件慢）
- 查内存（`free -m`）：不够的话 ChromaDB 要频繁 swap

### 场景 3：Docker 打包 RAG 应用
把整个 RAG 系统打包成一个可交付的容器镜像。这正是联旌帮客户部署时的实际流程。

## 反思与下周计划

### 做得好的地方
- 走完了 RAG 从 0 到交付的完整链路
- 用评估脚本量化了检索质量（Hit Rate@3 = 100%），而不是光凭感觉说"效果不错"
- Docker 安全方案正确（密钥不打包进镜像）

### 需要改进的地方
- 向量库重复数据问题说明操作前没想清楚再动手，导致反复写入
- 项目里废弃的文件（`rag.py`、`ingest.py`）没有清理，职责不清晰
- 文档数量只有 2 个主文档，太少导致分块后内容覆盖面不够

### 下周重点关注（大模型 API + Agent）
- 本地模型 vs 云端 API 的对比
- Agent 范式：ReAct / Tool Use / Memory
- Function Calling：模型调用外部工具
- 将 RAG 包装为 API 服务（而不仅是网页界面）
