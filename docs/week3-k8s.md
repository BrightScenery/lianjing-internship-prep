# 第3周学习总结：K8s 名词扫盲

> 日期：2026.05.06 - 2026.05.12

## 本周目标
理解 Kubernetes 核心概念，能用 k3s 搭建轻量级集群，部署容器化应用。

## 学习内容

### 核心概念

| 概念 | 我的理解 |
|------|---------|
| Pod | K8s 最小部署单元，一个或多个容器的组合。同 Pod 内容器共享 IP、端口、存储，通过 localhost 通信。为什么不是直接管容器？因为 K8s 需要管理"一组紧密协作的容器"，Pod 就是这个协作单元 |
| Deployment | Pod 的"管家"。声明"我要几个副本"，Deployment 负责始终保持这个数量，Pod 挂了自动拉起，更新镜像时做滚动更新（逐个替换，不停机） |
| Service | 给 Pod 提供稳定网络入口的"前台接待"。Pod 死了重建 IP 会变，Service 通过 label selector 关联一组 Pod，提供稳定 IP。三种类型：ClusterIP（内网）/ NodePort（节点端口）/ LoadBalancer（云负载均衡） |
| Namespace | K8s 里的虚拟隔离空间。类似电脑上的不同用户文件夹，不同 Namespace 下的资源互不干扰。默认有 default、kube-system（系统组件）、kube-public |
| YAML 配置文件 | K8s 的"愿望清单"——声明式 API。不直接操作容器，而是写 YAML 告诉 K8s "我想要什么状态"，K8s 负责让这个状态变成现实 |
| 调度器（Scheduler） | 决定 Pod 去哪个节点的"分配员"。看节点 CPU/内存/GPU 够不够、标签匹不匹配，然后分配。联旌 EaaS 的核心就是做这件事，只不过更复杂（异构资源：GPU/NPU/DCU） |
| GPU 资源管理 | GPU 是特殊硬件，K8s 不认识，需要 NVIDIA Device Plugin 注册成 `nvidia.com/gpu` 资源。最小申请单位是 1。共享方案：MPS（时间片无隔离）/ vGPU（软件隔离）/ MIG（硬件隔离，仅 A100+） |
| Helm | K8s 的包管理器。Chart = 安装包（Go 模板 + 默认 values），Release = 安装实例，Values = 自定义配置。核心数据流：values.yaml → {{ .Values.xxx }} 模板 → 最终 YAML。`helm install/upgrade/rollback` 管理生命周期 |

### 完成的 YAML 配置（目标 2+）

1. [x] `deployment.yaml` — nginx Deployment（3副本 + 资源限制）
2. [x] `service.yaml` — nginx Service（NodePort 端口暴露）
3. [x] `flask-deployment.yaml` — Flask Deployment（2副本）
4. [x] `flask-service.yaml` — Flask Service（NodePort）
5. [x] `gpu-deployment.yaml` — GPU 资源声明（nvidia.com/gpu: 1）
6. [x] Helm Chart — 模板化 Flask 部署（deployment.yaml + service.yaml + _helpers.tpl）
7. [x] `ingressroute.yaml` — Traefik IngressRoute（7层路径路由）

## 本周产出
- 项目：[K8s k3s 部署实战](../../projects/k8s-k3s-demo/)

## 量化数据
| 指标 | 目标 | 实际 |
|------|------|------|
| commit 次数 | 7 | 7 |
| 学习时长 | 12h | 12h |
| 编写 YAML 配置 | 2 | 7 |
| 成功部署应用 | 1 | 2 |

## K8s 架构图

```
                    用户（kubectl / Helm）
                           |
                           v
                   ┌───────────────┐
                   │  API Server   │  ← K8s 的"前台"，所有操作都通过它
                   │  (kube-apiserver) │
                   └───────┬───────┘
                           |
              ┌────────────┼────────────┐
              v            v            v
      ┌───────────┐ ┌───────────┐ ┌───────────┐
      │ etcd      │ │ Scheduler │ │ Controller│
      │ (数据库)   │ │ (调度器)   │ │ (控制器)   │
      │ 存储所有   │ │ 决定Pod   │ │ 维持期望  │
      │ 配置和状态 │ │ 去哪个节点 │ │ 副本数量  │
      └───────────┘ └───────────┘ └───────────┘
                           |
                           v
              ┌────────────────────────┐
              │     Worker Node 1      │
              │  ┌──────────────────┐  │
              │  │    Pod A          │  │
              │  │  ┌─────┬───────┐ │  │
              │  │  │Flask│ Sidecar│ │  │  ← 同 Pod 内共享 IP/存储
              │  │  └─────┴───────┘ │  │
              │  └──────────────────┘  │
              │  ┌──────────────────┐  │
              │  │    Pod B          │  │
              │  │  ┌──────┐        │  │
              │  │  │Flask │        │  │
              │  │  └──────┘        │  │
              │  └──────────────────┘  │
              │  ┌──────────────────┐  │
              │  │ kubelet          │  │  ← 节点管家，向 API Server 汇报状态
              │  └──────────────────┘  │
              │  ┌──────────────────┐  │
              │  │ kube-proxy       │  │  ← 网络管家，维护 Service → Pod 映射
              │  └──────────────────┘  │
              └────────────────────────┘
                           |
              ┌────────────┼────────────┐
              v            v            v
       ┌──────────┐  ┌──────────┐  ┌──────────┐
       │ Service  │  │ Ingress  │  │  Volume  │
       │ (稳定入口)│  │ (7层路由) │  │ (持久化) │
       └──────────┘  └──────────┘  └──────────┘
```

### 一次请求的完整路径（以你的 Flask 应用为例）

```
浏览器请求
    ↓
服务器 IP:NodePort (30080)
    ↓
kube-proxy (iptables 规则，把请求转发到 Pod)
    ↓
Service (通过 label selector 找到 Flask Pod)
    ↓
Pod:Flask 容器 (5000 端口处理请求)
```

### 核心组件关系图

```
Namespace: default
├── Deployment (helm-flask)
│   ├── Pod (flask-pod-abc123)  ← 标签: app=flask
│   │   └── Container: flask-app:5000
│   └── Pod (flask-pod-def456)  ← 标签: app=flask
│       └── Container: flask-app:5000
│
├── Service (flask-service)
│   ├── selector: app=flask       ← 关联上面的两个 Pod
│   ├── ClusterIP: 10.43.x.x      ← 集群内稳定 IP
│   └── NodePort: 30080           ← 外部访问入口
│
└── IngressRoute (Traefik)
    ├── 路径: /api → flask-service:5000
    └── 路径: /nginx → nginx-service:80
```

### 声明式 API 的核心思想

```
你写 YAML → kubectl apply → API Server 记录"期望状态"
                              ↓
                    Controller 持续对比：
                    "期望状态" vs "实际状态"
                              ↓
                    不一致 → 自动修正（创建/删除/重启 Pod）
                              ↓
                    一致 → 维持现状
```

这就是 K8s 的精髓：**你告诉它"要什么"，它负责"怎么做到"**。不需要手动 ssh 到机器上起进程、配负载均衡、监控进程——这些全部自动化。

## 为什么学 K8s？

联旌智能的 EaaS 平台底层是容器化架构，其自研容器引擎和调度系统的设计理念与 K8s 一脉相承。理解 K8s 的调度模型、资源管理、服务发现等概念，能帮助我理解这类产品解决的核心问题：如何在异构算力环境中高效调度任务。

## 重点场景（结合实际业务）

### 场景 1：GPU 资源调度
高校买了 A100 显卡，要在 K8s 上跑训练。需要理解：
- `nvidia-smi` 查看 GPU 状态（显存占用、温度、利用率）
- K8s 里怎么声明 GPU 资源：`resources.limits: nvidia.com/gpu: 1`
- GPU 共享 vs MIG 切分：一张卡给多个任务用
- CUDA 版本不对导致容器起不来：怎么排查（`kubectl logs`，进容器看 `nvcc --version`）

### 场景 2：OOM Kill 排查
文章提到的真实场景：程序跑了一半崩了。在 K8s 里怎么查？
- `kubectl get pod` 看状态是不是 `OOMKilled`
- `kubectl describe pod` 看 Events 里有没有 OOM 事件
- 检查资源限制（cgroup 限制）：`resources.limits.memory`
- 解决：调大配额或者优化代码内存占用

### 场景 3：GPU 利用率忽高忽低
文章提到的杀手锏能力——通过 Linux 指标反推业务瓶颈：
- GPU 利用率 0% → 看 CPU Load（`htop`），Load 高说明 CPU 来不及喂数据（预处理太慢）
- Load 低但 iowait 高 → 磁盘 IO 瓶颈，需要搬到 NVMe SSD
- 这和"会用命令"的区别在于：**知道什么症状对应什么指标，知道去哪看**

## 反思与下周计划

### 做得好的地方

- 学习时间充足（15.5h vs 12h 目标），每天坚持
- 从手动写 YAML 到 Helm 模板化，理解了工具演进的逻辑
- 没有停留在概念层面，在腾讯云服务器上实际跑了 k3s，部署了两个应用

### 需要改进的地方

- 知识停留在"知道是什么"，还没到"知道为什么"——深度不够
- 计算机网络、端口、Flask 等基础知识薄弱，影响对 K8s 概念的深入理解
- 边学边忘，缺少定期复习和实操巩固机制
- 对云计算、GPU/CUDA、芯片等行业的底层知识了解不足，行业认知有待加强

### 知识串联：从 Week1 到 Week3

```
Linux 命令 (Week1) → Docker 容器化 (Week2) → K8s 编排 (Week3)
     ↓                      ↓                      ↓
  操作系统基础           单个应用打包            多应用调度
  文件/进程/网络         镜像/容器/Volume        Pod/Deployment/Service
```

K8s 本质上就是把 Docker 的"单机管理"放大到"集群管理"。Docker 解决了"怎么打包"，K8s 解决了"怎么跑、跑在哪、怎么找"。

### 下周重点关注（RAG 实战）

- 从"部署容器"到"跑 AI 应用"——把 RAG 应用跑起来
- Ollama 本地模型部署（和公司帮客户部署大模型的逻辑类似）
- RAG 是高校最常见的 AI 落地场景
- 把前三周的知识串起来：Linux 基础 + Docker 容器化 + K8s 编排
 