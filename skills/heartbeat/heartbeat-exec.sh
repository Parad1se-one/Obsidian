#!/bin/bash
# heartbeat-exec.sh - 自动执行 Heartbeat 任务
# 根据当前时间自动判断并执行对应任务

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE="/home/openclaw/.openclaw/workspace"
LOG_FILE="$WORKSPACE/logs/heartbeat-exec.log"

# 创建日志目录
mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 获取当前时间
CURRENT_HOUR=$(date +%H)
CURRENT_MIN=$(date +%M)
CURRENT_DAY=$(date +%u)  # 1=Monday, 7=Sunday
CURRENT_TIME="${CURRENT_HOUR}:${CURRENT_MIN}"

log "=========================================="
log "🦐 Heartbeat 自动执行 | ${CURRENT_TIME} | 周${CURRENT_DAY}"
log "=========================================="

# 任务执行窗口 (允许前后 30 分钟误差)
# 09:00 RL 学习 - 窗口 08:30-09:30
# 14:00 RL 论文 - 窗口 13:30-14:30
# 20:00 RL 代码 - 窗口 19:30-20:30
# 07:30 财经日报 - 窗口 07:00-08:00 (工作日)

execute_rl_study() {
    local topic=$1
    log "📚 执行 RL 学习：$topic"
    cd "$WORKSPACE" && ./skills/rl-researcher/rl-study.sh "$topic" 30
    log "✅ RL 学习完成：$topic"
}

execute_financial_daily() {
    log "📈 执行财经日报生成"
    cd "$WORKSPACE" && ./skills/financial-daily/financial-daily.sh
    log "✅ 财经日报完成"
}

execute_weekly_maintenance() {
    log "🧹 执行周日知识维护"
    # 这里可以调用专门的维护脚本
    log "📝 知识维护需要手动确认（涉及索引更新）"
}

# 检查是否在执行窗口内
in_window() {
    local target_hour=$1
    local target_min=$2
    local window=$3  # 分钟窗口
    
    local target_total=$((target_hour * 60 + target_min))
    local current_total=$((CURRENT_HOUR * 60 + CURRENT_MIN))
    local diff=$((current_total - target_total))
    
    # 取绝对值
    if [ $diff -lt 0 ]; then
        diff=$((-diff))
    fi
    
    [ $diff -le $window ]
}

# 检查今日是否已执行 (通过检查日志)
already_executed() {
    local task=$1
    local today=$(date +%Y-%m-%d)
    
    if grep -q "$task.*$today" "$LOG_FILE" 2>/dev/null; then
        return 0
    fi
    return 1
}

# ========== 任务调度 ==========

# 财经日报 (工作日 07:30)
if [ "$CURRENT_DAY" -le 5 ] && in_window 7 30 30; then
    if ! already_executed "财经日报"; then
        execute_financial_daily
    else
        log "⏭️  财经日报今日已执行"
    fi
fi

# RL 学习 - 上午 (09:00)
if in_window 9 0 60; then
    if ! already_executed "RL 学习 - 上午"; then
        # 自动选择主题（可根据日期轮换）
        local topics=("basics" "algorithms")
        local topic=${topics[$((RANDOM % ${#topics[@]}))]}
        execute_rl_study "$topic"
    else
        log "⏭️  RL 上午学习今日已执行"
    fi
fi

# RL 学习 - 下午 (14:00)
if in_window 14 0 60; then
    if ! already_executed "RL 学习 - 下午"; then
        execute_rl_study "paper"
    else
        log "⏭️  RL 下午学习今日已执行"
    fi
fi

# RL 学习 - 晚间 (20:00)
if in_window 20 0 90; then
    if ! already_executed "RL 学习 - 晚间"; then
        execute_rl_study "code"
    else
        log "⏭️  RL 晚间学习今日已执行"
    fi
fi

# 周日知识维护 (10:00 - 只在周日)
if [ "$CURRENT_DAY" -eq 7 ] && in_window 10 0 120; then
    if ! already_executed "周日维护"; then
        execute_weekly_maintenance
    else
        log "⏭️  周日维护今日已执行"
    fi
fi

log "=========================================="
log "✅ Heartbeat 检查完成"
log "=========================================="
