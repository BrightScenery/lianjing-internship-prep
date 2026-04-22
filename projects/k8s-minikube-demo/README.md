# 项目3：K8s Minikube 部署

> **对应周次**：第3周（5.6 - 5.12）
> **技术栈**：Kubernetes + Minikube + YAML
> **学习目标**：理解 K8s 核心概念，能用 kubectl 部署应用

## 项目说明

在本地搭建 Minikube 单节点集群，将第2周的 Docker 镜像部署到 K8s 上，理解 Pod / Deployment / Service 的关系。

## 为什么做这个项目

联旌智能的自研容器引擎和调度系统，其设计理念与 K8s 一脉相承。虽然公司底层是自研技术，但理解 K8s 的调度模型、资源管理、服务发现等概念，能帮助我理解他们产品解决的核心问题：**如何在异构算力环境中高效调度任务**。这也是 HR 明确建议学习的内容。

## 文件列表

- `deployment.yaml` — Deployment 配置
- `service.yaml` — Service 配置

## 运行方式

```bash
minikube start
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
kubectl get pods
```

## 学到的 K8s 概念

| 概念 | 理解 |
|------|------|
| Pod | |
| Deployment | |
| Service | |
| Namespace | |
| 调度器（Scheduler） | |
| GPU 资源管理 | |
