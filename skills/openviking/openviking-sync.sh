#!/bin/bash
# openviking-sync.sh - 自动同步记忆文件到 OpenViking
# 每次记忆更新时自动导入

set -e

WORKSPACE="/home/openclaw/.openclaw/workspace"
MEMORY_DIR="$WORKSPACE/memory"
LOG_FILE="$WORKSPACE/logs/openviking-sync.log"
STATE_FILE="$WORKSPACE/.openviking/sync-state.json"

mkdir -p "$(dirname "$LOG_FILE")"
mkdir -p "$(dirname "$STATE_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

log "=========================================="
log "🦐 OpenViking 记忆同步"
log "=========================================="

# 使用 Python 处理 JSON 状态
python3 << 'PYTHON_SCRIPT'
import json
import os
import subprocess
from datetime import datetime
from pathlib import Path

WORKSPACE = "/home/openclaw/.openclaw/workspace"
MEMORY_DIR = os.path.join(WORKSPACE, "memory")
STATE_FILE = os.path.join(WORKSPACE, ".openviking/sync-state.json")

# 读取状态
def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, 'r') as f:
            return json.load(f)
    return {"synced": [], "last_sync": None}

# 保存状态
def save_state(state):
    state["last_sync"] = datetime.now().isoformat()
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f, indent=2)

# 获取已同步文件列表
state = load_state()
synced_files = set(state.get("synced", []))

# 获取所有记忆文件
memory_files = list(Path(MEMORY_DIR).glob("*.md"))
files_to_sync = [f for f in memory_files if f.name not in synced_files]

if not files_to_sync:
    print("✅ 所有记忆文件已同步")
else:
    print(f"📥 发现 {len(files_to_sync)} 个未同步文件")
    
    for f in files_to_sync:
        print(f"导入：{f.name}")
        try:
            result = subprocess.run(
                ["ov", "add-resource", str(f)],
                cwd=WORKSPACE,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print(f"  ✅ 成功")
                synced_files.add(f.name)
            else:
                print(f"  ❌ 失败：{result.stderr}")
        except Exception as e:
            print(f"  ❌ 异常：{e}")
    
    # 更新状态
    state["synced"] = sorted(list(synced_files))
    save_state(state)
    
    print(f"✅ 同步完成，共 {len(state['synced'])} 个文件")

PYTHON_SCRIPT

log "=========================================="
