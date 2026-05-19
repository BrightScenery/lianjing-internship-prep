"""
RAG 系统评估脚本
目标：用预设的问题-答案对，评估检索准确率和回答质量

原理：
  1. 准备一组测试问题 + 预期答案（ground truth）
  2. 对每个问题，检查检索回来的文档是否包含关键信息（检索准确率）
  3. 记录每次检索的 top-k 文档和相关性
  4. 输出评估报告

这不是"让 LLM 给自己打分"，而是用已知答案来判断检索是否命中。
"""

import os
from dotenv import load_dotenv

load_dotenv()

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_chroma import Chroma

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(SCRIPT_DIR, "chroma_db_gradio")
DATA_DIR = os.path.join(SCRIPT_DIR, "data")

# ==========================================
# 1. 加载向量库
# ==========================================
api_key = os.environ.get("DASHSCOPE_API_KEY")
if not api_key:
    raise ValueError("未找到 DASHSCOPE_API_KEY 环境变量")

embeddings = DashScopeEmbeddings(dashscope_api_key=api_key)

if not os.path.exists(DB_PATH):
    print("=== 向量库不存在，正在创建... ===")
    loader = DirectoryLoader(DATA_DIR, glob="*.md", loader_cls=lambda p: TextLoader(p, encoding="utf-8"))
    documents = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    chunks = text_splitter.split_documents(documents)
    Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=DB_PATH, collection_name="gradio_rag")
    print("向量库创建完成")

vector_store = Chroma(persist_directory=DB_PATH, embedding_function=embeddings, collection_name="gradio_rag")
retriever = vector_store.as_retriever(search_kwargs={"k": 3})

# ==========================================
# 2. 定义测试集
# ==========================================
# 每个测试用例包含：问题、关键词（用于判断检索是否命中）、预期答案摘要
test_cases = [
    {
        "question": "联旌智能的核心产品是什么？",
        "keywords": ["EaaS", "产品", "平台"],
        "expected_summary": "EaaS 平台，整合 HPC + AI + 大数据",
    },
    {
        "question": "Mini EaaS 的免费策略是什么？",
        "keywords": ["Mini", "免费", "0-2节点"],
        "expected_summary": "0-2节点免费",
    },
    {
        "question": "什么是 RAG？",
        "keywords": ["RAG", "检索增强生成", "开卷考试"],
        "expected_summary": "检索增强生成，先检索再生成回答",
    },
    {
        "question": "GPU MIG 切分是什么？",
        "keywords": ["MIG", "切分", "A100", "共享"],
        "expected_summary": "把物理 GPU 切成多个独立实例",
    },
    {
        "question": "联旌智能的主要客户是谁？",
        "keywords": ["高校", "政府", "科研院所", "兰州大学"],
        "expected_summary": "高校、政府、科研院所",
    },
    {
        "question": "Docker 容器和虚拟机有什么区别？",
        "keywords": ["容器", "虚拟机", "内核", "轻量"],
        "expected_summary": "容器共享宿主机内核，更轻量",
    },
    {
        "question": "Kubernetes 的 Pod 是什么？",
        "keywords": ["Pod", "最小部署单元", "容器"],
        "expected_summary": "K8s 的最小部署单元",
    },
]

# ==========================================
# 3. 执行评估
# ==========================================
def check_hit(retrieved_docs, keywords):
    """
    判断检索结果是否"命中"：top-k 文档中是否有包含关键词的。
    这是简化版的 Hit Rate@K 指标。
    """
    hit_keywords = []
    doc_texts = " ".join([doc.page_content.lower() for doc in retrieved_docs])
    for kw in keywords:
        if kw.lower() in doc_texts:
            hit_keywords.append(kw)
    return hit_keywords

print("=" * 70)
print("RAG 检索评估报告")
print("=" * 70)
print(f"测试用例数: {len(test_cases)}")
print(f"检索策略: Top-K (K=3)")
print(f"向量库: {DB_PATH}")
print("=" * 70)

total_hits = 0
total_keywords = 0
matched_keywords = 0

results = []

for i, tc in enumerate(test_cases, 1):
    print(f"\n--- 测试 {i}/{len(test_cases)} ---")
    print(f"问题: {tc['question']}")

    docs = retriever.invoke(tc["question"])

    hit_keywords = check_hit(docs, tc["keywords"])
    hit_rate = len(hit_keywords) / len(tc["keywords"]) * 100

    is_hit = len(hit_keywords) > 0
    total_hits += 1 if is_hit else 0
    total_keywords += len(tc["keywords"])
    matched_keywords += len(hit_keywords)

    status = "✅ HIT" if is_hit else "❌ MISS"
    print(f"关键词命中: {hit_keywords}/{tc['keywords']} ({hit_rate:.0f}%) → {status}")

    # 打印检索到的文档来源
    print(f"检索到 {len(docs)} 个片段:")
    for j, doc in enumerate(docs):
        source = doc.metadata.get("source", "unknown")
        preview = doc.page_content[:80]
        print(f"  [{j+1}] {os.path.basename(source)}: {preview}...")

    results.append({
        "question": tc["question"],
        "hit": is_hit,
        "hit_keywords": hit_keywords,
        "total_keywords": len(tc["keywords"]),
        "n_docs": len(docs),
    })

# ==========================================
# 4. 汇总报告
# ==========================================
print("\n" + "=" * 70)
print("评估结果汇总")
print("=" * 70)

hit_rate_at_k = total_hits / len(test_cases) * 100
keyword_recall = matched_keywords / total_keywords * 100

print(f"Hit Rate@3: {total_hits}/{len(test_cases)} = {hit_rate_at_k:.1f}%")
print(f"关键词召回率: {matched_keywords}/{total_keywords} = {keyword_recall:.1f}%")

print(f"\n详细结果:")
for i, r in enumerate(results, 1):
    status = "✅" if r["hit"] else "❌"
    print(f"  {status} Q{i}: {r['question'][:40]}... → 命中 {len(r['hit_keywords'])}/{r['total_keywords']} 关键词")

print("\n" + "=" * 70)
print("结论")
print("=" * 70)

if hit_rate_at_k >= 80:
    print("检索质量良好，可以用于生产环境。")
elif hit_rate_at_k >= 60:
    print("检索质量一般，建议优化分块策略或增加文档数量。")
else:
    print("检索质量较差，需要排查：")
    print("  1. 文档内容是否覆盖了测试问题")
    print("  2. 分块大小是否合适（当前 chunk_size=800）")
    print("  3. Embedding 模型是否支持中文")
