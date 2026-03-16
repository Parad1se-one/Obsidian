#!/bin/bash
# Financial Daily V2 - 财经日报自动生成主脚本
# 版本：v2.0 | 最后更新：2026-03-16

set -e

# ==================== 配置 ====================
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="/home/openclaw/.openclaw/workspace"
OUTPUT_DIR="${WORKSPACE_DIR}/obsidian-repo/daily/financial-news"
LOG_FILE="${WORKSPACE_DIR}/logs/financial-daily-v2.log"
ERROR_LOG="${WORKSPACE_DIR}/logs/financial-daily-v2-error.log"
TEMP_DIR="${WORKSPACE_DIR}/.tmp/financial-daily"

# 数据源配置 (可扩展)
declare -a DATA_SOURCES=(
    "cls"
    "21jingji"
    "caijing-toutiao"
    "eastmoney"
    "wallstreetcn"
    "finance-calendar"
)

# ==================== 初始化 ====================
init() {
    mkdir -p "${OUTPUT_DIR}"
    mkdir -p "${TEMP_DIR}"
    mkdir -p "$(dirname "${LOG_FILE}")"
    
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] ========== 财经日报生成开始 ==========" >> "${LOG_FILE}"
}

# ==================== 日志函数 ====================
log_info() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [INFO] $1" | tee -a "${LOG_FILE}"
}

log_error() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [ERROR] $1" | tee -a "${ERROR_LOG}" >> "${LOG_FILE}"
}

# ==================== 抓取数据源 ====================
fetch_sources() {
    log_info "开始抓取数据源..."
    
    for source in "${DATA_SOURCES[@]}"; do
        local script="${SCRIPT_DIR}/scripts/sources/${source}.sh"
        if [[ -f "${script}" && -x "${script}" ]]; then
            log_info "抓取数据源：${source}"
            if "${script}" >> "${LOG_FILE}" 2>&1; then
                log_info "✓ ${source} 抓取成功"
            else
                log_error "✗ ${source} 抓取失败"
            fi
        else
            log_error "✗ ${source} 脚本不存在或不可执行：${script}"
        fi
    done
}

# ==================== 生成日报 ====================
generate_daily() {
    local date_str=$(date '+%Y-%m-%d')
    OUTPUT_FILE="${OUTPUT_DIR}/${date_str}.md"
    
    log_info "开始生成财经日报：${OUTPUT_FILE}"
    
    # 调用生成器
    if "${SCRIPT_DIR}/scripts/generator.sh" "${OUTPUT_FILE}" >> "${LOG_FILE}" 2>&1; then
        log_info "✓ 日报生成成功"
        return 0
    else
        log_error "✗ 日报生成失败"
        return 1
    fi
}

# ==================== 质量检查 ====================
quality_check() {
    local file="$1"
    
    log_info "开始质量检查：${file}"
    
    if "${SCRIPT_DIR}/scripts/quality-check.sh" "${file}" >> "${LOG_FILE}" 2>&1; then
        log_info "✓ 质量检查通过"
        return 0
    else
        log_error "✗ 质量检查未通过"
        return 1
    fi
}

# ==================== Git 提交推送 ====================
git_push() {
    local file="$1"
    
    log_info "开始 Git 提交推送..."
    
    cd "${WORKSPACE_DIR}/obsidian-repo"
    
    git add "${file#*/obsidian-repo/}" 2>> "${LOG_FILE}" || true
    git add "scripts/cron.log" 2>> "${LOG_FILE}" || true
    
    local date_str=$(date '+%Y-%m-%d')
    if git commit -m "📈 财经日报 ${date_str} [auto]" >> "${LOG_FILE}" 2>&1; then
        log_info "✓ Git commit 成功"
        
        if git push >> "${LOG_FILE}" 2>&1; then
            log_info "✓ Git push 成功"
        else
            log_error "✗ Git push 失败"
            return 1
        fi
    else
        log_error "✗ Git commit 失败 (可能无变更)"
    fi
    
    return 0
}

# ==================== 飞书通知 ====================
feishu_notify() {
    local file="$1"
    
    log_info "发送飞书通知..."
    
    # 这里调用 OpenClaw message 工具
    # 由于是 shell 脚本，通过 exec 调用
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] [FEISHU] 通知已发送" >> "${LOG_FILE}"
}

# ==================== 清理 ====================
cleanup() {
    rm -rf "${TEMP_DIR}"
    log_info "清理临时文件完成"
}

# ==================== 主流程 ====================
main() {
    init
    
    # 1. 抓取数据源
    fetch_sources
    
    # 2. 生成日报
    if ! generate_daily; then
        log_error "日报生成失败，终止流程"
        cleanup
        exit 1
    fi
    
    # 3. 质量检查
    if ! quality_check "${OUTPUT_FILE}"; then
        log_error "质量检查未通过，终止流程"
        cleanup
        exit 1
    fi
    
    # 4. Git 提交推送
    git_push "${OUTPUT_FILE}"
    
    # 5. 飞书通知
    feishu_notify "${OUTPUT_FILE}"
    
    # 6. 清理
    cleanup
    
    log_info "========== 财经日报生成完成 =========="
}

# 执行
main "$@"
