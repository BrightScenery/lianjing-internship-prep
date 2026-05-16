"""
RAG 知识库 - Gradio Web 界面
目标：将之前的 RAG 系统包装成可视化网页，支持浏览器对话交互
"""

import os
import gradio as gr
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ==========================================
# 路径配置
# ==========================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data")
DB_PATH = os.path.join(SCRIPT_DIR, "chroma_db_gradio")

# ==========================================
# 第一步：加载文档 → 分块 → 向量化
# ==========================================
print("=== 正在加载文档... ===")
loader = DirectoryLoader(
    DATA_DIR,
    glob="*.md",
    loader_cls=lambda p: TextLoader(p, encoding="utf-8")
)
documents = loader.load()
print(f"共加载 {len(documents)} 个文档")

print("\n=== 正在分块... ===")
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150,
    separators=["\n\n", "\n", " ", ""]
)
chunks = text_splitter.split_documents(documents)
print(f"共分成 {len(chunks)} 个文本块")

# 这里需要设置 DASHSCOPE_API_KEY
api_key = os.environ.get("DASHSCOPE_API_KEY")
if not api_key:
    api_key = input("\n请输入通义 API Key: ").strip()

from langchain_community.chat_models import ChatTongyi

print("\n=== 正在向量化并构建索引... ===")
# DashScopeEmbeddings 默认使用 text-embedding-v3 模型
# 注意：需要显式传入 dashscope_api_key，环境变量名可能不被识别
embeddings = DashScopeEmbeddings(dashscope_api_key=api_key)
vector_store = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory=DB_PATH,
    collection_name="gradio_rag",
)
print(f"向量数据库就绪，数据保存在: {DB_PATH}")

# ==========================================
# 第二步：构建 RAG 链（LCEL）
# ==========================================
print("\n=== 构建 RAG 链... ===")

retriever = vector_store.as_retriever(search_kwargs={"k": 3})

from operator import itemgetter

prompt = ChatPromptTemplate.from_template("""你是一个基于检索资料的问答助手。请只使用参考资料来回答问题。

如果资料中没有相关信息，请明确说明"资料中没有相关信息"，不要编造答案。

参考资料：
{context}

问题：{question}

回答：""")

llm = ChatTongyi(model="qwen-plus", temperature=0, dashscope_api_key=api_key)

rag_chain = (
    {"context": itemgetter("question") | retriever, "question": itemgetter("question")}
    | prompt
    | llm
    | StrOutputParser()
)
print("RAG 链构建完成！\n")

# ==========================================
# 第三步：Gradio 界面
# ==========================================

def respond(message, history):
    """
    这是 Gradio ChatInterface 的核心回调函数。
    参数:
        message: 用户当前输入的消息（字符串）
        history: 之前的对话历史 [[用户消息, AI回复], ...]
    返回:
        AI 的回答（字符串）
    """
    try:
        answer = rag_chain.invoke({"question": message})
        return answer
    except Exception as e:
        return f"出错了: {str(e)}"

# gr.ChatInterface 会自动生成:
# - 聊天消息显示区
# - 底部输入框
# - 发送按钮
# - 清空对话按钮
demo = gr.ChatInterface(
    fn=respond,
    title="RAG 知识库问答",
    description="基于联旌实习准备资料的知识库系统 — 使用 LangChain + DashScope + ChromaDB",
)

if __name__ == "__main__":
    # launch() 会在本地启动一个 Web 服务
    # 默认地址: http://127.0.0.1:7860
    demo.launch()
