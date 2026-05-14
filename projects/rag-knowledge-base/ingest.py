import os
import glob
import chromadb
import ollama

# ---------- 配置路径 ----------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data")
DB_PATH = os.path.join(SCRIPT_DIR, "chroma_db")

# ---------- 1. 加载文档 ----------
def load_documents(data_dir):
    """读取 data 目录下所有 .md 文件"""
    docs = []
    for filepath in glob.glob(os.path.join(data_dir, "*.md")):
        filename = os.path.basename(filepath)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            docs.append({"filename": filename, "content": content})
            print(f"读取到文档：{filename}，长度 {len(content)} 字符")
    return docs

# ---------- 2. 文本分块 ----------
def chunk_text(text, chunk_size=400, overlap=50):
    """文本分块，支持重叠"""
    chunks = []
    step = chunk_size - overlap
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        if end == len(text):
            break
        start += step
    return chunks

# ---------- 3. 构建索引（ingest） ----------
def ingest():
    """加载文档 → 分块 → 向量化 → 存入 ChromaDB"""
    print("=== 第1步：加载文档 ===")
    all_docs = load_documents(DATA_DIR)
    print(f"共加载 {len(all_docs)} 个文档\n")

    print("=== 第2步：文本分块 ===")
    chunks = []
    for doc in all_docs:
        pieces = chunk_text(doc["content"])
        for piece in pieces:
            chunks.append({"text": piece, "source": doc["filename"]})
    print(f"共分成 {len(chunks)} 个文本块\n")

    print("=== 第3步：初始化 ChromaDB ===")
    client = chromadb.PersistentClient(path=DB_PATH)
    try:
        client.delete_collection(name="learning_docs")
        print("  已删除旧的 learning_docs 集合")
    except:
        pass
    collection = client.get_or_create_collection(name="learning_docs")
    print("  集合 learning_docs 已就绪\n")

    print("=== 第4步：向量化并存入（较慢，请耐心）===")
    ids, texts, embeddings, metadatas = [], [], [], []
    for i, chunk in enumerate(chunks):
        resp = ollama.embed(model="bge-m3", input=chunk["text"])
        vec = resp["embeddings"][0]
        ids.append(f"chunk_{i}")
        texts.append(chunk["text"])
        embeddings.append(vec)
        metadatas.append({"source": chunk["source"]})
        if (i + 1) % 10 == 0:
            print(f"  已处理 {i + 1}/{len(chunks)} 块...")

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )
    print(f"\n完成！共向量化并存储 {len(chunks)} 个文本块")
    print(f"数据保存在: {DB_PATH}\n")

# ---------- 4. 查询与问答 ----------
def get_collection():
    """连接到已有的 ChromaDB 集合"""
    client = chromadb.PersistentClient(path=DB_PATH)
    return client.get_collection(name="learning_docs")

def ask_question(question, n_results=3):
    """提问 → 检索 → 生成回答"""
    print(f"\n{'='*60}")
    print(f"问题: {question}")

    # 1. 获取集合
    collection = get_collection()

    # 2. 向量化问题
    resp = ollama.embed(model="bge-m3", input=question)
    query_vec = resp["embeddings"][0]

    # 3. 检索
    results = collection.query(
        query_embeddings=[query_vec],
        n_results=n_results
    )
    docs = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    # 4. 打印检索到的参考资料
    print(f"\n【检索到 {len(docs)} 条相关文档】")
    for i, (doc, meta, dist) in enumerate(zip(docs, metadatas, distances)):
        print(f"  [{i+1}] 来自 {meta['source']}，相似度: {dist:.4f}")
        print(f"      {doc[:100]}...")

    # 5. 拼装 prompt
    context_text = "\n---\n".join(docs)
    prompt = f"""请根据以下参考资料回答问题。请根据参考资料并结合你自己的知识来回答。如果资料中没有相关信息，请说明。请用一两句话简短回答。

参考资料：
{context_text}

问题：{question}

回答："""

    # 6. 调用 LLM 生成回答
    response = ollama.chat(
        model="qwen3:4b",
        messages=[{"role": "user", "content": prompt}]
    )
    answer = response["message"]["content"]
    print(f"\n【回答】{answer}")

# ---------- 主程序 ----------
if __name__ == "__main__":
    # 第一次运行时，取消下面一行的注释来构建索引
    # 索引建好后，就可以注释掉这行，以后只运行查询
    # ingest()

    # 测试问答（确保已经运行过一次 ingest 生成了索引）
    questions = [
        "WSL2 是什么？",
        "Docker 容器和虚拟机有什么区别？",
        "K8s 的 Pod 是什么？",
        "你们支持哪些异构算力？",
        "chmod 命令是干什么的？",
        "docker-compose 有什么用？",
    ]
    for q in questions:
        ask_question(q)