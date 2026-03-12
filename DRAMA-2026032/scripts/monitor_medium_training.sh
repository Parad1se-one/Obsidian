#!/bin/bash
# Medium 难度训练监控脚本
# 每 5 分钟检查一次进度并记录

LOG_FILE="/home/openclaw/.openclaw/workspace/logs/medium_training_monitor.log"
mkdir -p /home/openclaw/.openclaw/workspace/logs

echo "==========================================" >> "$LOG_FILE"
echo "Medium 训练监控启动 | $(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
echo "==========================================" >> "$LOG_FILE"

while true; do
    echo "" >> "$LOG_FILE"
    echo "检查时间：$(date '+%Y-%m-%d %H:%M:%S')" >> "$LOG_FILE"
    echo "----------------------------------------" >> "$LOG_FILE"
    
    for alg in ippo ippo_rm mappo mappo_rm dqn; do
        log="/tmp/medium_${alg}.log"
        if [ -f "$log" ]; then
            # 提取最新进度
            progress=$(grep -o "Ep [0-9]*/500" "$log" 2>/dev/null | tail -1)
            reward=$(grep -o "reward=[0-9.-]*" "$log" 2>/dev/null | tail -1)
            echo "[$alg] $progress $reward" >> "$LOG_FILE"
        else
            echo "[$alg] 日志不存在" >> "$LOG_FILE"
        fi
    done
    
    # 检查进程是否还在运行
    running=$(ps aux | grep "train_.*medium.py" | grep -v grep | wc -l)
    echo "运行中进程数：$running" >> "$LOG_FILE"
    
    sleep 300  # 5 分钟
done
