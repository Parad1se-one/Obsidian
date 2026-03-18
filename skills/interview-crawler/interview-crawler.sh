#!/bin/bash
# LLM 面试题目爬虫 - 定时任务脚本
# 每天 09:00 执行

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(dirname "$SCRIPT_DIR")"
LOG_DIR="$WORKSPACE_DIR/logs"
LOG_FILE="$LOG_DIR/interview-crawler-$(date +%Y-%m-%d).log"

# 创建日志目录
mkdir -p "$LOG_DIR"

echo "[$(date '+%Y-%m-%d %H:%M:%S')] ========== 面试题目爬虫开始 ==========" | tee -a "$LOG_FILE"

# 激活虚拟环境（如果有）
if [ -f "$WORKSPACE_DIR/venv/bin/activate" ]; then
    source "$WORKSPACE_DIR/venv/bin/activate"
fi

# 执行爬虫
cd "$SCRIPT_DIR"
python3 crawler.py 2>&1 | tee -a "$LOG_FILE"

# Git 提交推送
if [ -d "$WORKSPACE_DIR/obsidian-repo" ]; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始 Git 提交..." | tee -a "$LOG_FILE"
    cd "$WORKSPACE_DIR/obsidian-repo"
    
    git add .
    
    if ! git diff --cached --quiet; then
        git commit -m "📝 LLM 面试题库：$(date +%Y-%m-%d) 自动抓取"
        git push 2>&1 | tee -a "$LOG_FILE"
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✓ Git 推送成功" | tee -a "$LOG_FILE"
    else
        echo "[$(date '+%Y-%m-%d %H:%M:%S')] 无变更，跳过提交" | tee -a "$LOG_FILE"
    fi
fi

echo "[$(date '+%Y-%m-%d %H:%M:%S')] ========== 面试题目爬虫结束 ==========" | tee -a "$LOG_FILE"
