#!/bin/bash
# Automated Daily Conversation Logger
# Runs at midnight, creates/updates daily work log, commits and pushes

set -e

REPO_PATH="/home/openclaw/.openclaw/workspace/obsidian-repo"
DAILY_WORK_PATH="$REPO_PATH/daily/work"
TEMPLATE_PATH="$REPO_PATH/.obsidian/templates/Daily Conversation Template.md"
SESSION_LOG_PATH="/home/openclaw/.openclaw/workspace/memory"

# Get yesterday's date (since we're running at midnight)
YESTERDAY=$(date -d "yesterday" +%Y-%m-%d)
TODAY=$(date +%Y-%m-%d)
OUTPUT_FILE="$DAILY_WORK_PATH/${YESTERDAY}.md"

cd "$REPO_PATH"

# Configure git
git config user.name "小虾"
git config user.email "xiaoxia@local"

# Create file from template if it doesn't exist
if [ ! -f "$OUTPUT_FILE" ]; then
    echo "📝 Creating daily log for $YESTERDAY"
    cp "$TEMPLATE_PATH" "$OUTPUT_FILE"
    
    # Update the date in the file
    sed -i "s/<% tp.date.now(\"YYYY-MM-DD\") %>/$YESTERDAY/g" "$OUTPUT_FILE"
    sed -i "s/<% tp.date.now(\"YYYY-MM-DD HH:mm\") %>/$TODAY 00:00/g" "$OUTPUT_FILE"
else
    echo "✅ Daily log already exists: $OUTPUT_FILE"
fi

# Stage, commit, and push
git add "$OUTPUT_FILE"
git commit -m "📝 Daily log: $YESTERDAY" || echo "No changes to commit"
git push origin main || git push origin master || echo "Push failed - may need manual intervention"

echo "✅ Daily log completed for $YESTERDAY"
