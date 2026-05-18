FROM python:3.12-slim

WORKDIR /app

# 先安装依赖（利用 Docker 缓存分层）
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制代码和数据
COPY gradio_app.py .
COPY data/ ./data/

# .env 不打包进镜像，启动时通过 docker-compose 的 env_file 注入

EXPOSE 7860

ENV GRADIO_SERVER_NAME=0.0.0.0

CMD ["python", "gradio_app.py"]
