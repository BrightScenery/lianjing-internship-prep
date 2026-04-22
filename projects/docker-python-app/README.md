# 项目2：Flask Web 服务容器化

> **对应周次**：第2周（4.29 - 5.5）
> **技术栈**：Docker + Python + Flask
> **学习目标**：理解容器化原理，能独立编写 Dockerfile

## 项目说明

用 Python Flask 写一个简单的 Web 服务（返回 JSON 数据），然后编写 Dockerfile 将其容器化，最终实现 `docker run` 一键启动服务。

## 为什么做这个项目

联旌智能的 EaaS 平台核心就是**容器化交付**——把客户需要的软件（HPC 应用、AI 模型等）打包成标准化容器镜像，实现"一次构建，到处运行"。通过这个项目，我能理解 Docker 镜像分层、容器网络、数据卷等核心概念，这些是理解 EaaS 平台底层架构的基础。

## 文件列表

- `app.py` — Flask 应用代码
- `Dockerfile` — 容器构建文件
- `requirements.txt` — Python 依赖

## 运行方式

```bash
docker build -t flask-app .
docker run -p 5000:5000 flask-app
```

## 学到的 Docker 概念

| 概念 | 理解 |
|------|------|
| Image（镜像） | |
| Container（容器） | |
| Dockerfile | |
| Volume（数据卷） | |
| Port Mapping | |
