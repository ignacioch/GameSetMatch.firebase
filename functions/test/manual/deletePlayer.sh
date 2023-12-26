#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 player_id"
    exit 1
fi

PLAYER_ID="$1"
URL="http://localhost:5001/gamesetmatch-ef350/us-central1/deletePlayer"

curl -X POST "$URL" -d "player_id=$PLAYER_ID"
