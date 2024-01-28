#!/bin/bash

# ./getMatchDetails.sh --id "match_id"
# ./getMatchDetails.sh --player "player_id"

# Validate number of arguments
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 [--local] [--id match_id] [--player player_id]"
    exit 1
fi

# Define your local and remote URLs
LOCAL_URL="http://localhost:5001/gamesetmatch-ef350/us-central1/deleteMatch"
REMOTE_URL="https://us-central1-gamesetmatch-ef350.cloudfunctions.net/deleteMatch"

# Initialize variables
MATCH_ID=""
PLAYER_ID=""
URL="$REMOTE_URL"  # Default to remote URL

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --local) URL="$LOCAL_URL"; shift ;;
        --id) MATCH_ID="$2"; shift 2 ;;
        --player) PLAYER_ID="$2"; shift 2 ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
done

# Construct and send the curl command
curl -X POST "$URL" \
-H "Content-Type: application/json" \
-d "{\"match_id\": \"$MATCH_ID\", \"player_id\": \"$PLAYER_ID\"}"
