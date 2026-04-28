# 第3周学习总结：K8s 名词扫盲

> 日期：2026.05.06 - 2026.05.12

## 本周目标
理解 Kubernetes 核心概念，能用 Minikube 搭建本地集群，部署容器化应用。

## 学习内容

### 核心概念

| 概念 | 我的理解 |
|------|---------|
| Pod | |
| Deployment | |
| Service | |
| Namespace | |
| YAML 配置文件 | |
| 调度器（Scheduler） | |
| GPU 资源管理 | |
| Helm | |

### 完成的 YAML 配置（目标 2+）

1. [ ] Deployment 配置
2. [ ] Service 配置

## 本周产出
- 项目：[K8s Minikube 部署](../../projects/k8s-minikube-demo/)

## 量化数据
| 指标 | 目标 | 实际 |
|------|------|------|
| commit 次数 | 7 | |
| 学习时长 | 12h | |
| 编写 YAML 配置 | 2 | |
| 成功部署应用 | 1 | |

## 为什么学 K8s？

联旌智能的自研容器引擎和调度系统，其设计理念与 K8s 一脉相承。理解 K8s 的调度模型、资源管理、服务发现等概念，能帮助我理解他们产品解决的核心问题：如何在异构算力环境中高效调度任务。

## 重点场景（结合联旌实际业务）

### 场景 1：GPU 资源调度（联旌核心场景）
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

### 需要改进的地方

### 下周重点关注（RAG 实战）
- 从"部署容器"到"跑 AI 应用"
- Ollama 本地模型部署（和联旌的 DeepSeek 部署逻辑类似）
- RAG 是高校最常见的 AI 落地场景
