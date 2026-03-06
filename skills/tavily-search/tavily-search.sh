#!/bin/bash
# Tavily Search Helper Script
# Usage: ./tavily-search.sh "search query" [max_results]

QUERY="$1"
MAX_RESULTS="${2:-5}"
API_KEY="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"

if [ -z "$QUERY" ]; then
    echo "Usage: $0 \"search query\" [max_results]"
    exit 1
fi

curl -s -X POST https://api.tavily.com/search \
  -H "Content-Type: application/json" \
  -d "{
    \"api_key\": \"$API_KEY\",
    \"query\": \"$QUERY\",
    \"max_results\": $MAX_RESULTS
  }"
