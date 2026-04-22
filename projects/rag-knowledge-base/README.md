# 项目4：本地 RAG 知识库

> **对应周次**：第4-5周（5.13 - 5.26）
> **技术栈**：LangChain + Ollama + ChromaDB + Docker
> **学习目标**：掌握 RAG 原理，能独立搭建本地知识库问答系统

## 项目说明

搭建一个本地 RAG（检索增强生成）知识库：
1. 上传专业文档（PDF / Markdown）
2. 文档分块并向量化存入 ChromaDB
3. 用户提问时，先检索相关文档片段，再交给 LLM 生成回答
4. 用 Docker 打包，一键部署

## 为什么做这个项目

这是**最能直接对标联旌智能业务场景的项目**。根据公开信息，联旌智能帮合肥工业大学等高校部署了 DeepSeek 大模型，而 RAG 知识库是企业/高校落地 AI 最常见的需求——让大模型基于私有数据回答问题。

作为实习生，我可能不会直接接触核心调度代码，但如果我能**独立完成一个 RAG 系统的搭建和交付**，就能在实施/支持环节提供实际价值。这正是 HR 所说的"从打下手开始"的最佳切入点。

## 文件列表

- `rag.py` — RAG 核心代码
- `agent.py` — Agent 扩展代码
- `Dockerfile` — 容器化文件
- `data/` — 测试文档（上传的 PDF/Markdown）

## 运行方式

```bash
# 本地运行
python rag.py

# Docker 运行
docker build -t rag-app .
docker run -p 7860:7860 rag-app
```

## 技术架构图

```
用户提问
    ↓
[检索器] → ChromaDB（向量数据库）
    ↓ 检索相关文档片段
[LLM] → Ollama（本地 Qwen2.5）
    ↓
生成回答
```

## 学到的概念

| 概念 | 理解 |
|------|------|
| RAG 原理 | |
| 向量数据库 | |
| 文本分块（Chunking） | |
| Embedding | |
| 本地模型部署（Ollama） | |
| Prompt Engineering | |
| Agent / Function Calling | |
