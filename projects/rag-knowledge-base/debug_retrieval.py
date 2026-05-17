"""
RAG 检索诊断脚本 — 查看检索器到底找到了什么
运行: python debug_retrieval.py
需要设置 DASHSCOPE_API_KEY 环境变量
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_chroma import Chroma

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data")
DB_PATH = os.path.join(SCRIPT_DIR, "chroma_db_gradio")

api_key = os.environ.get("DASHSCOPE_API_KEY")
if not api_key:
    api_key = input("请输入通义 API Key: ").strip()

embeddings = DashScopeEmbeddings(dashscope_api_key=api_key)
vector_store = Chroma(persist_directory=DB_PATH, embedding_function=embeddings, collection_name="gradio_rag")
retriever = vector_store.as_retriever(search_kwargs={"k": 5})

test_queries = [
    "什么是RAG",
    "什么是 RAG（检索增强生成）",
    "docker的优势是什么",
    "Docker的优势是是什么",
    "联旌智能做什么的",
    "GPU MIG是什么",
]

for q in test_queries:
    print(f"\n{'='*60}")
    print(f"查询: {q}")
    print(f"{'='*60}")
    docs = retriever.invoke(q)
    for i, doc in enumerate(docs):
        source = doc.metadata.get("source", "unknown")
        # 只取文件名
        if isinstance(source, str):
            source = os.path.basename(source)
        print(f"\n  --- 结果 {i+1} ---")
        print(f"  来源: {source}")
        print(f"  内容: {doc.page_content[:200]}...")
