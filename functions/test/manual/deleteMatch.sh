#!/bin/bash

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 match_id"
    exit 1
fi

MATCH_ID="$1"
URL="http://localhost:5001/gamesetmatch-ef350/us-central1/deleteMatch"

curl -X POST "$URL" -d "match_id=$MATCH_ID"
