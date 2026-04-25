# Linux 常用命令大全

> 从零到熟练：Linux 新手必备参考手册

---

## 目录

1. [Linux 基础知识](#1-linux-基础知识)
2. [文件与目录管理](#2-文件与目录管理)
3. [文件权限管理](#3-文件权限管理)
4. [文本查看与编辑](#4-文本查看与编辑)
5. [文本处理三剑客：grep、sed、awk](#5-文本处理三剑客grepsedawk)
6. [文件查找](#6-文件查找)
7. [压缩与解压](#7-压缩与解压)
8. [用户与用户组管理](#8-用户与用户组管理)
9. [进程管理](#9-进程管理)
10. [网络管理](#10-网络管理)
11. [磁盘与文件系统](#11-磁盘与文件系统)
12. [系统信息与环境](#12-系统信息与环境)
13. [软件包管理](#13-软件包管理)
14. [重定向与管道](#14-重定向与管道)
15. [Shell 快捷键](#15-shell-快捷键)
16. [Vim 编辑器常用操作](#16-vim-编辑器常用操作)
17. [常见快捷键汇总](#17-常见快捷键汇总)
18. [常见问题与解决方法](#18-常见问题与解决方法)
19. [附录：命令英文全称速查](#19-附录命令英文全称速查)

---

## 1. Linux 基础知识

### 1.1 什么是 Linux？

Linux 是一个**开源、免费**的类 Unix 操作系统内核，由芬兰学生 **Linus Torvalds**（林纳斯·托瓦兹）于 1991 年首次发布。我们日常说的 "Linux 系统"，通常指的是基于 Linux 内核的完整操作系统，如 Ubuntu、CentOS、Debian 等，这些被称为**发行版**（Distribution，简称 Distro）。

### 1.2 Linux 的目录结构

Linux 采用**树形文件系统**，从根目录 `/` 开始：

```
/                   ← 根目录（整个文件系统的起点）
├── bin             ← binary，存放常用可执行命令（ls, cp, cat 等）
├── sbin            ← system binary，系统管理员专用命令
├── etc             ← 系统配置文件存放处
├── home            ← 普通用户的家目录（类似 Windows 的 C:\Users）
│   └── username    ← 你的个人目录，用 ~ 表示
├── root            ← root（超级管理员）用户的家目录
├── tmp             ← temporary，临时文件
├── var             ← variable，经常变化的文件（日志等）
├── usr             ← Unix System Resources，用户程序和数据
├── opt             ← optional，可选安装的软件
├── boot            ← 启动相关文件
├── dev             ← device，设备文件
├── proc            ← process，进程和内核信息的虚拟文件系统
└── lib             ← library，库文件
```

> **重要概念**：Linux 中**一切皆文件**——硬件设备、进程信息、网络连接等都以文件形式呈现。

### 1.3 终端（Terminal）与 Shell

- **终端**（Terminal）：你输入命令的界面，也叫控制台（Console）
- **Shell**：命令解释器，接收你的命令并执行。最常见的是 **bash**（Bourne Again SHell）

```
你输入命令 → Shell 解析 → 内核执行 → 结果返回给终端显示
```

### 1.4 用户与权限

Linux 是多用户系统，有两种主要用户：

| 用户 | 说明 |
|------|------|
| **root** | 超级管理员，拥有最高权限，可以对系统做任何操作 |
| **普通用户** | 权限受限，只能操作自己的文件和部分系统资源 |

> **安全提示**：日常使用建议用普通用户，需要管理员权限时用 `sudo`（SuperUser DO）临时提升权限。

### 1.5 绝对路径与相对路径

```
绝对路径：从根目录 / 开始的完整路径，如 /home/user/documents/file.txt
相对路径：相对于当前目录的路径，如 ./file.txt 或 ../parent/file.txt

.    表示当前目录
..   表示上一级目录
~    表示当前用户的家目录（如 /home/username）
```

---

## 2. 文件与目录管理

### 2.1 ls — 列出目录内容

```bash
ls                          # 列出当前目录内容
ls -l                       # 以长格式显示（详细信息：权限、所有者、大小、时间）
ls -a                       # 显示所有文件，包括隐藏文件（以 . 开头的文件）
ls -la                      # 组合：长格式 + 显示隐藏文件
ls -lh                      # 长格式 + 人类可读的文件大小（K, M, G）
ls -lt                      # 按修改时间排序（最新的在前）
ls -R                       # 递归显示子目录内容
ls -l *.txt                 # 只显示 .txt 文件
```

> **英文全称**：**l**i**s**t（列表）

### 2.2 cd — 切换目录

```bash
cd /home/user/documents     # 切换到指定目录
cd ..                       # 返回上一级目录
cd ~                        # 回到家目录
cd -                        # 回到上一次所在的目录
cd                          # 直接回到家目录（等同于 cd ~）
cd ../..                    # 返回上两级目录
```

> **英文全称**：**c**hange **d**irectory（更改目录）

### 2.3 pwd — 显示当前目录路径

```bash
pwd                         # 显示当前工作目录的绝对路径
pwd -P                      # 显示物理路径（解析符号链接）
```

> **英文全称**：**p**rint **w**orking **d**irectory（打印工作目录）

### 2.4 mkdir — 创建目录

```bash
mkdir mydir                 # 创建名为 mydir 的目录
mkdir -p a/b/c              # 递归创建目录，如果父目录不存在也会一并创建
mkdir dir1 dir2 dir3        # 同时创建多个目录
mkdir -m 755 newdir         # 创建目录时指定权限
```

> **英文全称**：**m**a**k**e **dir**ectory（创建目录）

### 2.5 touch — 创建空文件或更新时间戳

```bash
touch file.txt              # 创建空文件，如果文件已存在则更新其时间戳
touch file1.txt file2.txt   # 同时创建多个文件
```

> **说明**：touch 原本是用来更新文件时间戳的，但常被用来创建空文件。

### 2.6 cp — 复制文件或目录

```bash
cp file.txt /tmp/           # 复制文件到 /tmp 目录
cp file.txt newfile.txt     # 复制并重命名
cp -r dir1/ dir2/           # 递归复制目录（必须加 -r）
cp -i file.txt /tmp/        # 覆盖前提示确认（interactive）
cp -p file.txt /tmp/        # 保留文件的属性（权限、时间戳等）
cp -a source/ dest/         # 归档复制，等同于 -dpR（保留一切）
cp file.{txt,bak}           # 复制 file.txt 为 file.bak（花括号展开）
```

> **英文全称**：**c**o**p**y（复制）

### 2.7 mv — 移动或重命名文件

```bash
mv file.txt /tmp/           # 移动文件到 /tmp
mv file.txt newname.txt     # 重命名文件
mv -i file.txt /tmp/        # 覆盖前提示
mv dir1/ dir2/              # 移动目录
mv *.txt documents/         # 将所有 .txt 文件移到 documents 目录
```

> **英文全称**：**m**o**v**e（移动）

### 2.8 rm — 删除文件或目录

```bash
rm file.txt                 # 删除文件
rm -r dir/                  # 递归删除目录及其内容
rm -f file.txt              # 强制删除，不提示确认（force）
rm -rf dir/                 # 强制递归删除（⚠️ 非常危险！使用前务必确认路径）
rm -i file.txt              # 删除前逐一确认
rm *.log                    # 删除所有 .log 文件
```

> **英文全称**：**r**e**m**ove（移除）
>
> ⚠️ **警告**：`rm -rf /` 会删除整个系统，永远不要执行这条命令！

### 2.9 ln — 创建链接

```bash
ln source.txt link.txt      # 创建硬链接（两个文件指向同一数据块）
ln -s /path/to/file link    # 创建软链接/符号链接（类似 Windows 快捷方式）
```

> **硬链接**（Hard Link）：直接指向文件数据，原文件删除后仍可用
> **软链接**（Symbolic Link）：类似快捷方式，指向路径，原文件删除后失效

### 2.10 tree — 以树形显示目录结构

```bash
tree                        # 树形显示当前目录
tree -L 2                   # 只显示两层深度
tree -a                     # 包含隐藏文件
```

---

## 3. 文件权限管理

### 3.1 理解权限表示

```
-rwxr-xr--  1  user  group  4096  Jan 1 12:00  file.txt
 │ │ │ │
 │ │ │ └── 其他用户权限（r-- = 只读）
 │ │ └──── 所属组权限（r-x = 读+执行）
 │ └────── 所有者权限（rwx = 读+写+执行）
 └──────── 文件类型（- = 普通文件, d = 目录, l = 链接）
```

| 权限 | 字母 | 数字 | 含义 |
|------|------|------|------|
| 读 | r | 4 | 读取文件内容 / 列出目录内容 |
| 写 | w | 2 | 修改文件 / 在目录中创建删除文件 |
| 执行 | x | 1 | 执行文件 / 进入目录 |

### 3.2 chmod — 修改权限

```bash
chmod 755 file.sh           # rwxr-xr-x（所有者全权限，其他人读+执行）
chmod 644 file.txt          # rw-r--r--（所有者读写，其他人只读）
chmod +x script.sh          # 给所有用户添加执行权限
chmod u+x script.sh         # 仅给所有者（user）添加执行权限
chmod g-w file.txt          # 去除组（group）的写权限
chmod o-r file.txt          # 去除其他人（others）的读权限
chmod -R 755 dir/           # 递归修改目录及其内容的权限
```

> **英文全称**：**ch**ange **mod**e（更改模式）

### 3.3 chown — 修改所有者

```bash
chown user file.txt         # 修改文件所有者为 user
chown user:group file.txt   # 同时修改所有者和所属组
chown -R user:group dir/    # 递归修改
```

> **英文全称**：**ch**ange **own**er（更改所有者）

### 3.4 chgrp — 修改所属组

```bash
chgrp group file.txt        # 修改所属组
chgrp -R group dir/         # 递归修改
```

> **英文全称**：**ch**ange **grp**oup（更改组）

---

## 4. 文本查看与编辑

### 4.1 cat — 查看文件内容

```bash
cat file.txt                # 显示文件全部内容
cat -n file.txt             # 显示行号
cat file1.txt file2.txt     # 依次显示多个文件
cat file1.txt > combined.txt  # 合并多个文件
```

> **英文全称**：con**cat**enate（连接、串联）

### 4.2 more / less — 分页查看

```bash
more file.txt               # 分页查看（只能向下翻页，空格翻下一页，q 退出）
less file.txt               # 分页查看（可上下翻页，功能更强大，推荐）
```

**less 常用操作**：
- `空格` / `PageDown`：向下翻一页
- `PageUp` / `b`：向上翻一页
- `G`：跳到文件末尾
- `gg`：跳到文件开头
- `/关键词`：搜索（n 下一个，N 上一个）
- `q`：退出

### 4.3 head / tail — 查看首/尾行

```bash
head file.txt               # 显示前 10 行
head -n 20 file.txt         # 显示前 20 行
tail file.txt               # 显示最后 10 行
tail -n 20 file.txt         # 显示最后 20 行
tail -f /var/log/syslog     # 实时跟踪文件新增内容（查看日志神器）
tail -f -n 50 log.txt       # 实时跟踪最后 50 行
```

### 4.4 nano — 简易文本编辑器

```bash
nano file.txt               # 用 nano 编辑文件
```

**nano 常用快捷键**（底部菜单会显示）：
- `Ctrl + O`：保存（Write Out）
- `Ctrl + X`：退出
- `Ctrl + W`：搜索
- `Ctrl + K`：剪切一行
- `Ctrl + U`：粘贴

### 4.5 diff — 比较文件差异

```bash
diff file1.txt file2.txt    # 比较两个文件的差异
diff -u file1.txt file2.txt # 以统一格式显示（适合生成补丁）
diff -r dir1/ dir2/         # 递归比较两个目录
```

> **英文全称**：**diff**erence（差异）

---

## 5. 文本处理三剑客：grep、sed、awk

### 5.1 grep — 文本搜索

```bash
grep "hello" file.txt       # 在文件中搜索包含 "hello" 的行
grep -i "hello" file.txt    # 忽略大小写搜索
grep -n "hello" file.txt    # 显示匹配行的行号
grep -r "hello" /path/      # 递归搜索目录下的所有文件
grep -v "hello" file.txt    # 显示不包含 "hello" 的行（反向匹配）
grep -c "hello" file.txt    # 统计匹配的行数
grep -l "hello" *.txt       # 只显示包含匹配内容的文件名
grep -E "pattern1|pattern2" # 使用扩展正则，匹配多个模式
grep "^start" file.txt      # 搜索以 "start" 开头的行（^ 表示行首）
grep "end$" file.txt        # 搜索以 "end" 结尾的行（$ 表示行尾）
```

> **英文全称**：**g**lobal **r**egular **e**xpression **p**rint（全局正则表达式打印）

### 5.2 sed — 流编辑器

```bash
sed 's/old/new/g' file.txt  # 将所有 "old" 替换为 "new"（全局替换）
sed 's/old/new/' file.txt   # 只替换每行第一个 "old"
sed -i 's/old/new/g' file.txt # 直接修改文件并保存（-i = in-place）
sed '2d' file.txt           # 删除第 2 行
sed '3,5d' file.txt         # 删除第 3 到 5 行
sed '/pattern/d' file.txt   # 删除包含 pattern 的行
sed -n '5,10p' file.txt     # 只打印第 5 到 10 行
sed 's/\bword\b/NEW/g'      # 全词匹配替换
```

> **英文全称**：**s**tream **ed**itor（流编辑器）

### 5.3 awk — 文本分析工具

```bash
awk '{print $1}' file.txt   # 打印每行第一个字段（默认以空格分隔）
awk -F: '{print $1}' /etc/passwd  # 以 : 为分隔符，打印第一个字段
awk '{sum += $1} END {print sum}' # 对第一列求和
awk 'NR==5' file.txt        # 打印第 5 行（NR = Number of Row）
awk 'NR>=3 && NR<=7' file.txt # 打印第 3 到 7 行
awk '{print NR": "$0}' file.txt # 给每行添加行号
awk '/pattern/ {print}' file.txt # 打印匹配 pattern 的行
```

> **英文全称**：取自三位作者 **A**ho、**W**einberger、**K**ernighan 的首字母

---

## 6. 文件查找

### 6.1 find — 按条件查找文件

```bash
find . -name "file.txt"     # 在当前目录查找指定名称的文件
find / -name "*.log"        # 在整个系统查找 .log 文件
find . -type f              # 查找所有普通文件（f = file）
find . -type d              # 查找所有目录（d = directory）
find . -size +100M          # 查找大于 100MB 的文件
find . -mtime -7            # 查找 7 天内修改过的文件
find . -mtime +30           # 查找 30 天前修改过的文件
find . -name "*.tmp" -delete  # 查找并删除 .tmp 文件
find . -name "*.py" -exec grep "import" {} \;  # 找到 .py 文件并执行 grep
find . -empty               # 查找空文件/空目录
```

> **常用时间选项**：
> - `-mtime`：修改时间（modify time）
> - `-atime`：访问时间（access time）
> - `-ctime`：状态改变时间（change time）

### 6.2 locate — 快速查找文件

```bash
locate file.txt             # 快速查找文件（基于数据库，速度快）
sudo updatedb               # 更新文件数据库（新文件需要先更新才能查到）
locate -i "*.txt"           # 忽略大小写
```

> **区别**：`find` 实时搜索磁盘，准确但较慢；`locate` 搜索数据库，快但可能不是最新的。

### 6.3 which / whereis — 查找命令位置

```bash
which python                # 显示可执行文件的完整路径
whereis python              # 显示命令的二进制、源码和手册页位置
```

---

## 7. 压缩与解压

### 7.1 tar — 打包与压缩

```bash
# 压缩
tar -czvf archive.tar.gz dir/    # 将目录打包并 gzip 压缩
tar -cjvf archive.tar.bz2 dir/   # 打包并 bzip2 压缩
tar -cJvf archive.tar.xz dir/    # 打包并 xz 压缩

# 解压
tar -xzvf archive.tar.gz         # 解压 .tar.gz
tar -xjvf archive.tar.bz2        # 解压 .tar.bz2
tar -xJvf archive.tar.xz         # 解压 .tar.xz
tar -tf archive.tar.gz           # 查看压缩包内容（不解压）
```

> **参数记忆**：
> - **t**ar 的参数中，**c** = create（创建）、**x** = e**x**tract（解压）、**z** = g**z**ip、**j** = bzip**2**、**J** = xz、**v** = **v**erbose（显示过程）、**f** = **f**ile（指定文件名）

### 7.2 zip / unzip — ZIP 格式

```bash
zip archive.zip file1 file2   # 压缩文件为 zip
zip -r archive.zip dir/       # 压缩目录（需要 -r 递归）
unzip archive.zip             # 解压 zip 文件
unzip -l archive.zip          # 查看内容
unzip archive.zip -d /path/   # 解压到指定目录
```

### 7.3 gzip / gunzip

```bash
gzip file.txt                 # 压缩为 file.txt.gz（会删除原文件）
gunzip file.txt.gz            # 解压
gzip -k file.txt              # 压缩但保留原文件（keep）
```

---

## 8. 用户与用户组管理

### 8.1 用户管理

```bash
whoami                      # 显示当前用户名
id                          # 显示当前用户 ID 和组信息
useradd newuser             # 创建新用户
useradd -m -s /bin/bash newuser  # 创建用户并生成家目录、指定 Shell
passwd newuser              # 设置/修改用户密码
usermod -aG sudo newuser    # 将用户添加到 sudo 组（赋予管理员权限）
userdel -r username         # 删除用户及其家目录（-r = remove）
```

### 8.2 用户组管理

```bash
groupadd groupname          # 创建新用户组
groupdel groupname          # 删除用户组
groups username             # 查看用户所属组
```

### 8.3 su 与 sudo — 切换用户与提权

```bash
su                          # 切换到 root 用户（需要 root 密码）
su - username               # 切换到指定用户并加载其环境
sudo command                # 以 root 权限执行命令
sudo -i                     # 切换到 root 用户的登录 Shell
sudo -s                     # 启动 root 的 Shell
sudo -l                     # 查看当前用户的 sudo 权限
```

> **su**：**s**witch **u**ser（切换用户）
> **sudo**：**s**uper**u**ser **do**（以超级用户身份执行）

---

## 9. 进程管理

### 9.1 ps — 查看进程

```bash
ps                          # 查看当前终端的进程
ps aux                      # 查看所有进程的详细信息
ps -ef                      # 以完整格式显示所有进程
ps aux | grep nginx         # 查找 nginx 相关进程
ps aux --sort=-%mem         # 按内存使用排序
ps aux --sort=-%cpu         # 按 CPU 使用率排序
```

> **英文全称**：**p**rocess **s**tatus（进程状态）
>
> **ps aux 输出说明**：
> - `USER`：进程所有者
> - `PID`：进程 ID（Process ID）
> - `%CPU` / `%MEM`：CPU/内存使用率
> - `VSZ` / `RSS`：虚拟内存 / 物理内存
> - `STAT`：进程状态（R=运行, S=睡眠, Z=僵尸, T=停止）
> - `COMMAND`：启动命令

### 9.2 top / htop — 动态监控进程

```bash
top                         # 实时显示进程状态（q 退出）
htop                        # 更美观的进程监控（需安装）
```

**top 常用操作**：
- `P`：按 CPU 排序
- `M`：按内存排序
- `q`：退出
- `k`：输入 PID 杀死进程

### 9.3 kill / killall — 终止进程

```bash
kill 1234                   # 向 PID 1234 发送终止信号（默认 SIGTERM，优雅退出）
kill -9 1234                # 强制杀死进程（SIGKILL，立即终止）
kill -15 1234               # 等同于 kill 1234（SIGTERM）
killall nginx               # 按进程名杀死所有 nginx 进程
pkill -f "python app"       # 按模式匹配杀死进程
```

> **信号说明**：
> - `SIGTERM`（15）：请求进程优雅退出（默认）
> - `SIGKILL`（9）：强制杀死，进程无法捕获
> - `SIGHUP`（1）：挂起信号，常用于重载配置

### 9.4 前台与后台任务

```bash
command &                   # 在后台运行命令
Ctrl + Z                    # 暂停前台任务
bg                          # 将暂停的任务放到后台继续运行
fg                          # 将后台任务调回前台
jobs                        # 查看后台任务列表
```

### 9.5 nohup — 不受终端关闭影响的运行

```bash
nohup command &             # 后台运行，关闭终端也不中断
nohup command > log.txt 2>&1 &  # 后台运行并重定向日志
```

> **英文全称**：**no** **h**ang**up**（不挂断）

---

## 10. 网络管理

### 10.1 ping — 测试网络连通性

```bash
ping google.com             # 持续 ping（Ctrl+C 停止）
ping -c 4 google.com        # ping 4 次后停止
ping -c 4 -i 0.5 baidu.com  # 每 0.5 秒 ping 一次
```

> **原理**：发送 ICMP Echo Request 包到目标主机，等待 ICMP Echo Reply 回复，以此判断网络是否通畅。

### 10.2 curl — 发送 HTTP 请求

```bash
curl https://example.com                # 获取网页内容
curl -o file.html https://example.com   # 下载到文件
curl -I https://example.com             # 只获取响应头（Header）
curl -X POST https://api.example.com    # 发送 POST 请求
curl -X POST -d "key=value" URL         # POST 并携带数据
curl -H "Authorization:Bearer xxx" URL  # 添加自定义请求头
curl -v https://example.com             # 显示详细请求过程（verbose）
```

> **英文全称**：**c**lient for **URL**s（URL 客户端）

### 10.3 wget — 下载文件

```bash
wget https://example.com/file.zip       # 下载文件
wget -O custom_name.zip URL             # 下载并重命名
wget -r https://example.com/            # 递归下载整个网站
wget -c URL                             # 断点续传（continue）
```

> **英文全称**：**W**orld **W**ide **W**eb **get**（从万维网获取）

### 10.4 ifconfig / ip — 查看网络配置

```bash
ifconfig                    # 查看网络接口信息（传统命令，部分系统已弃用）
ip addr                     # 查看 IP 地址（推荐）
ip addr show                # 显示所有网络接口
ip link                     # 显示网络接口状态
ip route                    # 显示路由表
ip route show default       # 显示默认网关
```

### 10.5 netstat / ss — 查看网络连接

```bash
netstat -tulnp              # 查看所有监听的端口及对应程序
ss -tulnp                   # 查看网络连接（推荐，更快）
netstat -an | grep :80      # 查看 80 端口的连接
```

> **netstat**：**net**work **stat**istics（网络统计）
> **ss**：**s**ocket **s**tatistics（套接字统计）

### 10.6 ssh — 远程登录

```bash
ssh user@192.168.1.100      # SSH 登录远程服务器
ssh -p 2222 user@host       # 指定端口连接
ssh -i ~/.ssh/key.pem user@host  # 使用密钥文件登录
ssh user@host "ls -la"      # 远程执行命令并返回结果
scp file.txt user@host:/path/  # 通过 SSH 传输文件到远程
scp user@host:/path/file.txt ./  # 从远程下载文件
```

> **英文全称**：**S**ecure **SH**ell（安全 Shell）
> **scp**：**s**ecure **c**o**p**y（安全复制）

### 10.7 其他网络命令

```bash
nslookup google.com         # DNS 查询
dig google.com              # 详细 DNS 查询
traceroute google.com       # 追踪数据包路由路径
hostname                    # 显示主机名
hostname -I                 # 显示所有 IP 地址
```

---

## 11. 磁盘与文件系统

### 11.1 df — 查看磁盘空间

```bash
df                          # 显示文件系统磁盘使用情况
df -h                       # 人类可读格式（推荐）
df -i                       # 查看 inode 使用情况
```

> **英文全称**：**d**isk **f**ree（磁盘空闲空间）

### 11.2 du — 查看目录大小

```bash
du -sh /home                # 查看 /home 目录的总大小
du -sh *                    # 查看当前目录每个文件/目录的大小
du -h --max-depth=1 /var    # 查看 /var 下一级子目录的大小
du -ah | sort -rh | head -20 # 找出最大的 20 个文件
```

> **英文全称**：**d**isk **u**sage（磁盘使用量）

### 11.3 mount / umount — 挂载与卸载

```bash
mount                       # 显示已挂载的文件系统
mount /dev/sdb1 /mnt        # 挂载设备到 /mnt
umount /mnt                 # 卸载 /mnt
mount -t iso9660 file.iso /mnt  # 挂载 ISO 镜像
```

### 11.4 fdisk / lsblk — 查看磁盘分区

```bash
lsblk                       # 列出块设备（磁盘和分区）
lsblk -f                    # 显示文件系统类型
sudo fdisk -l               # 列出所有磁盘分区详情
```

---

## 12. 系统信息与环境

### 12.1 uname — 系统信息

```bash
uname                       # 显示操作系统名称
uname -a                    # 显示所有系统信息
uname -r                    # 显示内核版本
uname -m                    # 显示机器架构（x86_64, aarch64 等）
```

> **英文全称**：**un**ix **name**（Unix 名称）

### 12.2 其他系统信息命令

```bash
hostnamectl                 # 查看主机名和系统版本
cat /etc/os-release         # 查看操作系统发行版信息
cat /proc/cpuinfo           # 查看 CPU 信息
cat /proc/meminfo           # 查看内存信息
free -h                     # 查看内存使用情况（人类可读）
uptime                      # 查看系统运行时间和平均负载
date                        # 显示当前日期时间
cal                         # 显示日历
who                         # 查看当前登录的用户
w                           # 查看登录用户及其正在做什么
last                        # 查看最近的登录记录
```

### 12.3 systemctl — 服务管理（Systemd 系统）

```bash
systemctl status nginx              # 查看服务状态
systemctl start nginx               # 启动服务
systemctl stop nginx                # 停止服务
systemctl restart nginx             # 重启服务
systemctl reload nginx              # 重新加载配置（不中断服务）
systemctl enable nginx              # 设置开机自启
systemctl disable nginx             # 取消开机自启
systemctl list-units --type=service # 列出所有服务
```

---

## 13. 软件包管理

### 13.1 APT（Debian/Ubuntu 系列）

```bash
sudo apt update                     # 更新软件包列表
sudo apt upgrade                    # 升级所有已安装的软件包
sudo apt install package_name       # 安装软件包
sudo apt remove package_name        # 卸载软件包（保留配置）
sudo apt purge package_name         # 卸载并删除配置文件
sudo apt search keyword             # 搜索软件包
sudo apt autoremove                 # 自动删除不再需要的依赖
dpkg -l                             # 列出已安装的包
```

> **英文全称**：**A**dvanced **P**ackaging **T**ool（高级打包工具）

### 13.2 YUM/DNF（CentOS/RHEL/Fedora 系列）

```bash
sudo yum install package_name       # 安装（CentOS 7）
sudo dnf install package_name       # 安装（Fedora / CentOS 8+，推荐）
sudo yum remove package_name        # 卸载
sudo yum search keyword             # 搜索
sudo yum update                     # 更新所有包
rpm -qa                             # 列出所有已安装的 RPM 包
```

> **英文全称**：**YUM** = **Y**ellowdog **U**pdater **M**odified
> **DNF** = **D**andified **Y**UM（YUM 的升级版）

### 13.3 snap（通用）

```bash
sudo snap install package_name      # 安装 snap 包
sudo snap remove package_name       # 卸载
snap list                           # 列出已安装的 snap 包
```

---

## 14. 重定向与管道

### 14.1 重定向

```bash
command > file.txt          # 将标准输出重定向到文件（覆盖）
command >> file.txt         # 将标准输出追加到文件
command 2> error.txt        # 将错误输出重定向到文件
command > file.txt 2>&1     # 将标准输出和错误都重定向到同一文件
command &> file.txt         # 同上（bash 简写）
command < file.txt          # 从文件读取输入
cat << EOF                  # Here Document，多行输入
line 1
line 2
EOF
```

> **文件描述符**：
> - `0` = 标准输入（stdin）
> - `1` = 标准输出（stdout）
> - `2` = 标准错误（stderr）

### 14.2 管道（|）

```bash
command1 | command2         # 将 command1 的输出作为 command2 的输入
ls -la | grep "txt"         # 列出文件并过滤含 "txt" 的行
cat log.txt | grep "ERROR" | wc -l  # 统计日志中 ERROR 的行数
ps aux | sort -k4 -rn | head -10   # 按内存排序显示前 10 个进程
cat file.txt | tr 'a-z' 'A-Z'      # 将文件内容转为大写
cat numbers.txt | sort -n | uniq     # 排序并去重
```

> **管道原理**：管道 `|` 将前一个命令的 **标准输出** 连接到后一个命令的 **标准输入**，是 Linux "组合小工具完成大任务"哲学的核心体现。

---

## 15. Shell 快捷键

以下快捷键在 Bash Shell 命令行中通用：

### 15.1 光标移动

| 快捷键 | 功能 | 记忆 |
|--------|------|------|
| `Ctrl + A` | 跳到行首 | **A** = 开头 |
| `Ctrl + E` | 跳到行尾 | **E** = **E**nd |
| `Ctrl + B` | 光标左移一个字符 | **B** = **B**ackward |
| `Ctrl + F` | 光标右移一个字符 | **F** = **F**orward |
| `Alt + B` | 跳到上一个单词开头 | **B** = **B**ackward word |
| `Alt + F` | 跳到下一个单词结尾 | **F** = **F**orward word |

### 15.2 编辑操作

| 快捷键 | 功能 | 记忆 |
|--------|------|------|
| `Ctrl + U` | 删除光标到行首的内容 | |
| `Ctrl + K` | 删除光标到行尾的内容 | **K** = kill to end |
| `Ctrl + W` | 删除光标前的一个单词 | **W** = word |
| `Ctrl + Y` | 粘贴最近删除的内容 | **Y** = **y**ank（粘贴） |
| `Ctrl + T` | 交换光标与前一个字符 | **T** = transpose |
| `Alt + T` | 交换光标与前一个单词 | |
| `Ctrl + _` | 撤销 | undo |

### 15.3 历史与搜索

| 快捷键 | 功能 | 记忆 |
|--------|------|------|
| `Ctrl + P` | 上一条命令（同 ↑） | **P** = **P**revious |
| `Ctrl + N` | 下一条命令（同 ↓） | **N** = **N**ext |
| `Ctrl + R` | 反向搜索历史命令 | **R** = reverse search |
| `Ctrl + G` | 退出历史搜索 | **G** = give up |
| `!!` | 重复上一条命令 | |
| `!$` | 上一条命令的最后一个参数 | |
| `!n` | 执行历史中第 n 条命令 | |
| `!string` | 执行最近以 string 开头的命令 | |

### 15.4 终端控制

| 快捷键 | 功能 | 记忆 |
|--------|------|------|
| `Ctrl + C` | 中断/终止当前命令 | 终止 |
| `Ctrl + D` | 退出当前 Shell（或输入结束） | **D** = done |
| `Ctrl + Z` | 暂停前台任务，放到后台 | 挂起 |
| `Ctrl + L` | 清屏（同 clear 命令） | 清屏 |
| `Ctrl + S` | 暂停终端输出（XOFF） | 注意：会"卡住"终端 |
| `Ctrl + Q` | 恢复终端输出（XON） | 配合 Ctrl+S 使用 |

> ⚠️ **注意**：如果终端突然"卡住"不显示任何内容，很可能是误按了 `Ctrl + S`，按 `Ctrl + Q` 即可恢复。

---

## 16. Vim 编辑器常用操作

Vim 是 Linux 下最强大的文本编辑器，有三种基本模式：

### 16.1 三种模式

```
正常模式（Normal）─── i/a/o ───→ 插入模式（Insert）
       ↑                              │
       │                           Esc │
       │                              ↓
       └────── : 或 / 或 v ───→ 命令/可视模式（Command/Visual）
```

- **正常模式**：启动 Vim 时默认进入，用于导航和操作
- **插入模式**：可以像普通编辑器一样输入文字
- **命令模式**：输入 `:` 进入，用于保存、退出等高级操作

### 16.2 基本操作

**启动与退出**：
```bash
vim file.txt                # 编辑文件
vimtutor                    # Vim 官方教程（强烈推荐！约 30 分钟）
```

**退出**（需在正常模式下）：
| 命令 | 功能 |
|------|------|
| `:q` | 退出（未修改时） |
| `:q!` | 强制退出（放弃修改） |
| `:w` | 保存 |
| `:wq` 或 `:x` | 保存并退出 |

### 16.3 常用快捷键（正常模式）

**移动**：
| 快捷键 | 功能 |
|--------|------|
| `h` `j` `k` `l` | 左、下、上、右 |
| `w` | 跳到下一个单词开头 |
| `b` | 跳到上一个单词开头 |
| `0`（零） | 跳到行首 |
| `$` | 跳到行尾 |
| `gg` | 跳到文件第一行 |
| `G` | 跳到文件最后一行 |
| `5G` / `:5` | 跳到第 5 行 |

**编辑**：
| 快捷键 | 功能 |
|--------|------|
| `i` | 在光标前插入 |
| `a` | 在光标后插入（append） |
| `o` | 在下一行插入新行 |
| `x` | 删除光标处字符 |
| `dd` | 删除（剪切）当前行 |
| `yy` | 复制（复制）当前行 |
| `p` | 粘贴 |
| `u` | 撤销 |
| `Ctrl + R` | 重做 |

**搜索与替换**：
| 命令 | 功能 |
|------|------|
| `/pattern` | 向下搜索 |
| `?pattern` | 向上搜索 |
| `n` / `N` | 下一个 / 上一个匹配 |
| `:%s/old/new/g` | 全局替换 |
| `:%s/old/new/gc` | 全局替换并逐一确认 |

---

## 17. 常见快捷键汇总

### 17.1 终端通用快捷键

| 快捷键 | 功能 |
|--------|------|
| `Tab` | 自动补全命令或文件名（按两次显示所有匹配项） |
| `Ctrl + C` | 终止当前运行的命令 |
| `Ctrl + D` | 退出当前终端 |
| `Ctrl + L` | 清屏 |
| `Ctrl + R` | 搜索历史命令 |
| `↑` / `↓` | 浏览历史命令 |
| `Ctrl + A` / `Ctrl + E` | 跳到行首 / 行尾 |
| `Ctrl + U` / `Ctrl + K` | 删除到行首 / 行尾 |
| `Ctrl + W` | 删除前一个单词 |

### 17.2 Tmux 快捷键（终端复用器，需安装）

Tmux 允许你在一个终端窗口中创建多个会话、窗口和面板：

| 快捷键 | 功能 |
|--------|------|
| `tmux` | 启动 tmux |
| `Ctrl + B, C` | 创建新窗口（前缀键 Ctrl+B 后按 C） |
| `Ctrl + B, N` | 切换到下一个窗口 |
| `Ctrl + B, P` | 切换到上一个窗口 |
| `Ctrl + B, "` | 水平分割面板 |
| `Ctrl + B, %` | 垂直分割面板 |
| `Ctrl + B, 方向键` | 在面板间切换 |
| `Ctrl + B, D` | 分离会话（后台运行） |
| `tmux attach` | 重新连接之前分离的会话 |

---

## 18. 常见问题与解决方法

### 18.1 权限问题

**问题**：`Permission denied`（权限被拒绝）

```bash
# 解决方法 1：使用 sudo 提权
sudo command

# 解决方法 2：修改文件权限
chmod +x script.sh          # 添加执行权限
chmod 755 file              # 修改权限

# 解决方法 3：修改文件所有者
sudo chown $USER:$USER file
```

### 18.2 命令找不到

**问题**：`command not found`

```bash
# 检查命令是否安装
which command_name

# 安装缺失的命令
sudo apt install package_name       # Ubuntu/Debian
sudo dnf install package_name       # CentOS/Fedora

# 如果命令刚安装但找不到，刷新哈希表
hash -r
```

> **常见原因**：
> 1. 命令未安装
> 2. 命令不在 PATH 环境变量中
> 3. 拼写错误（Linux 命令区分大小写！）

### 18.3 终端"卡住"不动

**问题**：终端不响应输入，也不显示内容

```bash
# 原因 1：误按了 Ctrl + S（暂停输出）
# 解决：按 Ctrl + Q 恢复

# 原因 2：命令正在等待输入
# 解决：按 Ctrl + C 终止

# 原因 3：进程在后台运行但没有返回提示符
# 解决：按 Enter 键尝试
```

### 18.4 磁盘空间不足

**问题**：`No space left on device`

```bash
# 查看磁盘使用情况
df -h

# 找出大文件
du -sh /* | sort -rh | head -10

# 清理常见垃圾
sudo apt clean                      # 清理 apt 缓存
sudo apt autoremove                 # 清理无用依赖
rm -rf ~/.cache/*                   # 清理用户缓存
journalctl --vacuum-size=100M       # 清理系统日志

# 查找并删除大文件
find / -type f -size +500M -exec ls -lh {} \; 2>/dev/null
```

### 18.5 误删文件恢复

```bash
# 如果有备份/快照
# 从回收机制恢复（部分文件系统）

# 紧急情况下，立即停止写入操作
# 使用工具尝试恢复
sudo apt install testdisk
sudo testdisk

# 预防：重要文件定期备份，或使用版本控制（git）
```

### 18.6 Vim 退出问题

**问题**：不知道怎么退出 Vim

```
# 经典步骤：
1. 按 Esc 键（确保在正常模式）
2. 输入 :q!   （不保存强制退出）
   或输入 :wq  （保存并退出）
3. 按 Enter 键
```

### 18.7 中文乱码问题

**问题**：终端或文件显示中文乱码

```bash
# 检查系统 locale 设置
locale

# 设置 UTF-8 编码
sudo dpkg-reconfigure locales      # Debian/Ubuntu
# 选择 zh_CN.UTF-8

# 在 ~/.bashrc 中添加
export LANG=zh_CN.UTF-8
export LC_ALL=zh_CN.UTF-8
```

### 18.8 SSH 连接问题

**问题**：SSH 连接被拒绝或超时

```bash
# 检查 SSH 服务是否运行
sudo systemctl status sshd

# 启动 SSH 服务
sudo systemctl start sshd

# 检查端口是否正确
ssh -p 22 user@host

# 检查防火墙
sudo ufw status                    # Ubuntu
sudo firewall-cmd --list-all       # CentOS

# 使用 -v 调试连接
ssh -v user@host
```

### 18.9 环境变量问题

**问题**：安装的软件找不到命令

```bash
# 查看当前 PATH
echo $PATH

# 临时添加到 PATH
export PATH=$PATH:/new/path

# 永久添加：在 ~/.bashrc 末尾加入
echo 'export PATH=$PATH:/new/path' >> ~/.bashrc
source ~/.bashrc                   # 使配置立即生效
```

### 18.10 僵尸进程

**问题**：`ps` 看到大量 Z（僵尸）状态的进程

```bash
# 查看僵尸进程
ps aux | grep 'Z'

# 僵尸进程是已终止但父进程未回收的进程
# 解决方法：杀死父进程
kill -9 <父进程PID>

# 或向父进程发送 SIGCHLD
kill -SIGCHLD <父进程PID>
```

---

## 19. 附录：命令英文全称速查

| 命令 | 英文全称 | 中文含义 |
|------|----------|----------|
| `ls` | **l**i**s**t | 列表 |
| `cd` | **c**hange **d**irectory | 更改目录 |
| `pwd` | **p**rint **w**orking **d**irectory | 打印工作目录 |
| `cp` | **c**o**p**y | 复制 |
| `mv` | **m**o**v**e | 移动 |
| `rm` | **r**e**m**ove | 移除 |
| `mkdir` | **m**a**k**e **dir**ectory | 创建目录 |
| `rmdir` | **r**e**m**ove **dir**ectory | 移除目录 |
| `chmod` | **ch**ange **mod**e | 更改模式 |
| `chown` | **ch**ange **own**er | 更改所有者 |
| `chgrp` | **ch**ange **grp**oup | 更改组 |
| `cat` | con**cat**enate | 连接、串联 |
| `ln` | **l**i**n**k | 链接 |
| `grep` | **g**lobal **r**egular **e**xpression **p**rint | 全局正则打印 |
| `sed` | **s**tream **ed**itor | 流编辑器 |
| `awk` | Aho, Weinberger, Kernighan | 三位作者姓氏首字母 |
| `diff` | **diff**erence | 差异 |
| `find` | find | 查找 |
| `tar` | **t**ape **ar**chive | 磁带归档 |
| `gzip` | GNU **zip** | GNU 压缩 |
| `ps` | **p**rocess **s**tatus | 进程状态 |
| `kill` | kill | 杀死（进程） |
| `top` | table **o**f **p**rocesses | 进程表 |
| `df` | **d**isk **f**ree | 磁盘空闲 |
| `du` | **d**isk **u**sage | 磁盘使用 |
| `free` | free | 空闲（内存） |
| `uname` | **un**ix **name** | Unix 名称 |
| `hostname` | host name | 主机名 |
| `ping` | Packet InterNet Groper | 网络连通测试 |
| `curl` | **c**lient for **URL**s | URL 客户端 |
| `wget` | **W**orld **W**ide **W**eb **get** | 万维网获取 |
| `ssh` | **S**ecure **SH**ell | 安全 Shell |
| `scp` | **s**ecure **c**o**p**y | 安全复制 |
| `netstat` | **net**work **stat**istics | 网络统计 |
| `ss` | **s**ocket **s**tatistics | 套接字统计 |
| `ifconfig` | **if** **config**ure | 接口配置 |
| `mount` | mount | 挂载 |
| `su` | **s**witch **u**ser | 切换用户 |
| `sudo` | **s**uper**u**ser **do** | 超级用户执行 |
| `apt` | **A**dvanced **P**ackaging **T**ool | 高级打包工具 |
| `yum` | **Y**ellowdog **U**pdater **M**odified | 黄狗更新器（修改版） |
| `rpm` | **R**edhat **P**ackage **M**anager | RedHat 包管理器 |
| `nohup` | **no** **h**ang**up** | 不挂断 |
| `man` | **man**ual | 手册 |
| `echo` | echo | 回显 |
| `env` | **env**ironment | 环境 |
| `touch` | touch | 触摸（更新文件时间戳） |
| `file` | file | 文件（类型） |
| `which` | which | 哪个（命令位置） |
| `sort` | sort | 排序 |
| `uniq` | **uniq**ue | 唯一、去重 |
| `wc` | **w**ord **c**ount | 字数统计 |
| `head` | head | 头部 |
| `tail` | tail | 尾部 |
| `less` | less | 更少（分页查看，反向 more） |
| `more` | more | 更多（分页查看） |
| `alias` | alias | 别名 |
| `history` | history | 历史 |
| `which` | which | 哪一个 |
| `whereis` | where is | 在哪里 |
| `locate` | locate | 定位 |
| `who` | who | 谁 |
| `whoami` | who am I | 我是谁 |
| `date` | date | 日期 |
| `cal` | **cal**endar | 日历 |
| `clear` | clear | 清除 |
| `reboot` | reboot | 重启 |
| `shutdown` | shutdown | 关机 |
| `exit` | exit | 退出 |
| `export` | export | 导出（环境变量） |
| `source` | source | 来源（执行脚本在当前 Shell） |
| `alias` | alias | 别名 |
| `cron` | **cron**os（希腊时间之神） | 定时任务 |
| `daemon` | **daemon**（希腊守护神） | 守护进程 |

---

## 20. 学习建议与进阶路径

### 20.1 新手入门步骤

1. **安装 Linux**：建议先用虚拟机（VirtualBox / VMware）安装 Ubuntu，或使用 WSL（Windows Subsystem for Linux）
2. **打开终端**：熟悉基本命令 `ls`、`cd`、`pwd`、`mkdir`、`touch`
3. **练习文件操作**：`cp`、`mv`、`rm`、`cat`
4. **学习权限**：理解 `chmod`、`chown`、`sudo`
5. **掌握文本处理**：`grep`、`管道 |`、`重定向 >`
6. **学会看帮助**：`man command`、`command --help`
7. **学习 Shell 脚本**：从简单的脚本开始，逐步掌握编程

### 20.2 获取帮助的方法

```bash
man command                 # 查看命令的手册页（manual）
command --help              # 查看命令的帮助信息
command -h                  # 简短帮助信息（同 --help）
info command                # 更详细的信息（比 man 更丰富）
tldr command                # 简洁的命令示例（需安装：sudo apt install tldr）
```

### 20.3 推荐学习资源

- **Vim 入门**：终端中输入 `vimtutor`，官方交互式教程
- **Linux 命令行经典书籍**：《鸟哥的 Linux 私房菜》（中文经典）
- **在线练习**：
  - [Linux Journey](https://linuxjourney.com/) — 交互式 Linux 学习
  - [OverTheWire Bandit](https://overthewire.org/wargames/bandit/) — 通过游戏学习 Linux
- **Shell 脚本学习**：《Advanced Bash-Scripting Guide》

---

> 📝 **提示**：学习 Linux 最好的方式就是**多用**。不要害怕出错（只要不执行 `rm -rf /` 这类危险命令），多练习、多查手册，慢慢就会熟练起来。
>
> 祝学习愉快！
