#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 [--local] player_id"
    exit 1
fi


LOCAL_URL="http://localhost:5001/gamesetmatch-ef350/us-central1/deletePlayer"
LOCAL_URL="https://us-central1-gamesetmatch-ef350.cloudfunctions.net/deletePlayer"

# Check if the first argument is --local
if [ "$1" == "--local" ]; then
    URL="$LOCAL_URL"
    PLAYER_ID="$2"
else
    URL="$REMOTE_URL"
    PLAYER_ID="$1"
fi

curl -X POST "$URL" -H "Content-Type: application/json" -d "{\"player_id\": \"$PLAYER_ID\"}"
