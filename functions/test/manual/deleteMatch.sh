#!/bin/bash

# Define your local and remote URLs
LOCAL_URL="http://localhost:5001/gamesetmatch-ef350/us-central1/deleteMatch"
REMOTE_URL="https://us-central1-gamesetmatch-ef350.cloudfunctions.net/deleteMatch"

# Check for minimum number of arguments
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 [--local] match_id"
    exit 1
fi

# Check if the first argument is --local
if [ "$1" == "--local" ]; then
    URL="$LOCAL_URL"
    MATCH_ID="$2"
else
    URL="$REMOTE_URL"
    MATCH_ID="$1"
fi

# Perform the curl request
curl -X POST "$URL" -H "Content-Type: application/json" -d "{\"match_id\": \"$MATCH_ID\"}"
