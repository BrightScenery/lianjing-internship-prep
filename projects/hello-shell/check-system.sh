#!/bin/bash
# 系统状态检查脚本 - 第1周项目
# 功能：输出当前系统的关键状态信息，用于服务器巡检

echo "========================================"
echo "  系统状态巡检报告"
echo "  日期: $(date '+%Y-%m-%d %H:%M:%S')"
echo "========================================"

# 1. 系统信息
echo ""
echo "[1/9] 系统信息"
echo "  主机名: $(hostname)"
echo "  系统:   $(uname -s) $(uname -r)"

# 2. CPU 负载
echo ""
echo "[2/9] CPU 负载"
echo "  $(uptime)"

# 3. 内存使用
echo ""
echo "[3/9] 内存使用"
free -m | awk 'NR==2 {printf "  总计: %4d MB | 已用: %4d MB | 可用: %4d MB | 使用率: %.1f%%\n", $2, $3, $4, $3/$2*100}'

# 4. 磁盘使用（所有挂载点）
echo ""
echo "[4/9] 磁盘使用（挂载点）"
df -h | awk 'NR>1 {printf "  %-30s 总计: %8s  已用: %8s  可用: %8s  使用率: %s\n", $6, $2, $3, $4, $5}'

# 5. 目录磁盘占用 TOP 5
echo ""
echo "[5/9] 目录磁盘占用 TOP 5（根目录一级，排除挂载点）"
du --max-depth=1 -h / --exclude=/mnt --exclude=/proc --exclude=/sys --exclude=/dev --exclude=/run 2>/dev/null | sort -hr | head -5 | awk '{printf "  %-40s %s\n", $2, $1}'

# 6. 进程统计
echo ""
echo "[6/9] 进程统计"
echo "  当前进程总数: $(($(ps aux | wc -l) - 1))"
echo "  运行中 (R):   $(ps aux | awk '$8~/R/ {count++} END {print count+0}')"
echo "  睡眠中 (S):   $(ps aux | awk '$8~/S/ {count++} END {print count+0}')"
echo "  僵尸 (Z):     $(ps aux | awk '$8~/Z/ {count++} END {print count+0}')"

# 7. CPU 占用 TOP 3
echo ""
echo "[7/9] CPU 占用 TOP 3"
ps aux --sort=-%cpu | awk 'NR>1 && NR<=4 {printf "  PID %-8s CPU: %5s%%  MEM: %5s%%  %s\n", $2, $3, $4, $11}'

# 8. 内存占用 TOP 3
echo ""
echo "[8/9] 内存占用 TOP 3"
ps aux --sort=-%mem | awk 'NR>1 && NR<=4 {printf "  PID %-8s MEM: %5s%%  CPU: %5s%%  %s\n", $2, $4, $3, $11}'

# 9. 登录用户
echo ""
echo "[9/9] 当前登录用户"
if who 2>/dev/null | grep -q .; then
    who | awk '{printf "  %-10s %-12s %s\n", $1, $2, $3}'
else
    echo "  无用户登录（WSL 环境）"
fi

echo ""
echo "========================================"
echo "  巡检完成"
echo "========================================"
