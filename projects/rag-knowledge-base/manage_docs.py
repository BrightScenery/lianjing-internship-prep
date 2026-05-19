"""
RAG 文档管理工具
目标：提供增/删/列/重建向量库的功能，无需手动操作代码

企业场景：客户说"我新加了一份产品手册，帮我更新知识库"
——你不能让人去改 Python 代码，应该有一个清晰的命令行工具。

用法：
  python manage_docs.py list          # 列出当前数据目录的文档
  python manage_docs.py add xxx.md    # 添加文档到 data/ 目录
  python manage_docs.py rebuild       # 删除旧向量库，重新向量化
  python manage_docs.py status        # 查看向量库和文档状态
"""

import os
import sys
import shutil
from dotenv import load_dotenv

load_dotenv()

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "data")
DB_PATH = os.path.join(SCRIPT_DIR, "chroma_db_gradio")


def cmd_list():
    """列出 data/ 目录下的所有文档"""
    if not os.path.exists(DATA_DIR):
        print("data/ 目录不存在")
        return
    files = [f for f in os.listdir(DATA_DIR) if f.endswith((".md", ".txt"))]
    if not files:
        print("data/ 目录下没有文档")
        return
    print(f"data/ 目录下的文档（共 {len(files)} 个）:")
    for f in sorted(files):
        size = os.path.getsize(os.path.join(DATA_DIR, f))
        print(f"  {f} ({size} bytes)")


def cmd_add(filename):
    """
    添加文档：如果传入的是绝对路径或相对路径，复制到 data/ 目录
    如果文件已在 data/ 下，跳过
    """
    src = os.path.abspath(filename)
    if not os.path.exists(src):
        print(f"错误：文件 {filename} 不存在")
        sys.exit(1)
    dst = os.path.join(DATA_DIR, os.path.basename(filename))
    if os.path.exists(dst):
        print(f"文件 {os.path.basename(filename)} 已存在于 data/ 目录，跳过")
        return
    shutil.copy2(src, dst)
    print(f"已添加 {os.path.basename(filename)} 到 data/ 目录")
    print("注意：添加文档后需要执行 'rebuild' 重建向量库才能生效")


def cmd_rebuild():
    """删除旧向量库，重新向量化"""
    api_key = os.environ.get("DASHSCOPE_API_KEY")
    if not api_key:
        print("错误：未设置 DASHSCOPE_API_KEY 环境变量")
        sys.exit(1)

    # 删除旧库
    if os.path.exists(DB_PATH):
        shutil.rmtree(DB_PATH)
        print(f"已删除旧向量库: {DB_PATH}")

    # 引入 LangChain 组件（需要时才加载，避免 list 命令慢）
    from langchain_community.document_loaders import DirectoryLoader, TextLoader
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.embeddings import DashScopeEmbeddings
    from langchain_chroma import Chroma

    # 加载文档
    loader = DirectoryLoader(DATA_DIR, glob="*.md", loader_cls=lambda p: TextLoader(p, encoding="utf-8"))
    documents = loader.load()
    print(f"加载 {len(documents)} 个文档")

    # 分块
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=150)
    chunks = text_splitter.split_documents(documents)
    print(f"分成 {len(chunks)} 个文本块")

    # 向量化
    embeddings = DashScopeEmbeddings(dashscope_api_key=api_key)
    Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=DB_PATH, collection_name="gradio_rag")
    print(f"向量库重建完成: {DB_PATH}")


def cmd_status():
    """查看系统状态"""
    # 向量库状态
    if os.path.exists(DB_PATH):
        size = sum(os.path.getsize(os.path.join(dp, f)) for dp, dn, filenames in os.walk(DB_PATH) for f in filenames)
        print(f"向量库: 存在 ({size / 1024:.1f} KB)")
    else:
        print("向量库: 不存在（需要执行 rebuild）")

    # 文档状态
    if os.path.exists(DATA_DIR):
        files = [f for f in os.listdir(DATA_DIR) if f.endswith((".md", ".txt"))]
        print(f"文档数: {len(files)}")
    else:
        print("data/ 目录: 不存在")


def print_usage():
    print("用法: python manage_docs.py <命令> [参数]")
    print()
    print("命令:")
    print("  list        列出 data/ 目录的文档")
    print("  add <文件>   添加文档到 data/ 目录")
    print("  rebuild     删除旧向量库，重新向量化")
    print("  status      查看系统状态")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_usage()
        sys.exit(1)

    command = sys.argv[1]

    if command == "list":
        cmd_list()
    elif command == "add":
        if len(sys.argv) < 3:
            print("错误：add 命令需要指定文件路径")
            print("用法: python manage_docs.py add <文件路径>")
            sys.exit(1)
        cmd_add(sys.argv[2])
    elif command == "rebuild":
        cmd_rebuild()
    elif command == "status":
        cmd_status()
    else:
        print(f"未知命令: {command}")
        print_usage()
        sys.exit(1)
