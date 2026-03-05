#!/bin/bash
# Daily Conversation Logger for Obsidian
# Usage: ./daily-logger.sh [date]
# If no date specified, uses today's date

set -e

REPO_PATH="/home/openclaw/.openclaw/workspace/obsidian-repo"
DAILY_WORK_PATH="$REPO_PATH/daily/work"
TEMPLATE_PATH="$REPO_PATH/.obsidian/templates/Daily Conversation Template.md"

# Get date (default: today)
DATE="${1:-$(date +%Y-%m-%d)}"
OUTPUT_FILE="$DAILY_WORK_PATH/${DATE}.md"

# Ensure directory exists
mkdir -p "$DAILY_WORK_PATH"

# Create file from template if it doesn't exist
if [ ! -f "$OUTPUT_FILE" ]; then
    echo "📝 Creating new daily log: $OUTPUT_FILE"
    cp "$TEMPLATE_PATH" "$OUTPUT_FILE"
else
    echo "✅ Daily log already exists: $OUTPUT_FILE"
fi

# Append conversation summary (to be filled by agent)
echo ""
echo "File ready: $OUTPUT_FILE"
echo "Edit this file to add today's conversation summary, then commit and push."
