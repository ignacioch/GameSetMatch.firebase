#!/bin/bash

# ./getMatchDetails.sh --id "match_id"
# ./getMatchDetails.sh --player "player_id"

# Validate number of arguments
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 [--id match_id] [--player player_id]"
    exit 1
fi

# Initialize variables
MATCH_ID=""
PLAYER_ID=""

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --id) MATCH_ID="$2"; shift ;;
        --player) PLAYER_ID="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

# URL of the Cloud Function
URL="http://localhost:5001/gamesetmatch-ef350/us-central1/getMatchDetailsEndpoint"

# Construct and send the curl command
curl -X POST "$URL" \
-H "Content-Type: application/json" \
-d "{\"match_id\": \"$MATCH_ID\", \"player_id\": \"$PLAYER_ID\"}"
