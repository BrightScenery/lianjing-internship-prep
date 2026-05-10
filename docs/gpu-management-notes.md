# GPU 管理笔记 — K8s 中的 GPU 资源管理

> 日期：2026-05-10 | 第3周·Day 5

## 一、GPU 是什么，为什么 K8s 要专门管？

### CPU vs GPU 的区别
| 维度 | CPU | GPU |
|------|-----|-----|
| 擅长 | 通用计算，逻辑控制 | 大规模并行计算（矩阵乘法） |
| 并发 | 几个到几十个线程 | 几万个线程同时跑 |
| K8s 支持 | 原生支持 | 需要插件（NVIDIA Device Plugin） |
| 最小单位 | 1m（千分之一核） | 1（不能要 0.5 张卡） |

### 为什么 GPU 需要专门调度？
1. **数量少**：一台机器可能有 64 核 CPU，但通常只有 1-8 张 GPU
2. **不能分割**：原生 GPU 是独占的，要 1 就是 1 整张卡
3. **驱动依赖**：容器需要 NVIDIA Container Runtime 才能访问 GPU
4. **显存隔离**：显存和系统内存是分开的，K8s 默认的内存限制不管显存

### K8s 管理 GPU 的完整链路
```
物理 GPU → NVIDIA Device Plugin 注册资源 → K8s 知道有 GPU
         → 调度器匹配 Pod 需求 → 选到有 GPU 的 Node
         → NVIDIA Container Runtime 映射 GPU 进容器
         → 容器内 nvidia-smi 能看到 GPU
```

## 二、K8s 原生 GPU 声明方式

### 基本语法
```yaml
resources:
  requests:
    nvidia.com/gpu: 1    # 调度器参考：优先选有 GPU 的 Node
  limits:
    nvidia.com/gpu: 1    # 硬限制：容器最多用 1 张 GPU
```

### 三个关键点
1. **最小单位是 1**：不能写 0.5，GPU 是整数资源
2. **requests 和 limits 必须相同**：GPU 不支持超卖（overcommit）
3. **只声明了"要卡"，不代表"能用卡"**：还需要 NVIDIA Container Runtime 在容器运行时把 GPU 设备映射进去

### 环境变量（可选但推荐）
```yaml
env:
- name: NVIDIA_VISIBLE_DEVICES
  value: "all"           # 默认值，让容器看到所有分配给它的 GPU
- name: NVIDIA_DRIVER_CAPABILITIES
  value: "compute,utility"  # compute=CUDA 计算, utility=nvidia-smi 等工具
```

## 三、GPU 共享的三种方案

### 方案对比
| 方案 | 隔离级别 | 适用硬件 | 性能损耗 | K8s 资源名 |
|------|---------|---------|---------|-----------|
| 时间片共享（MPS） | 无隔离 | 所有 NVIDIA GPU | 低 | nvidia.com/gpu |
| vGPU 虚拟化 | 软件隔离 | 需要许可证 | 10-15% | 自定义 |
| MIG 切分 | 硬件隔离 | A100/H100 以上 | 无 | nvidia.com/mig-* |

### 1. 时间片共享（MPS）
- **原理**：多个进程共用同一张 GPU，GPU 按时间片轮流服务
- **K8s 视角**：每个 Pod 仍然要 nvidia.com/gpu: 1，但通过外部配置允许多个 Pod 映射到同一张物理卡
- **致命问题**：没有显存隔离！进程 A 吃满 80GB 显存，进程 B 直接 OOM
- **适合场景**：多个小任务轮流跑，不会同时吃满显存

### 2. vGPU 虚拟化
- **原理**：hypervisor 层把物理 GPU 虚拟化成多个虚拟 GPU
- **K8s 视角**：每个 vGPU 对 K8s 来说就是一张"卡"
- **缺点**：需要 NVIDIA vGPU 许可证（要钱），性能有 10-15% 损耗
- **适合场景**：虚拟化环境，需要给每个虚拟机分 GPU

### 3. MIG 切分（Multi-Instance GPU）⭐ 联旌核心
- **原理**：硬件级别把 GPU 切成多个独立实例，每个有专用 SM（流处理器）和显存
- **K8s 视角**：每个 MIG 实例是一个独立的扩展资源
  ```yaml
  nvidia.com/mig-1g.10gb: 1   # 1 个 MIG 实例，10GB 显存
  nvidia.com/mig-2g.20gb: 1   # 2 个 SM 组，20GB 显存
  nvidia.com/mig-3g.40gb: 1   # 3 个 SM 组，40GB 显存
  ```
- **优点**：完全硬件隔离、性能无损、灵活切分
- **限制**：只有 A100/H100/H200 等高端数据中心 GPU 支持
- **A100 80GB 最多可切 7 个实例**，H100 也是 7 个

### MIG 切分配置示例
```bash
# 在宿主机上启用 MIG 模式
nvidia-smi -i 0 -mig 1

# 创建 MIG 实例（切 2 个 1g.10gb 实例）
nvidia-smi mig -cgi 1g.10gb -C 2

# 查看 MIG 实例
nvidia-smi mig -lgi

# 在 K8s 中使用
# Pod YAML 中声明 nvidia.com/mig-1g.10gb: 1
```

## 四、故障排查：GPU 任务跑崩了怎么查？

### 排查流程（从症状到根因）

#### 症状1：Pod 状态是 `OOMKilled`
```bash
# 1. 确认是显存 OOM 还是内存 OOM
kubectl get pod <pod-name> -o jsonpath='{.status.containerStatuses[*].lastState.terminated.reason}'
# → OOMKilled

# 2. 看系统日志确认
dmesg | grep -i oom
# 如果有 "nvidia" 字样 = 显存 OOM
# 如果没有 = 容器内存 OOM（resources.limits.memory）

# 3. 解决
# 显存 OOM → 减小 batch_size，或者换更大的 GPU / MIG 实例
# 内存 OOM → 调大 resources.limits.memory
```

#### 症状2：容器内 `nvidia-smi` 报错
```bash
# 常见错误1：NVIDIA-SMI has failed because it couldn't communicate with the NVIDIA driver
# 原因：NVIDIA Container Runtime 没装好，或者驱动版本不匹配
# 解决：确认 nvidia-container-toolkit 已安装，驱动版本 >= CUDA 要求版本

# 常见错误2：No devices were found
# 原因：Pod 没有声明 GPU 资源，或者 Device Plugin 没注册成功
# 解决：检查 YAML 中是否有 nvidia.com/gpu: 1

# 排查命令
kubectl exec -it <pod-name> -- nvidia-smi
kubectl describe pod <pod-name> | grep -A5 "Limits"
```

#### 症状3：GPU 利用率忽高忽低
```bash
# 这是联旌文章提到的杀手锏场景——反推业务瓶颈

# 1. GPU 利用率接近 0% → 看 CPU Load
nvidia-smi          # 看 GPU 利用率
htop                # 看 CPU Load

# CPU Load 高 = CPU 来不及喂数据给 GPU（数据预处理太慢）
# 解决：优化数据加载 pipeline，或者用 DataLoader 多进程

# 2. CPU Load 低，但 iowait 高 → 磁盘 IO 瓶颈
iostat -x 1        # 看磁盘 IO 等待
# iowait > 20% = 磁盘读写太慢
# 解决：把数据搬到 NVMe SSD，或者用内存缓存

# 3. GPU 利用率稳定在 90%+ → 正常，GPU 跑满了
```

### nvidia-smi 输出解读
```
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 535.129.03   Driver Version: 535.129.03   CUDA Version: 12.2     |
|-------------------------------+----------------------+----------------------+
| GPU  Name        Persistence-M| Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|===============================+======================+======================|
|   0  NVIDIA A100-PCIE-40GB  On| 00000000:00:04.0 Off |                    0 |
| N/A   35C    P0    35W / 250W |   5248MiB / 40960MiB |     85%      Default |
+-------------------------------+----------------------+----------------------+
```

| 字段 | 含义 | 重点关注 |
|------|------|---------|
| Temp | GPU 温度 | > 80C 需要关注散热 |
| Pwr:Usage/Cap | 当前功耗/最大功耗 | 接近 Cap 说明跑满了 |
| Memory-Usage | 显存占用/总显存 | 接近满 = 显存不够了 |
| GPU-Util | GPU 计算利用率 | 90%+ = 跑满了，0% = 闲置 |

## 五、联旌 GPU 调度业务场景模拟

### 场景：某高校买了 4 张 A100，要给学生做深度学习实验

#### 需求分析
- 40 个研究生，每人每周要做 2-3 次小实验（batch_size=32，模型=BERT-base）
- 3 个博士生，每人每天跑一次大训练（batch_size=128，模型=LLaMA-7B 微调）
- 博士生需要独占 GPU，研究生可以共用

#### 方案
```
A100 #1 → 博士生 A 独占（3g.40gb MIG 实例，独占 40GB）
A100 #2 → 博士生 B 独占（3g.40gb MIG 实例，独占 40GB）
A100 #3 → 博士生 C 独占（3g.40gb MIG 实例，独占 40GB）
A100 #4 → 切 7 个 MIG 实例（1g.5gb 每个），分给研究生轮流用
```

#### K8s YAML 对应
```yaml
# 博士生 Pod（独占）
resources:
  limits:
    nvidia.com/mig-3g.40gb: 1

# 研究生 Pod（共享）
resources:
  limits:
    nvidia.com/mig-1g.5gb: 1
```

#### 联旌 EaaS 平台在这个场景中的价值
用户不需要知道 MIG、Device Plugin、CUDA 驱动这些底层细节。
通过 EaaS 平台的 Web 界面，选择"GPU 规格"→ 平台自动完成 MIG 切分、Pod 调度、GPU 映射。

这就是为什么学 K8s + GPU 管理——**理解联旌的产品在底层做了什么**。

## 六、核心字段速查

| 字段 | 说明 | 示例值 |
|------|------|--------|
| `nvidia.com/gpu` | 标准 GPU 资源（独占整卡） | `1` |
| `nvidia.com/mig-1g.10gb` | MIG 1 分区，10GB | `1` |
| `nvidia.com/mig-2g.20gb` | MIG 2 分区，20GB | `1` |
| `nvidia.com/mig-3g.40gb` | MIG 3 分区，40GB | `1` |
| `NVIDIA_VISIBLE_DEVICES` | 容器内可见的 GPU | `all` / `0,1` / `none` |
| `NVIDIA_DRIVER_CAPABILITIES` | 容器内 GPU 功能 | `compute,utility` |
| `runtimeClassName: nvidia` | 使用 NVIDIA Container Runtime | (ContainerClass) |
