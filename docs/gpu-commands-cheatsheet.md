# GPU 工作必备命令速查

> 按实际工作场景分类 —— 遇到什么问题 → 用什么命令 → 看什么输出

## 场景1：看 GPU 状态（最常用）

```bash
# 看所有 GPU 的概况（温度、显存、利用率）
nvidia-smi

# 实时监控，每 1 秒刷新（类似 top）
nvidia-smi -l 1

# 只看关键字段，简洁输出
nvidia-smi --query-gpu=name,memory.used,memory.total,utilization.gpu --format=csv
```

**看什么：**
- Memory-Usage：显存占用 → 满了会 OOM
- GPU-Util：利用率 → 90%+ 跑满了，0% 闲置
- Temp：温度 → > 80°C 要关注散热

## 场景2：排查 GPU 任务崩了

```bash
# 查看 Pod 状态
kubectl get pod <pod-name>

# 看 Pod 详细事件
kubectl describe pod <pod-name>

# 看 Pod 日志
kubectl logs <pod-name> --tail=50

# 进入容器内检查 GPU
kubectl exec -it <pod-name> -- nvidia-smi

# 进容器看 CUDA 版本
kubectl exec -it <pod-name> -- nvcc --version

# 确认 OOM 类型
dmesg | grep -i oom
# 有 nvidia 字样 = 显存 OOM
# 没有 = 容器内存 OOM
```

## 场景3：MIG 切分操作

```bash
# 启用/关闭 MIG 模式
nvidia-smi -i 0 -mig 1    # 启用
nvidia-smi -i 0 -mig 0    # 关闭

# 列出可用的 MIG 配置
nvidia-smi mig -lgip

# 创建 MIG 实例
nvidia-smi mig -cgi 1g.10gb -C 2

# 列出当前 MIG 实例
nvidia-smi mig -lgi

# 删除所有 MIG 实例
nvidia-smi mig -dci
```

## 场景4：K8s GPU 资源管理

```bash
# 看节点上有多少 GPU
kubectl describe node | grep -A5 "nvidia.com/gpu"

# 确认 Device Plugin 在跑
kubectl get pods -n kube-system | grep nvidia-device-plugin

# 查看 Pod 的 GPU 资源声明
kubectl describe pod <pod-name> | grep -A5 "Limits"
```

## 核心记住

**工作中最常用的就两个命令：**
1. `nvidia-smi` —— 看 GPU 状态
2. `kubectl describe pod` —— 看 Pod 为什么崩

其他命令都是在这两个基础上补充信息。
