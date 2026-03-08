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

# 获取已同步的文件列表
get_synced_files() {
    if [ -f "$STATE_FILE" ]; then
        cat "$STATE_FILE" | python3 -c "import sys,json; print('\n'.join(json.load(sys.stdin).get('synced', [])))"
    fi
}

# 更新同步状态
update_state() {
    local files="$1"
    echo "{\"synced\": $files, \"last_sync\": \"$(date -Iseconds)\"}" > "$STATE_FILE"
}

log "=========================================="
log "🦐 OpenViking 记忆同步"
log "=========================================="

# 获取所有记忆文件
SYNCED=$(get_synced_files)
FILES_TO_SYNC=()

for f in "$MEMORY_DIR"/*.md; do
    if [ -f "$f" ]; then
        filename=$(basename "$f")
        if ! echo "$SYNCED" | grep -q "$filename"; then
            FILES_TO_SYNC+=("$f")
        fi
    fi
done

if [ ${#FILES_TO_SYNC[@]} -eq 0 ]; then
    log "✅ 所有记忆文件已同步"
else
    log "📥 发现 ${#FILES_TO_SYNC[@]} 个未同步文件"
    
    SYNCED_LIST="["
    FIRST=true
    
    for f in "${FILES_TO_SYNC[@]}"; do
        filename=$(basename "$f")
        log "导入：$filename"
        
        cd "$WORKSPACE" && ov add-resource "$f" 2>&1 | tee -a "$LOG_FILE"
        
        if [ "$FIRST" = true ]; then
            SYNCED_LIST="$SYNCED_LIST\"$filename\""
            FIRST=false
        else
            SYNCED_LIST="$SYNCED_LIST, \"$filename\""
        fi
    done
    
    # 合并已同步列表
    if [ -f "$STATE_FILE" ]; then
        EXISTING=$(cat "$STATE_FILE" | python3 -c "import sys,json; print(','.join(json.load(sys.stdin).get('synced', [])))")
        if [ -n "$EXISTING" ]; then
            SYNCED_LIST="$SYNCED_LIST, $EXISTING"
        fi
    fi
    
    SYNCED_LIST="[$SYNCED_LIST]"
    update_state "$SYNCED_LIST"
    
    log "✅ 同步完成，共 $(echo "$SYNCED_LIST" | python3 -c "import sys,json; print(len(json.load(sys.stdin)['synced']))") 个文件"
fi

log "=========================================="
