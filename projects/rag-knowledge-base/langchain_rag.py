"""
用 LangChain 重写 RAG 知识库
目标：理解框架如何简化"文档加载→分块→向量化→检索→生成"的整条流水线
"""

import os

# 所有路径基于脚本所在目录，保证从任何位置运行都不会出错
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data")
DB_PATH = os.path.join(SCRIPT_DIR, "chroma_db_langchain")

# ==========================================
# 第一步：引入 LangChain 组件
# ==========================================

# --- 文档加载器：自动读取目录下所有文件 ---
from langchain_community.document_loaders import DirectoryLoader, TextLoader

# --- 文本分块器：按字符数递归切分 ---
from langchain_text_splitters import RecursiveCharacterTextSplitter

# --- Embedding：用 Ollama 跑本地 bge-m3 模型 ---
from langchain_ollama import OllamaEmbeddings

# --- 向量数据库：Chroma，持久化到本地文件 ---
from langchain_chroma import Chroma

# --- LLM：用 Ollama 跑本地 qwen3.5:4b ---
from langchain_community.chat_models import ChatTongyi

# --- Prompt 模板：用变量占位，避免手动拼字符串 ---
from langchain_core.prompts import ChatPromptTemplate

# --- 把检索器和 LLM 串成一条链 ---
from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# ==========================================
# 第二步：加载文档
# ==========================================
print("=== 第1步：加载文档 ===")
# DirectoryLoader 会自动读取 DATA_DIR 下的所有 .md 文件
# glob="*.md" 表示只匹配 .md 后缀的文件
loader = DirectoryLoader(DATA_DIR, glob="*.md", loader_cls=lambda p: TextLoader(p, encoding="utf-8"))
documents = loader.load()
print(f"共加载 {len(documents)} 个文档")
# 每个 document 对象都有 .page_content（文本内容）和 .metadata（来源等元信息）
for doc in documents:
    print(f"  - {doc.metadata.get('source', 'unknown')}: {len(doc.page_content)} 字符")

# ==========================================
# 第三步：文本分块
# ==========================================
print("\n=== 第2步：文本分块 ===")
# chunk_size=800 每个块 800 字符，包含更完整的知识点
# chunk_overlap=150 重叠 150 字符，减少信息丢失
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150,
    separators=["\n\n", "\n", " ", ""]  # 递归切：先按空行，再按换行，再按空格，最后按字符
)
chunks = text_splitter.split_documents(documents)
print(f"共分成 {len(chunks)} 个文本块")

# ==========================================
# 第四步：向量化 + 存入 ChromaDB
# ==========================================
print("\n=== 第3步：向量化 + 存入 ChromaDB ===")
# OllamaEmbeddings 内部会调用 ollama.embed(model="bge-m3", input=text)，我们不用自己拼 API 了
embeddings = OllamaEmbeddings(model="bge-m3")

# Chroma 会自动把 chunks 里的文本向量化并存入 DB_PATH
# from_documents 等价于：遍历 chunks → 调 embedding 模型算向量 → 存入 ChromaDB
vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=DB_PATH,
    collection_name="langchain_rag",
)
print(f"向量化完成，数据保存在: {DB_PATH}")

# ==========================================
# 第五步：构建检索 + 生成的"链"
# ==========================================
print("\n=== 第4步：构建 RAG 链 ===")

# --- 5.1 定义 Prompt 模板 ---
# input_variables 表示模板里有两个占位符：context 和 input
# context 会被检索到的文档片段填充，input 是用户的问题
prompt = ChatPromptTemplate.from_template("""你是一个基于检索资料的问答助手。请只使用参考资料来回答问题。

如果资料中没有相关信息，请明确说明"资料中没有相关信息"，不要编造答案。

参考资料：
{context}

问题：{input}

回答：""")

# --- 5.2 初始化 LLM：用 dashscope SDK 直接调通义 API ---
# 这里写一个薄包装类，让 dashscope 能接进 LangChain 的链里
# 优先从环境变量读取 API Key，避免明文暴露在代码中
api_key = os.environ.get("DASHSCOPE_API_KEY")
if not api_key:
    api_key = input("请输入通义 API Key: ").strip()

llm = ChatTongyi(model="qwen-plus", temperature=0, dashscope_api_key=api_key)

# --- 5.3 创建检索器 ---
retriever = vector_store.as_retriever(search_kwargs={"k": 3})

# --- 5.4 用 LCEL 表达式语言构建 RAG 链 ---
# LCEL 是新版 LangChain 的核心：用 | 把组件串成流水线
#
# 流程拆解：
# 1. {"context": retriever, "input": RunnablePassthrough()}：
#    - retriever 拿到输入中的 "input" 值，去检索文档列表，结果赋值给 context
#    - RunnablePassthrough() 把输入原封不动传下去，赋值给 input
# 2. prompt：把 context 和 input 填入模板
# 3. llm：调用 LLM 生成回答
# 4. StrOutputParser()：把 LLM 的原始输出转成纯字符串

# 回答链（只负责生成回答）
answer_chain = (
    {"context": itemgetter("input") | retriever, "input": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)
print("RAG 链构建完成！\n")

# ==========================================
# 第六步：测试问答
# ==========================================
print("=== 开始提问 ===\n")
questions = [
    "WSL2 是什么？",
    "Docker 容器和虚拟机有什么区别？",
    "K8s 的 Pod 是什么？",
    "你们支持哪些异构算力？",
    "chmod 命令是干什么的？",
    "LangChain 是什么？",  # 这个问题资料里没有，看模型会不会编造
]

for q in questions:
    print(f"{'='*60}")
    print(f"问题: {q}")
    print("-" * 60)

    # 先检索，再看回答
    docs = retriever.invoke(q)

    answer = answer_chain.invoke({"input": q})

    print(f"回答: {answer}")

    print(f"\n【参考来源】（共 {len(docs)} 条）")
    for i, doc in enumerate(docs):
        print(f"  [{i+1}] {doc.metadata.get('source', '?')}: {doc.page_content[:80]}...")
    print()
