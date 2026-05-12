"""
简单 RAG 检索演示（jieba + TF-IDF 版本）
目标：把文本存入索引，然后根据问题检索最相关的片段
不依赖任何外网下载，纯本地运行
"""

import jieba
from collections import Counter
import math

# 1. 准备知识库内容（模拟联旌智能的公司文档）
documents = [
    "联旌智能科技（上海）有限公司专注于高性能计算与GPU算力调度平台。核心产品是EaaS（Environment as a Service）平台，整合HPC、AI和大数据。",
    "Mini EaaS是联旌的轻量版产品，面向0-8节点小型集群，0-2节点免费。",
    "联旌智能是华为认证ISV合作伙伴，获鲲鹏双认证和昇腾认证。产品原生支持x86、ARM、GPU、NPU、DCU等异构算力。",
    "联旌的客户主要是高校、政府和科研院所，包括兰州大学、合肥工业大学等。",
    "EaaS平台支持容器和虚拟机双引擎，提供自研的多级调度技术，支持GPU透传、共享、vGPU和MIG切分。"
]

# 2. 分词 + 去停用词
stop_words = {"的", "是", "在", "了", "和", "与", "等", "及", "或", "（", "）", "。", "，", ""}

# 对每篇文档分词，得到词列表
tokenized_docs = []
for doc in documents:
    words = [w for w in jieba.lcut(doc) if w not in stop_words]
    tokenized_docs.append(words)

# 3. 计算 TF-IDF 权重
def compute_tfidf(tokenized_docs):
    """计算每篇文档每个词的 TF-IDF 值"""
    num_docs = len(tokenized_docs)

    # 计算 IDF：log(总文档数 / 包含该词的文档数)
    df = {}
    for doc_words in tokenized_docs:
        unique_words = set(doc_words)
        for word in unique_words:
            df[word] = df.get(word, 0) + 1

    idf = {}
    for word, count in df.items():
        idf[word] = math.log(num_docs / count)

    # 计算每篇文档的 TF-IDF
    tfidf_docs = []
    for doc_words in tokenized_docs:
        tf = Counter(doc_words)
        tfidf = {}
        for word, count in tf.items():
            tfidf[word] = count * idf[word]
        tfidf_docs.append(tfidf)

    return tfidf_docs, idf

tfidf_docs, idf = compute_tfidf(tokenized_docs)

print(f"已将 {len(documents)} 条文档建立索引！开始检索测试...\n")

# 4. 检索函数
def retrieve(query, tfidf_docs, idf, n_results=1):
    """根据问题检索最相关的文档"""
    query_words = [w for w in jieba.lcut(query) if w not in stop_words]

    # 计算问题的 TF-IDF
    query_tf = Counter(query_words)
    query_tfidf = {}
    for word, count in query_tf.items():
        if word in idf:
            query_tfidf[word] = count * idf[word]

    # 计算每篇文档与问题的余弦相似度
    scores = []
    for i, doc_tfidf in enumerate(tfidf_docs):
        common_words = set(query_tfidf.keys()) & set(doc_tfidf.keys())

        dot_product = sum(query_tfidf[w] * doc_tfidf[w] for w in common_words)
        query_norm = math.sqrt(sum(v ** 2 for v in query_tfidf.values()))
        doc_norm = math.sqrt(sum(v ** 2 for v in doc_tfidf.values()))

        if query_norm > 0 and doc_norm > 0:
            similarity = dot_product / (query_norm * doc_norm)
        else:
            similarity = 0

        scores.append((i, similarity))

    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:n_results]

# 5. 测试检索
questions = [
    "联旌的核心产品是什么？",
    "Mini EaaS 多少钱？",
    "联旌和华为是什么关系？",
    "GPU 怎么分配给多个任务用？",
]

for question in questions:
    results = retrieve(question, tfidf_docs, idf, n_results=1)
    idx, score = results[0]
    print(f"问题: {question}")
    print(f"  匹配到的文档: {documents[idx]}")
    print(f"  相似度: {score:.4f}（越大越相关）\n")