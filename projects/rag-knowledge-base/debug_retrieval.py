import os
import chromadb
import ollama

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "chroma_db")

client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_collection(name="learning_docs")

questions = [
    "WSL2 是什么？",
    "Docker 容器和虚拟机有什么区别？",
    "K8s 的 Pod 是什么？",
    "chmod 命令是干什么的？",
]

for q in questions:
    print(f"\n{'='*60}")
    print(f"问题: {q}")

    resp = ollama.embed(model="bge-m3", input=q)
    query_vec = resp["embeddings"][0]

    results = collection.query(
        query_embeddings=[query_vec],
        n_results=3
    )

    docs = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    for i, (doc, meta, dist) in enumerate(zip(docs, metadatas, distances)):
        print(f"\n  [{i+1}] 来源: {meta['source']}, 距离: {dist:.4f}")
        print(f"  {'-'*50}")
        print(f"  {doc}")
        print(f"  {'-'*50}")
