#!/bin/bash

# Validate number of arguments
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 [--local] [--id player_id] [--name player_name] [--email player_email]"
    exit 1
fi

# Define your local and remote URLs
LOCAL_URL="http://localhost:5001/gamesetmatch-ef350/us-central1/deleteMatch"
REMOTE_URL="https://us-central1-gamesetmatch-ef350.cloudfunctions.net/deleteMatch"


# Initialize variables
PLAYER_ID=""
PLAYER_NAME=""
PLAYER_EMAIL=""

URL="$REMOTE_URL"  # Default to remote URL

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --local) URL="$LOCAL_URL"; shift ;;
        --id) PLAYER_ID="$2"; shift 2;;
        --name) PLAYER_NAME="$2"; shift 2;;
        --email) PLAYER_EMAIL="$2"; shift 2;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
done

# URL of the Cloud Function
URL="http://localhost:5001/gamesetmatch-ef350/us-central1/getPlayerDetails"

# Construct and send the curl command
curl -X POST "$URL" \
-H "Content-Type: application/json" \
-d "{\"player_id\": \"$PLAYER_ID\", \"name\": \"$PLAYER_NAME\", \"email\": \"$PLAYER_EMAIL\"}"
