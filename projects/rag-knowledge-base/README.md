# 项目4：本地 RAG 知识库

> **对应周次**：第4周（5.13 - 5.19）
> **技术栈**：LangChain + DashScope API + ChromaDB + Docker + Gradio
> **学习目标**：掌握 RAG 原理，能独立搭建本地知识库问答系统

## 项目说明

搭建一个本地 RAG（检索增强生成）知识库：
1. 上传 Markdown 文档到 `data/` 目录
2. 文档分块并向量化存入 ChromaDB
3. 用户提问时，先检索相关文档片段，再交给 LLM 生成回答
4. Gradio Web 界面可视化交互
5. 用 Docker 打包，一键部署

## 为什么做这个项目

这是**最能直接对标目标公司业务场景的项目**。根据公开信息，联旌智能帮合肥工业大学等高校部署了 DeepSeek 大模型，而 RAG 知识库是企业/高校落地 AI 最常见的需求——让大模型基于私有数据回答问题。

作为实习生，如果能**独立完成一个 RAG 系统的搭建和交付**，就能在实施/支持环节提供实际价值。

## 文件列表

| 文件 | 说明 |
|------|------|
| `gradio_app.py` | **主入口** — RAG Web 界面，支持多轮对话 |
| `langchain_rag.py` | LangChain LCEL 链版本（终端交互式） |
| `simple_rag.py` | 纯本地 jieba + TF-IDF 检索演示（不需要网络） |
| `evaluate_rag.py` | 检索质量评估脚本（Hit Rate@K） |
| `manage_docs.py` | 文档管理工具（list/add/rebuild/status） |
| `rag.py` | 最初版本（Ollama 本地方案，已废弃，保留作参考） |
| `ingest.py` | 手动入库脚本（已废弃，被 gradio_app.py 自动逻辑替代） |
| `debug_retrieval.py` | 检索诊断工具 |
| `rebuild_and_test.py` | 重建向量库并测试 |
| `Dockerfile` | Docker 镜像构建文件 |
| `docker-compose.yml` | Docker 编排（env_file 安全注入密钥） |
| `.dockerignore` | 构建忽略规则 |
| `requirements.txt` | Python 依赖 |
| `data/` | 文档目录（.md 文件） |
| `chroma_db_gradio/` | 向量数据库（持久化存储） |

## 运行方式

```bash
# 确保 .env 文件中有 DASHSCOPE_API_KEY

# 方式1：本地运行
pip install -r requirements.txt
python gradio_app.py

# 方式2：Docker 运行
docker compose up -d

# 文档管理
python manage_docs.py list        # 查看已有文档
python manage_docs.py add xxx.md  # 添加文档
python manage_docs.py rebuild     # 重建向量库
python manage_docs.py status      # 查看状态

# 评估
python evaluate_rag.py
```

## 技术架构图

```
用户提问（浏览器）
         ↓
    Gradio Web 界面
         ↓
    [检索器] → ChromaDB（向量数据库）
         ↓ 检索 top-3 相关片段
    [Prompt] 拼接：角色 + 历史 + 资料 + 问题
         ↓
    [LLM] → DashScope qwen-plus
         ↓
    生成回答 → 展示在网页
```

## 学到的概念

| 概念 | 理解 |
|------|------|
| RAG 原理 | 两阶段：检索 + 生成。检索质量决定回答质量，开卷考试类比 |
| 向量数据库 | ChromaDB 存储向量 + HNSW 索引，语义相似则距离近 |
| 文本分块 | RecursiveCharacterTextSplitter 递归切分，chunk_overlap 防止断裂 |
| Embedding | 文本→高维向量，text-embedding-v3 输出 1024 维 |
| LangChain LCEL | 用 \| 管道符串联组件的声明式写法 |
| Docker 安全 | 密钥不进镜像，env_file 运行时注入 |
| 多轮对话 | history 拼入 prompt，检索仍基于当前 message |
