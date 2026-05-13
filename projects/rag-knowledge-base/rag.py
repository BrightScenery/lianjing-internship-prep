import os
import chromadb
import ollama

# ChromaDB 数据目录：始终存在脚本同级目录，不管从哪运行
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "chroma_db")

def get_embedding(text):
    """用 bge-m3 模型把一段文字变成向量"""
    resp = ollama.embed(model="bge-m3", input=text)
    return resp["embeddings"][0]

# 准备知识库文档
documents = [
    "联旌智能科技（上海）有限公司专注于高性能计算与GPU算力调度平台。核心产品是EaaS平台，整合HPC、AI和大数据。",
    "Mini EaaS是联旌的轻量版产品，面向0-8节点小型集群，0-2节点免费。",
    "联旌智能是华为认证ISV合作伙伴，获鲲鹏双认证和昇腾认证。产品原生支持x86、ARM、GPU、NPU、DCU等异构算力。",
    "联旌的客户主要是高校、政府和科研院所，包括兰州大学、合肥工业大学等。",
    "EaaS平台支持容器和虚拟机双引擎，提供自研的多级调度技术，支持GPU透传、共享、vGPU和MIG切分。"
]

# 创建 ChromaDB 客户端（数据存在本地文件夹，关掉不丢）
client = chromadb.PersistentClient(path=DB_PATH)

# 创建集合，不指定 embedding_function，我们手动传向量
collection = client.get_or_create_collection(name="lianjing_docs")

# 手动算向量 + 存入 ChromaDB
ids = []
docs = []
embeddings = []
for i, doc in enumerate(documents):
    ids.append(f"doc_{i}")
    docs.append(doc)
    embeddings.append(get_embedding(doc))

collection.add(ids=ids, documents=docs, embeddings=embeddings)
print(f"已将 {len(documents)} 条文档建立向量索引！")

# === 问答阶段 ===

def ask_question(question, n_results=2):
    """检索相关文档，交给LLM生成回答"""
    # 1. 手动把问题变成向量
    query_vec = get_embedding(question)

    # 2. 用向量检索最相关的文档
    results = collection.query(
        query_embeddings=[query_vec],
        n_results=n_results
    )

    context_docs = results["documents"][0]

    print(f"\n【检索到的参考资料】（共 {len(context_docs)} 条）")
    for i, doc in enumerate(context_docs):
        print(f"  [{i+1}] {doc}")

    # 3. 拼装 Prompt
    context_text = "\n".join(context_docs)
    prompt = f"""请根据以下参考资料回答问题。请根据参考资料并结合你自己的知识来回答。如果资料中没有相关信息，请说明。请用一两句话简短回答。

参考资料：
{context_text}

问题：{question}

回答："""

    # 4. 调用 LLM 生成回答
    response = ollama.chat(
        model="qwen3:4b",
        messages=[{"role": "user", "content": prompt}]
    )
    answer = response["message"]["content"]
    print(f"\n【回答】{answer}")

# === 测试几个问题 ===
questions = [
    "联旌的轻量产品叫什么？",
    "联旌和华为是什么关系？",
    "GPU怎么分配给多个任务？",
    "你们支持docker吗？"
]

for q in questions:
    print(f"\n{'='*50}")
    print(f"问题: {q}")
    ask_question(q)
