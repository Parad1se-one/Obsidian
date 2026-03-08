#!/bin/bash
# Tavily Search Helper Script
# Usage: ./tavily-search.sh "search query" [max_results]
# 
# API Key Configuration:
#   Option 1: Export environment variable
#     export TAVILY_API_KEY="your_api_key"
#   Option 2: Store in .env file (recommended for development)
#     Create .env file with: TAVILY_API_KEY=your_api_key
#   Option 3: Use default dev key (not recommended for production)

QUERY="$1"
MAX_RESULTS="${2:-5}"

# Load API key from environment variable or use default (dev only)
API_KEY="${TAVILY_API_KEY:-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}"

if [ -z "$QUERY" ]; then
    echo "Usage: $0 \"search query\" [max_results]"
    echo ""
    echo "API Key Setup:"
    echo "  export TAVILY_API_KEY=\"your_api_key\""
    echo ""
    echo "Get your API key at: https://app.tavily.com/"
    exit 1
fi

curl -s -X POST https://api.tavily.com/search \
  -H "Content-Type: application/json" \
  -d "{
    \"api_key\": \"$API_KEY\",
    \"query\": \"$QUERY\",
    \"max_results\": $MAX_RESULTS
  }"
