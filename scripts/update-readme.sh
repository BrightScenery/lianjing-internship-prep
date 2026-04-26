#!/bin/bash
# 自动更新 README.md 的进度总览
# 从 metrics/progress.json 读取数据，替换 README 中的对应内容

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
README="$PROJECT_DIR/README.md"
METRICS="$PROJECT_DIR/metrics/progress.json"

# 从 progress.json 读取数据
get_val() {
    grep "\"$1\"" "$METRICS" | head -1 | sed 's/.*: *//; s/[,} ]//g; s/"//g'
}

CURRENT_DAY=$(get_val "current_day")
TOTAL_COMMITS=$(get_val "total_commits")
CONSECUTIVE_DAYS=$(get_val "consecutive_days")
TOTAL_CODE_LINES=$(get_val "total_code_lines")
PROJECTS_COMPLETED=$(get_val "projects_completed")
TOTAL_NOTES="$CURRENT_DAY"

# 计算当前周次（用 python3 避免 WSL2 date 兼容问题）
WEEK_NUM=$(python3 -c "
import datetime
start = datetime.date(2026, 4, 22)
today = datetime.date.today()
diff = (today - start).days
week = diff // 7 + 1
print(max(1, min(6, week)))
" 2>/dev/null || echo 1)

# 简化版：用 awk 做整块替换，避免 sed 特殊字符问题
awk -v day="$CURRENT_DAY" -v commits="$TOTAL_COMMITS" \
    -v consecutive="$CONSECUTIVE_DAYS" -v lines="$TOTAL_CODE_LINES" \
    -v projects="$PROJECTS_COMPLETED" -v notes="$TOTAL_NOTES" \
    -v week="$WEEK_NUM" '
BEGIN { in_progress=0; in_roadmap=0; in_tech=0 }

# 进度总览区块 - 输出新内容
/\| 📅 学习天数 \|/ {
    print "| 📅 学习天数 | " day " / 45 |"
    print "| 🔥 连续 commit 天数 | " consecutive " |"
    print "| 📝 代码提交次数 | " commits " |"
    print "| 💻 累计代码行数 | " lines " |"
    print "| 📦 完成项目 | " projects " / 4 |"
    print "| 📖 学习笔记 | " notes " / 45 |"
    skip=1; next
}
skip && /\| 📖/ { skip=0; next }
skip { next }

# 路线图状态
/第1周.*Linux/ {
    s = (week==1) ? "🔥 进行中" : ((week>1) ? "✅ 已完成" : "⬜ 未开始")
    sub(/\| ⬜ .*\|$/, "| " s " |")
    sub(/\| 🔥 .*\|$/, "| " s " |")
    sub(/\| ✅ .*\|$/, "| " s " |")
}
/第2周.*Docker/ {
    s = (week==2) ? "🔥 进行中" : ((week>2) ? "✅ 已完成" : "⬜ 未开始")
    sub(/\| ⬜ .*\|$/, "| " s " |")
    sub(/\| 🔥 .*\|$/, "| " s " |")
    sub(/\| ✅ .*\|$/, "| " s " |")
}
/第3周.*K8s/ {
    s = (week==3) ? "🔥 进行中" : ((week>3) ? "✅ 已完成" : "⬜ 未开始")
    sub(/\| ⬜ .*\|$/, "| " s " |")
    sub(/\| 🔥 .*\|$/, "| " s " |")
    sub(/\| ✅ .*\|$/, "| " s " |")
}
/第4周.*RAG/ {
    s = (week==4) ? "🔥 进行中" : ((week>4) ? "✅ 已完成" : "⬜ 未开始")
    sub(/\| ⬜ .*\|$/, "| " s " |")
    sub(/\| 🔥 .*\|$/, "| " s " |")
    sub(/\| ✅ .*\|$/, "| " s " |")
}
/第5周.*Agent/ {
    s = (week==5) ? "🔥 进行中" : ((week>5) ? "✅ 已完成" : "⬜ 未开始")
    sub(/\| ⬜ .*\|$/, "| " s " |")
    sub(/\| 🔥 .*\|$/, "| " s " |")
    sub(/\| ✅ .*\|$/, "| " s " |")
}
/第6周.*邮件/ {
    s = (week==6) ? "🔥 进行中" : ((week>6) ? "✅ 已完成" : "⬜ 未开始")
    sub(/\| ⬜ .*\|$/, "| " s " |")
    sub(/\| 🔥 .*\|$/, "| " s " |")
    sub(/\| ✅ .*\|$/, "| " s " |")
}

{ print }
' "$README" > "$README.tmp" && mv "$README.tmp" "$README"

echo "README updated: Day $CURRENT_DAY, $TOTAL_COMMITS commits, $TOTAL_CODE_LINES lines, Week $WEEK_NUM"
