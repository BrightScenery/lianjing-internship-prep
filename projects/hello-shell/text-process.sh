#!/bin/bash
# ============================================
# 文本处理练习 - 2026-04-24
# 学习主题：grep / sed / awk / cut / sort / head / tail / 管道 / 重定向
# 练习文件位置：~/lianjing-shell-practice/
# ============================================

LOG="$HOME/lianjing-shell-practice/server.log"
CSV="$HOME/lianjing-shell-practice/scores.csv"

echo "=== 第1关：grep 搜索 ==="
# 1. 找出所有 ERROR 行
echo "--- 所有错误日志 ---"
grep "ERROR" $LOG

# 2. 统计 ERROR 的数量
echo "--- 错误数量 ---"
grep -c "ERROR" $LOG

# 独立练习：找出所有包含 192.168.1.100 的行
echo "--- 192.168.1.100 的请求 ---"
grep "192.168.1.100" $LOG
echo ""

echo "=== 第2关：管道 | ==="
# 3. 统计日志中有多少个 WARNING
echo "--- WARNING 数量 ---"
grep "WARNING" $LOG | wc -l

# 独立练习：统计有多少次请求来自 10.0.0.1
echo "--- 10.0.0.1 请求次数 ---"
grep "10.0.0.1" $LOG | wc -l
echo ""

echo "=== 第3关：cut 切割 ==="
# 4. 从 CSV 中只提取"姓名"列（第1列，逗号分隔）
echo "--- 学生姓名 ---"
cut -d',' -f1 $CSV

# 5. 提取姓名和数学成绩（第1列和第3列）
echo "--- 姓名和数学成绩 ---"
cut -d',' -f1,3 $CSV
echo ""

echo "=== 第4关：sort 排序 ==="
# 6. 按数学成绩排序（跳过表头）
echo "--- 按数学成绩排序 ---"
tail -n +2 $CSV | sort -t',' -k3 -nr | head

# 解释：
# tail -n +2  = 从第2行开始（跳过表头"姓名,语文,数学,英语"）
# sort -t','  = 用逗号分隔
#       -k3   = 按第3列（数学）排序
#       -nr   = 数字、逆序（从高到低）
echo ""

echo "=== 第5关：head / tail ==="
# 7. 查看日志的前5行
echo "--- 日志前5行 ---"
head -5 $LOG

# 8. 查看日志的最后3行
echo "--- 日志最后3行 ---"
tail -3 $LOG
echo ""

echo "=== 第6关：sed 替换 ==="
# 9. 把日志中的 ERROR 替换为 [严重]
echo "--- 替换 ERROR ---"
sed 's/ERROR/[严重]/g' $LOG | head -5

# 独立练习：把日志里的 192.168 替换为 "内网"
echo "--- 替换 192.168 为 内网 ---"
sed 's/192\.168/内网/g' $LOG | head -3
echo ""

echo "=== 第7关：重定向 ==="
# 10. 把所有 ERROR 行保存到文件
grep "ERROR" $LOG > $HOME/lianjing-shell-practice/errors_only.txt
echo "--- 已保存 errors_only.txt ---"
cat $HOME/lianjing-shell-practice/errors_only.txt
echo ""

echo "=== 第8关：综合实战 ==="
# 计算每个学生的总分，按总分从高到低排序
echo "--- 学生总分排名 ---"
tail -n +2 $CSV | awk -F',' '{total=$2+$3+$4; print $1": "total"分"}' | sort -t':' -k2 -nr

echo ""
echo "=== 练习完成！==="
echo "下一步：把 TODO 部分自己写一遍，然后尝试不看我写的代码，自己从头写一遍。"
