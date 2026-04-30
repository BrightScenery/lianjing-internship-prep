# 使用官方 Python 3.12 精简版镜像作为基础
FROM python:3.12-slim

# 设置容器内的工作目录（所有后续命令都在这个目录下执行）
WORKDIR /app

# 先只复制 requirements.txt（利用 Docker 缓存，避免每次改代码都重装依赖）
COPY requirements.txt .

# 安装 Python 依赖（--no-cache-dir 可以减小镜像体积
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码到工作目录
COPY app.py .

# 声明容器内应用监听的端口（纯文档说明，不影响实际功能）
EXPOSE 5000

# 容器启动时执行的命令
CMD ["python","app.py"]
