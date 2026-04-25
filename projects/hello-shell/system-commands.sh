#!/bin/bash
# ============================================
# 系统命令练习 - 2026-04-25
# 学习主题：ps / top / kill / free / df / du / chmod / chown
# 说明：跟着每一步的提示，在终端里手动敲命令，观察输出，然后填空
# ============================================

echo "========================================"
echo "  系统命令练习 - 第1周 Day 4"
echo "========================================"

# ============================================
echo ""
echo "=== 1. free：查看内存使用 ==="
echo "任务：手动运行 free -h，观察输出"
echo "问题1：你的系统总内存是多少？7.6Gi"
echo "问题2：可用内存大约占多少比例？93.4%"
echo "问题3：free 输出中 'buff/cache' 是什么？为什么占用了一部分内存？buff/cache 是缓冲区和页缓存，用于加速磁盘I/O，占用内存但可被应用程序回收。"
echo "问题4：free -h 和 free -m 的区别是什么？-h 以人类可读单位（自动K/M/G）显示，-m 强制以 MiB 为单位显示。"

# ============================================
echo ""
echo "=== 2. df：查看磁盘空间 ==="
echo "任务：运行 df -h 和 df -hT，观察输出"
echo "问题5：根分区 / 总共多少？已用多少？总共 1007G，已用 1.8G"
echo "问题6：你有几个挂载点？14个"
echo "问题7：df 和 du 的区别是什么？（查资料后写）df 查看文件系统整体磁盘使用情况（分区级别），du 查看指定目录或文件占用的磁盘空间。"

# ============================================
echo ""
echo "=== 3. du：查看目录/文件大小 ==="
echo "任务：运行以下命令，观察区别"
echo "  du -sh ."
echo "  du -sh *"
echo "  du --max-depth=1 -h /home 2>/dev/null"
echo "问题8：du -s 和不用 -s 的区别是什么？-s 只显示总计大小，不列出每个子目录的大小；不用 -s 会递归显示所有子目录的大小。"
echo "问题9：当前目录（脚本所在目录）总共多大？120K"

# ============================================
echo ""
echo "=== 4. ps：查看进程快照 ==="
echo "任务：运行 ps aux 和 ps -ef，观察输出区别"
echo "问题10：ps aux 的 'STAT' 列是什么意思？进程状态代码（如 R=运行，S=睡眠，Z=僵尸等）"
echo "问题11：ps aux 和 ps -ef 的区别是什么？aux 是 BSD 格式，显示更多列（%CPU,%MEM,STAT,START等）；-ef 是 System V 格式，显示 UID,PID,PPID,C,STIME 等。"
echo "问题12：你的系统当前有多少个进程？（ps aux | wc -l - 1）   28个"
echo ""
echo "问题13：找出 CPU 占用最高的 3 个进程"
echo "提示：ps aux --sort=-%cpu | head -4"
echo "PID 2387 进程名 wsl-pro-service CPU% 0.0"
echo "PID 1 进程名 init CPU% 0.0"
echo "PID 310 进程名 init CPU% 0.0"

# ============================================
echo ""
echo "=== 5. top：实时进程监控 ==="
echo "任务：手动运行 top，观察动态刷新"
echo "在 top 中尝试按 P（CPU排序）、M（内存排序）、q（退出）"
echo "问题14：top 和 ps 的根本区别是什么？top 是动态实时刷新显示，ps 是静态快照。"
echo "问题15：top 头部显示的 'load average' 三个数字分别代表什么？分别代表过去1分钟、5分钟、15分钟的系统平均负载。"
echo "问题16：%Cpu(s) 行中 'id' 是什么意思？CPU 空闲百分比（idle）。"

# ============================================
echo ""
echo "=== 6. kill：终止进程 ==="
echo "任务：创建一个测试进程，然后 kill 掉"
sleep 300 &
TEST_PID=$!
echo ""
echo "已创建测试进程，PID = $TEST_PID"
echo "先用 ps 确认它存在："
ps aux | grep "sleep 300" | grep -v grep
echo ""
echo "现在手动运行：kill $TEST_PID"
echo "然后再用 ps 确认它已消失："
ps aux | grep "sleep 300" | grep -v grep || echo "  进程已不存在"
echo ""
echo "问题17：kill 发送的是什么信号？进程会立即被杀掉吗？默认发送 SIGTERM(15)，进程不会立即被杀掉（可以捕获并执行清理）。"
echo "问题18：kill -9 和 kill（默认）的区别是什么？kill -9 发送 SIGKILL，强制杀死进程，进程无法忽略；默认 kill 发送 SIGTERM，可被进程捕获并处理。"
echo "问题19：如果想让 nginx 重新加载配置，应该发送什么信号？SIGHUP"

# ============================================
echo ""
echo "=== 7. chmod：修改文件权限 ==="
echo "任务：创建测试文件，练习权限修改"
echo "secret" > /tmp/test-perm.txt
echo "已创建 /tmp/test-perm.txt"
echo ""
echo "手动执行以下命令，观察每次变化："
echo "  ls -l /tmp/test-perm.txt          ← 先看看默认权限"
echo "  chmod 000 /tmp/test-perm.txt      ← 无任何权限"
echo "  ls -l /tmp/test-perm.txt"
echo "  chmod 600 /tmp/test-perm.txt      ← 只有所有者可读写"
echo "  ls -l /tmp/test-perm.txt"
echo "  chmod 744 /tmp/test-perm.txt      ← 所有者可执行，其他人只读"
echo "  ls -l /tmp/test-perm.txt"
echo "  chmod u+x,g+w /tmp/test-perm.txt  ← 符号方式修改"
echo "  ls -l /tmp/test-perm.txt"
echo ""
echo "问题20：755 对应的 rwx 写法是什么？rwx r-x r-x"
echo "问题21：644 对应的 rwx 写法是什么？rw- r-- r--"
echo "问题22：chmod u+x 和 chmod 755 两种方式分别叫什么？chmod u+x 是符号方式，chmod 755 是数字方式（绝对模式）。"
echo "问题23：如果我想让脚本可执行但不让其他人修改，应该设什么权限？755（所有者可读写执行，组和其他只读执行）或类似 751 等。"
rm -f /tmp/test-perm.txt

# ============================================
echo ""
echo "=== 8. chown：修改文件所有者 ==="
echo "任务：理解 chown 的用法（需要 root 权限）"
echo "问题24：chown 的格式是什么？chown [选项] 用户:组 文件"
echo "问题25：为什么普通用户不能用 chown？出于安全考虑，防止普通用户随意更改文件所有权，只有 root 用户可以修改。"
echo "问题26：chown -R 的 -R 是什么意思？递归修改目录及其下所有文件和子目录的所有者。"

# ============================================
echo ""
echo "=== 练习完成！==="
