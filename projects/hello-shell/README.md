# 项目1：系统状态检查脚本

> **对应周次**：第1周（4.22 - 4.28）
> **技术栈**：Linux + Shell
> **学习目标**：掌握 Linux 基础命令，能编写实用 Shell 脚本

## 项目说明

编写一个 Shell 脚本，运行后自动输出当前系统的状态信息，包括：
- CPU 使用率
- 内存使用情况
- 磁盘空间
- 当前运行的进程数
- 网络接口信息

## 为什么做这个项目

联旌智能的 EaaS 平台需要管理多台服务器集群，运维人员需要快速了解每台节点的健康状态。这个脚本模拟了运维中最常见的"巡检"场景，帮助我理解 Linux 系统管理的基本操作。

## 文件列表

| 文件 | 说明 | 日期 |
|------|------|------|
| `hello.py` | 第一个 Python 脚本 | 4.22 |
| `check-system.sh` | 系统状态检查脚本 | 4.24-4.25 |
| `text-process.sh` | 文本处理练习（grep/sed/awk） | 4.24 |
| `file-practice.sh` | 文件操作练习 | 4.23 |
| `net-api-check.sh` | 网络健康巡检脚本 | 4.26 |
| `batch-rename.sh` | 批量重命名文件脚本 | 4.27 |
| `scores.csv` | 练习用测试数据 | 4.23 |
| `server.log` | 模拟日志文件 | 4.23 |

## 运行方式

```bash
# 系统巡检
chmod +x check-system.sh
./check-system.sh

# 网络巡检
chmod +x net-api-check.sh
./net-api-check.sh

# 批量重命名
chmod +x batch-rename.sh
# 编辑脚本中的 target_dir 后运行
bash batch-rename.sh
```

## 用到的命令

### 第1天（4.22）：环境搭建
| 命令 | 用途 |
|------|------|
| `wsl` | 安装 WSL2 + Ubuntu |
| `python3` | 运行第一个 Python 脚本 |

### 第2-3天（4.23-4.24）：文件与文本处理
| 命令 | 用途 |
|------|------|
| `ls/cd/mkdir/cp/mv/rm/touch` | 基础文件操作 |
| `grep` | 搜索文件内容 |
| `sed` | 文本替换 |
| `awk` | 列提取 |
| `cut` | 按分隔符切分 |
| `sort/uniq/wc` | 统计排序 |

### 第4天（4.25）：系统管理
| 命令 | 用途 |
|------|------|
| `ps/top` | 查看进程 |
| `free` | 查看内存 |
| `df/du` | 查看磁盘 |
| `chmod/chown` | 修改权限 |

### 第5天（4.26）：网络命令
| 命令 | 用途 |
|------|------|
| `ping` | 测试连通性 |
| `curl` | 发 HTTP 请求 |
| `wget` | 文件下载 |
| `ssh` | 远程登录 |
| `tar/gzip` | 打包压缩 |

### 第6天（4.27）：Shell 编程
| 语法 | 用途 |
|------|------|
| 变量/`$()` | 存储数据和命令结果 |
| `if/elif/else` | 条件判断 |
| `for/while` | 循环遍历 |
| 函数/`local`/`return` | 封装可复用逻辑 |
