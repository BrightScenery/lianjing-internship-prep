# K8s 知识卡片

## 卡片 1：K8s 解决什么问题
- **一句话回答**：让一堆容器在多台机器上可靠地跑起来——挂了自动拉起、流量大了自动扩容、机器坏了自动迁移
- **和 Docker 的分工**：Docker 解决"怎么把一个应用打包跑起来"（单机），K8s 解决"怎么让一堆应用跑在多台机器上"（集群）
- **联旌场景**：EaaS 平台要管理 3-8 台服务器，上面跑几十种服务（Jupyter/推理/数据库/监控），必须自动化调度

## 卡片 2：Pod 为什么是最小单位
- **和 Container 的关系**：Pod 是 Container 的包装壳，一个 Pod 内可以放多个 Container
- **Sidecar 模式举例**：Flask 应用写日志到 /logs，Fluentd 容器从 /logs 收集日志发到远端——两个容器必须同宿主机、同生共死
- **共享什么**：网络命名空间（同 IP，localhost 通信）+ 存储卷（同一个 Volume，读写同一份数据）

## 卡片 3：Deployment → ReplicaSet → Pod
- **每层管什么**：Deployment 管"版本"（v1→v2、更新策略），ReplicaSet 管"数量"（保证 N 个副本），Pod 管"运行"（实际跑容器）
- **滚动更新原理**：更新时新建 ReplicaSet-v2，同时逐步缩小 ReplicaSet-v1，全程始终维持期望副本数，零停机
- **回滚为什么快**：旧 ReplicaSet 还在（只是 desired=0），`rollout undo` 就是把 desired 调回去，不需要重新创建

## 卡片 4：Service 和流量转发
- **Service 本质**：不是进程，是 K8s 里的一个声明对象——声明了 selector 和端口规则
- **kube-proxy 角色**：监听 Service 和 Endpoints 变化，把规则写成 iptables，真正转发数据包的是内核层的 iptables
- **Endpoints 的作用**：Service 和 Pod 之间的"通讯录"。selector 匹配到哪些 Pod，Endpoints 就列哪些 Pod 的 IP。选不中 = Endpoints 为空 = Service 是空壳

## 卡片 5：三种 Probe
- **各回答什么问题**：startupProbe → "启动完成了吗？"；livenessProbe → "还活着吗？"；readinessProbe → "能接客了吗？"
- **不通过的后果**：startupProbe 超限 → 杀 Pod；livenessProbe 不通过 → 杀 Pod 重启；readinessProbe 不通过 → 从 Endpoints 摘掉（不杀，不接客但活着）
- **startupProbe × failureThreshold = 最大启动时间**。例：periodSeconds=10, failureThreshold=30 → 最多给 5 分钟
- **关键规则**：startupProbe 存在时，其他两个探针被冻结，直到它第一次成功后才激活

## 卡片 6：resources requests vs limits
- **requests**：Scheduler 调度依据——选节点时看节点剩余资源是否 ≥ requests，不够就不调度到这个节点
- **limits**：运行时上限——容器跑起来后由 cgroup 强制限制
- **超 memory 后果**：OOMKilled，Pod 被强制杀掉（内存不可"限速"，用完就没了）
- **超 cpu 后果**：不会被杀，只是被限速（throttle）——等下一段时间片再给你（CPU 是时间片资源）

## 卡片 7：GPU 在 K8s 中怎么管理
- **为什么需要 Device Plugin**：GPU 是特殊硬件，K8s 不认识，需要 NVIDIA Device Plugin 把 GPU 注册为 `nvidia.com/gpu` 资源
- **GPU 资源声明**：`resources.limits.nvidia.com/gpu: 1`，最小申请单位是 1（不能要 0.5 张卡）
- **三种共享方案**：MPS（时间片共享，无隔离）/ vGPU（软件隔离，要许可证）/ MIG（硬件隔离，仅 A100+，联旌 EaaS 的核心能力）
- **排查三板斧**：`nvidia-smi` 看状态 → `kubectl describe pod` 看 Events → `kubectl exec -- nvidia-smi` 进容器确认

## 卡片 8：声明式 API
- **声明式 vs 命令式**：命令式（kubectl create deployment ...）= 敲完就没了；声明式（kubectl apply -f yaml）= 配置文件可版本控制、可复用
- **reconcile 循环**：Controller 持续比较"期望状态"（YAML 里写的）vs"实际状态"（集群当前的），不一致就自动修正（创建/删除/重启）
- **apply 的幂等性**：资源不存在 → created；已存在且不同 → configured；已存在且一致 → unchanged。同一个 YAML 执行多少次结果都一样
- **核心思想**：你告诉它"要什么"，它负责"怎么做到"
