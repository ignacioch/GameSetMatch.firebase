#!/bin/bash

# Validate number of arguments
if [ "$#" -ne 5 ]; then
    echo "Usage: $0 player_a_id player_b_id score match_date location"
    exit 1
fi

# Assign arguments to variables
PLAYER_A_ID="$1"
PLAYER_B_ID="$2"
SCORE="$3"
MATCH_DATE="$4"
LOCATION="$5"

# URL of the Cloud Function
URL="http://localhost:5001/gamesetmatch-ef350/us-central1/addMatch"

# Construct and send the curl command
curl -X POST "$URL" \
-H "Content-Type: application/json" \
-d "{\"player_a_id\": \"$PLAYER_A_ID\", \"player_b_id\": \"$PLAYER_B_ID\", \"score\": \"$SCORE\", \"date\": \"$MATCH_DATE\", \"location\": \"$LOCATION\"}"
