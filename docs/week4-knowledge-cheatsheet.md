# 第4周知识清单：RAG 知识库系统

> 日期：2026.05.13 - 2026.05.19
> 用途：复习 + 面试准备

---

## 1. RAG（检索增强生成）

### 是什么
RAG = Retrieval-Augmented Generation。让大模型在回答前先查阅私有资料。

### 为什么需要 RAG
普通大模型是"闭卷考试"，只靠训练时记住的知识。RAG 是"开卷考试"，可以翻资料作答。

### 完整流程
```
用户上传文档 → 分块(Chunking) → 向量化(Embedding) → 存入向量数据库
                                                          ↓
用户提问 → 向量化 → 相似度检索(Top-K) → (可选)Reranker 精排
                                                          ↓
拼接 Prompt（角色 + 参考资料 + 对话历史 + 问题）→ LLM 生成回答
```

### 面试常问
- **Q：RAG 和普通大模型的区别？**
  A：普通大模型依赖训练数据，RAG 可以基于私有文档回答，且回答有引用来源。
- **Q：怎么提升 RAG 的检索质量？**
  A：① 优化分块策略（chunk_size + overlap）② 用 Reranker 精排 ③ 增加高质量文档 ④ 选更好的 Embedding 模型

---

## 2. Embedding（文本向量化）

### 是什么
把一段文本转换成一串数字（向量），比如 1024 个浮点数。这个向量编码了文本的语义。

### 关键性质
- 语义相似的文本，向量在空间中的距离就近
- 同一个项目中，入库和检索必须用**同一个** Embedding 模型（维度要一致）
- 维度不是越高越好，存在最优区间

### 常见模型
| 模型 | 维度 | 特点 |
|------|------|------|
| text-embedding-v3（通义） | 1024 | 中英文都好 |
| bge-m3（智源） | 1024 | 中文优化 |
| ada-002（OpenAI） | 1536 | 英文为主 |

---

## 3. 文本分块（Chunking）

### RecursiveCharacterTextSplitter
按"段落 → 句子 → 词 → 字符"的优先级递归切分：
```python
separators=["\n\n", "\n", " ", ""]
```
- 先用空行切，如果切出来还是太大，再用换行切
- 再用空格切，最后兜底按字符切
- 保证一定能切到 ≤ chunk_size

### chunk_overlap 的作用
相邻块之间重叠一部分，防止相关内容被拦腰截断。

### 面试常问
- **Q：chunk_size 设多少合适？**
  A：没有标准答案。太小（<300）语义不完整，太大（>1500）检索噪音大。一般 500-1000 之间，根据文档类型调整。
- **Q：为什么不直接按固定长度切？**
  A：会打断段落、句子的自然边界。Recursive 策略保留语义完整性。

---

## 4. 向量数据库（ChromaDB）

### 是什么
专门存储和检索向量的数据库。核心操作：给一个查询向量，找到距离最近的 K 个向量。

### 底层存储
- `chroma.sqlite3`：SQLite 数据库，存储文档原文和元信息
- `data_level0.bin` / `header.bin` / `link_lists.bin` 等：**HNSW 索引文件**，记录向量间的连接关系，用于快速近似最近邻搜索

### HNSW（Hierarchical Navigable Small World）
一种高效的多层图索引结构。检索时不需要遍历所有向量，而是沿着图"跳"到最近的节点，速度远快于暴力搜索。

### 检索距离算法
- **L2 距离**（欧氏距离）：越小越相似
- **余弦相似度**：越大越相似（看方向不看长度）

### 面试常问
- **Q：ChromaDB 和 MySQL 的区别？**
  A：MySQL 是关系型数据库，按精确匹配或范围查询。ChromaDB 是按向量相似度查找，是"最接近"而不是"完全匹配"。

---

## 5. LangChain 框架

### 是什么
一个把 LLM 应用的各个组件（文档加载、分块、向量化、检索、生成）串联起来的框架。

### LCEL（LangChain Expression Language）
用 `|` 管道符把组件连成流水线：
```python
rag_chain = (
    {"context": itemgetter("question") | retriever, "question": itemgetter("question")}
    | prompt
    | llm
    | StrOutputParser()
)
```

### 关键组件
| 组件 | 作用 |
|------|------|
| DirectoryLoader | 自动读取目录下所有文件 |
| RecursiveCharacterTextSplitter | 递归文本分块 |
| DashScopeEmbeddings / OllamaEmbeddings | 文本向量化 |
| Chroma | 向量数据库 |
| ChatPromptTemplate | Prompt 模板，变量替换 |
| StrOutputParser | 把 LLM 输出转纯字符串 |
| itemgetter | 从输入字典中取字段值 |

### 面试常问
- **Q：为什么要用 LangChain 而不是自己写？**
  A：组件化 + 可替换。换 Embedding 模型只需改一行，不用重写整个流程。但简单场景自己写也能理解原理。

---

## 6. Docker 安全实践

### 密钥管理原则
**密钥永远不写进镜像**，只通过运行时环境变量注入。

### 错误方案
| 方案 | 问题 |
|------|------|
| `COPY .env .env` | 镜像分层永久保留，可被反编译 |
| 构建阶段 RUN 调 API | 构建日志/中间层可能暴露 Key |

### 正确方案
```yaml
# docker-compose.yml
services:
  rag-app:
    env_file: .env          # 运行时注入
    volumes: ./data:/app/data  # 数据持久化
```

### 镜像分层
Dockerfile 的每一条指令生成一个新层。即使后面 `rm` 删除了文件，之前的层仍然存在。用 `docker history` 或 `dive` 可以查看所有层。

---

## 7. Docker Compose

### 是什么
用 YAML 文件定义多容器应用的配置。把 `docker run` 的一长串参数变成可读的配置。

### 关键字段
| 字段 | 作用 |
|------|------|
| `build: .` | 用当前目录 Dockerfile 构建 |
| `ports: "7860:7860"` | 宿主机端口:容器端口 |
| `env_file: .env` | 安全注入环境变量 |
| `volumes: ./path:/app/path` | 数据持久化 |
| `restart: unless-stopped` | 崩溃自动重启 |

---

## 8. 实际运维场景

### 用 Shell 查 RAG 服务日志
```bash
# 统计报错最多的模块
grep "Error" rag-service.log | awk '{print $5}' | sort | uniq -c | sort -nr | head -10
```

### 性能排查
| 瓶颈 | 排查命令 | 指标 |
|------|---------|------|
| CPU | `htop` | Load > CPU核数 = 瓶颈 |
| 磁盘 IO | `top` → wa 列 | iowait > 30% = 瓶颈 |
| 内存 | `free -m` | 可用 < 500MB = 危险 |

---

## 9. 多轮对话的实现

### 问题
之前的 `respond(message, history)` 忽略了 `history` 参数，导致每次回答独立，无法追问。

### 解决
- 在 prompt 模板加入 `{chat_history}` 占位符
- 把 Gradio 的 `[[user, ai], ...]` 格式转为可读字符串
- 只保留最近 4 轮，避免 prompt 过长
- 检索仍只基于当前 `message`，防止历史污染检索

---

## 10. RAG 质量评估

### Hit Rate@K
一组测试问题中，检索到的 top-K 文档里有多少包含了正确答案的关键词。

### 企业交付 RAG 的要求
- 有评估报告（不是"效果不错"而是"Hit Rate@3 = 90%"）
- 有文档管理工具（增/删/重建向量库）
- 有监控日志（记录每次请求的检索质量和响应时间）
