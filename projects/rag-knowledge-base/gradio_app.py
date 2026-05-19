"""
RAG 知识库 - Gradio Web 界面
目标：将之前的 RAG 系统包装成可视化网页，支持浏览器对话交互

启动流程：
  1. 检查向量库是否存在
     - 存在 → 直接加载
     - 不存在 → 自动读取 data/*.md → 分块 → 向量化 → 保存 → 加载
  2. 构建 RAG 链
  3. 启动 Gradio 网页服务
"""

import os
from dotenv import load_dotenv

load_dotenv()  # 自动加载 .env 文件中的环境变量

import gradio as gr
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.chat_models import ChatTongyi
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter

# ==========================================
# 路径配置
# ==========================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data")
DB_PATH = os.path.join(SCRIPT_DIR, "chroma_db_gradio")

# ==========================================
# 第一步：获取 API Key
# ==========================================
api_key = os.environ.get("DASHSCOPE_API_KEY")
if not api_key:
    raise ValueError("未找到 DASHSCOPE_API_KEY 环境变量，请检查 .env 文件")

embeddings = DashScopeEmbeddings(dashscope_api_key=api_key)

# ==========================================
# 第二步：加载或创建向量数据库
# ==========================================
if os.path.exists(DB_PATH):
    print("=== 检测到已有向量库，直接加载... ===")
    vector_store = Chroma(
        persist_directory=DB_PATH,
        embedding_function=embeddings,
        collection_name="gradio_rag",
    )
    print(f"向量数据库加载完成: {DB_PATH}")
else:
    print("=== 未检测到向量库，开始初始化... ===")
    print("（首次启动较慢，需要向量化所有文档）")

    # 读取文档
    loader = DirectoryLoader(
        DATA_DIR,
        glob="*.md",
        loader_cls=lambda p: TextLoader(p, encoding="utf-8")
    )
    documents = loader.load()
    print(f"共加载 {len(documents)} 个文档")

    # 分块
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks = text_splitter.split_documents(documents)
    print(f"共分成 {len(chunks)} 个文本块")

    # 向量化并保存
    vector_store = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=DB_PATH,
        collection_name="gradio_rag",
    )
    print(f"向量数据库创建完成: {DB_PATH}")

# ==========================================
# 第三步：构建 RAG 链（LCEL）
# ==========================================
print("\n=== 构建 RAG 链... ===")

retriever = vector_store.as_retriever(search_kwargs={"k": 3})

prompt = ChatPromptTemplate.from_template("""你是一个基于检索资料的问答助手。请只使用参考资料来回答问题。

如果资料中没有相关信息，请明确说明"资料中没有相关信息"，不要编造答案。

对话历史：
{chat_history}

参考资料：
{context}

问题：{question}

回答：""")

llm = ChatTongyi(model="qwen-plus", temperature=0, dashscope_api_key=api_key)

def format_chat_history(history):
    """将 Gradio 的 [[user, ai], ...] 格式转为可读对话历史字符串"""
    if not history:
        return "无"
    lines = []
    for user_msg, ai_msg in history[-4:]:  # 只保留最近 4 轮，避免 prompt 过长
        lines.append(f"用户: {user_msg}")
        lines.append(f"助手: {ai_msg}")
    return "\n".join(lines)

rag_chain = (
    {"context": itemgetter("question") | retriever, "question": itemgetter("question"), "chat_history": itemgetter("chat_history")}
    | prompt
    | llm
    | StrOutputParser()
)
print("RAG 链构建完成！\n")

# ==========================================
# 第四步：Gradio 界面
# ==========================================

def respond(message, history):
    """
    核心回调函数，支持多轮对话。
    参数:
        message: 用户当前输入的消息（字符串）
        history: 之前的对话历史 [[用户消息, AI回复], ...]
    返回:
        AI 的回答（字符串）
    """
    try:
        chat_history = format_chat_history(history)
        answer = rag_chain.invoke({"question": message, "chat_history": chat_history})
        return answer
    except Exception as e:
        return f"出错了: {str(e)}"

demo = gr.ChatInterface(
    fn=respond,
    title="RAG 知识库问答",
    description="基于联旌实习准备资料的知识库系统 — 使用 LangChain + DashScope + ChromaDB\n支持多轮对话，可以直接追问（如'那GPU怎么切分？'）",
    examples=["联旌智能的核心产品是什么？", "RAG 是什么？", "GPU MIG 切分有什么用？", "你们的客户主要是谁？"],
)

if __name__ == "__main__":
    demo.launch()
