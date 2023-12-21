#!/bin/bash

# Validate number of arguments
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 [--id player_id] [--name player_name] [--email player_email]"
    exit 1
fi

# Initialize variables
PLAYER_ID=""
PLAYER_NAME=""
PLAYER_EMAIL=""

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case $1 in
        --id) PLAYER_ID="$2"; shift ;;
        --name) PLAYER_NAME="$2"; shift ;;
        --email) PLAYER_EMAIL="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

# URL of the Cloud Function
URL="http://localhost:5001/gamesetmatch-ef350/us-central1/getPlayerDetails"

# Construct and send the curl command
curl -X POST "$URL" \
-H "Content-Type: application/json" \
-d "{\"player_id\": \"$PLAYER_ID\", \"name\": \"$PLAYER_NAME\", \"email\": \"$PLAYER_EMAIL\"}"
