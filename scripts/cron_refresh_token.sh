#!/bin/bash
# Longbridge Token 自动刷新脚本
# 由 at 定时任务触发

set -e

PROJECT_DIR="/root/.openclaw/workspace/Longbridge_tools"
LOG_FILE="/root/.openclaw/workspace/memory/token_refresh.log"

# 记录日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

log "=== 开始刷新 Longbridge Token ==="

# 进入项目目录
cd "$PROJECT_DIR"

# 执行刷新
if python3 scripts/refresh_token.py >> "$LOG_FILE" 2>&1; then
    log "✅ Token 刷新成功!"
    
    # 发送飞书通知
    curl -s -X POST "https://open.feishu.cn/open-apis/bot/v2/hook/" \
        -H "Content-Type: application/json" \
        -d '{
            "msg_type": "text",
            "content": {
                "text": "✅ Longbridge Token 已自动刷新成功！\n时间: '"$(date '+%Y-%m-%d %H:%M:%S')"'"
            }
        }' >> "$LOG_FILE" 2>&1 || true
    
    log "通知已发送"
else
    log "❌ Token 刷新失败!"
    
    # 发送失败通知
    curl -s -X POST "https://open.feishu.cn/open-apis/bot/v2/hook/" \
        -H "Content-Type: application/json" \
        -d '{
            "msg_type": "text",
            "content": {
                "text": "⚠️ Longbridge Token 刷新失败，请手动处理！\n时间: '"$(date '+%Y-%m-%d %H:%M:%S')"'"
            }
        }' >> "$LOG_FILE" 2>&1 || true
fi

log "=== 刷新任务结束 ==="