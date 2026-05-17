"""
RAG 重建向量库 + 检索诊断
运行: python rebuild_and_test.py
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import os
from dotenv import load_dotenv

load_dotenv()  # 自动加载 .env 文件中的环境变量
import shutil
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

# 1. 删除旧库
if os.path.exists(DB_PATH):
    shutil.rmtree(DB_PATH)
    print(f"[1/3] 已删除旧向量库: {DB_PATH}")
else:
    print(f"[1/3] 无需清理（向量库不存在）")

# 2. 重建
print("\n[2/3] 正在重建向量库...")
print(f"  数据目录: {DATA_DIR}")
loader = DirectoryLoader(DATA_DIR, glob="*.md", loader_cls=lambda p: TextLoader(p, encoding="utf-8"))
documents = loader.load()
print(f"  加载文档数: {len(documents)}")

text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150, separators=["\n\n", "\n", " ", ""])
chunks = text_splitter.split_documents(documents)
print(f"  分块数: {len(chunks)}")

embeddings = DashScopeEmbeddings(dashscope_api_key=api_key)
vector_store = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=DB_PATH, collection_name="gradio_rag")
print(f"  向量库已重建: {DB_PATH}")

# 3. 诊断检索
print("\n[3/3] 检索诊断测试...")
retriever = vector_store.as_retriever(search_kwargs={"k": 3})

test_queries = [
    ("什么是RAG", "tech-concepts.md"),
    ("Docker的优势是什么", "tech-concepts.md"),
    ("联旌智能做什么的", "lianjing-business.md"),
    ("GPU MIG是什么", "tech-concepts.md"),
    ("RAG的原理是什么", "tech-concepts.md"),
]

for q, expected in test_queries:
    docs = retriever.invoke(q)
    sources = [os.path.basename(d.metadata.get("source", "")) for d in docs]
    hit = expected in sources
    status = "✅" if hit else "❌"
    print(f"\n  {status} 查询: {q}")
    for i, (doc, src) in enumerate(zip(docs, sources)):
        marker = " <-- 期望" if src == expected else ""
        print(f"    [{i+1}] {src}{marker} | 预览: {doc.page_content[:80]}...")
