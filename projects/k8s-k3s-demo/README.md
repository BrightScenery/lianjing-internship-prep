# 项目3：K8s k3s 部署实战

> **对应周次**：第3周（5.6 - 5.12）
> **技术栈**：Kubernetes + k3s + Traefik Ingress + YAML
> **学习目标**：理解 K8s 核心概念，能用 kubectl 部署应用

## 项目说明

在腾讯云服务器上部署 k3s（轻量级 K8s），将 Docker 镜像部署到 K8s 集群，理解 Pod / Deployment / Service / Ingress 的关系。

## 为什么做这个项目

联旌智能的自研容器引擎和调度系统，其设计理念与 K8s 一脉相承。虽然公司底层是自研技术，但理解 K8s 的调度模型、资源管理、服务发现等概念，能帮助我理解他们产品解决的核心问题：**如何在异构算力环境中高效调度任务**。这也是 HR 明确建议学习的内容。

## 为什么选 k3s 而不是 Minikube

- 服务器配置低（2核4GB），Minikube 太重跑不起来
- k3s 是专为资源受限场景设计的轻量级 K8s，二进制不到 100MB，内存占用约 500MB
- k3s 内置 Traefik Ingress Controller，不用额外安装

## 文件列表

| 文件 | 说明 | 对应知识点 |
|------|------|-----------|
| `deployment.yaml` | nginx Deployment（3副本） | Pod 管理 |
| `service.yaml` | nginx Service（NodePort） | 服务发现 |
| `flask-deployment.yaml` | Flask Deployment（2副本） | 多副本部署 |
| `flask-service.yaml` | Flask Service（NodePort） | 端口暴露 |
| `middleware-nginx.yaml` | Traefik StripPrefix 中间件 | 请求预处理 |
| `ingressroute.yaml` | Traefik IngressRoute（路径路由） | 7层路由 |

## 运行方式

```bash
# k3s 安装后自动运行
sudo k3s kubectl get pods
sudo k3s kubectl apply -f deployment.yaml
sudo k3s kubectl apply -f service.yaml
sudo k3s kubectl apply -f ingressroute.yaml

# 验证
curl http://localhost:31304/nginx
curl http://localhost:31304/api/health
```

## 学到的 K8s 概念

| 概念 | 理解 |
|------|------|
| Pod | 最小部署单元，一个或多个容器的组合 |
| Deployment | 管理 Pod 的副本数、滚动更新 |
| Service | 稳定的网络入口，关联到一组 Pod |
| Endpoints | Service 和 Pod 之间的"通讯录" |
| kube-proxy | 每个节点上的程序，监听 Service 变化，写入 iptables 规则 |
| Ingress | 7层路由，一个端口暴露多个服务 |
| Middleware | 请求预处理（路径重写、认证、限流） |
| IngressRoute | Traefik 的自定义 Ingress，支持每条路由单独配 Middleware |
