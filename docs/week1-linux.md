# 第1周学习总结：Linux 生存训练

> 日期：2026.04.22 - 2026.04.28

## 本周目标
掌握 Linux 基础操作，能熟练使用终端完成日常任务，编写实用的 Shell 脚本。

## 学习内容

### 安装的软件
- [x] WSL2 + Ubuntu

### 掌握的命令（目标 30+，实际 35+）

| 类别 | 命令 | 熟练程度 |
|------|------|---------|
| 文件操作 | ls, cd, mkdir, rm, cp, mv, cat, touch, find, ln | ✅ |
| 文本处理 | grep, sed, awk, cut, sort, head, tail, wc, uniq | ✅ |
| 系统命令 | ps, top, kill, free, df, du, chmod, chown, who, uptime | ✅ |
| 网络命令 | ping, curl, wget, ssh, scp | ✅ |
| 压缩归档 | tar, gzip | ✅ |
| 其他 | echo, seq, which, history, nohup, tmux | ⬜ 待加强 |

### 完成的脚本（目标 5+，实际 6 个）

1. `hello.py` — 第一个 Python 脚本，验证 WSL2 环境
2. `file-practice.sh` — 自动创建多级目录结构（mkdir -p 实战）
3. `text-process.sh` — 8 关文本处理练习（grep/管道/cut/sort/sed/awk 综合）
4. `check-system.sh` — 系统巡检脚本（CPU/内存/磁盘/进程/资源 TOP 5）
5. `net-api-check.sh` — 网络健康检查脚本（ping/curl/wget 5 项检查）
6. `batch-rename.sh` — 批量重命名文件（变量/函数/循环/条件判断综合）

## 本周产出
- 项目：[系统状态检查脚本](../../projects/hello-shell/)
- 笔记：[linux-commands-guide.md](../linux-commands-guide.md)（42KB，完整命令参考）

## 量化数据
| 指标 | 目标 | 实际 |
|------|------|------|
| commit 次数 | 7 | 7（含今日周总结） |
| 学习时长 | 12h | ~30h |
| 掌握命令数 | 30 | 35+ |
| 完成脚本数 | 5 | 6 |

## 踩过的坑（重要教训）

1. **WSL 路径**：`/mnt/c/` 才是 Windows C 盘，不能直接 `cd Desktop`
2. **`>` vs `>>`**：覆盖写入和追加写入的区别，手写试过才记住
3. **`free -h` 不能直接 awk 计算**：带单位的字符串做除法会出错，必须用 `free -m`
4. **`du` 扫描 `/mnt/c` 极慢**：跨挂载点扫描，要用 `--exclude` 排除
5. **vim 中文冒号**：中文输入法下的 `:` vim 不识别
6. **ping 127.0.0.1 ≠ 外网通**：回环地址只测本机网络栈
7. **变量名拼写错误**：`$burl` 写成 `$url`，shell 中未定义变量值为空，静默失败
8. **tar 不是压缩**：是归档，需要配合 gzip（`tar czf`）才真正压缩

## 反思与下周计划

### 做得好的地方
- 每天坚持写日志 + commit，连续 7 天不间断
- 脚本不是零散命令堆砌，每个都有明确场景（巡检/网络检查/文本处理）
- 踩坑后能独立排查并记录原因，而不是直接问人

### 需要改进的地方
- **缺问题排查能力**：尚未学习 nvidia-smi/dmesg/glances 
- **缺生产环境工具**：环境变量/PATH 理解不够
- **管道组合能力弱**：text-process.sh 是练习性质的，没有处理过真实大文件

### 下周重点关注（Docker）
- 不只会 `docker run`，还要理解**容器和宿主的区别**（文件系统、网络、进程隔离）
- 数据卷挂载 `-v` 的实际场景（大模型数据集挂载）
- 用 `docker logs` 排查容器问题
- 环境变量和 PATH 问题