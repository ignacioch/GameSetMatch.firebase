#!/bin/bash

# Validate number of arguments
if [ "$#" -lt 5 ]; then
    echo "Usage: $0 [--local] name email dob level areas"
    echo "areas should be a comma-separated list without spaces, e.g., area1,area2"
    exit 1
fi

# URL of the Cloud Function
LOCAL_URL="http://localhost:5001/gamesetmatch-ef350/us-central1/registerPlayer"
REMOTE_URL="https://us-central1-gamesetmatch-ef350.cloudfunctions.net/registerPlayer"

# Initialize areas variable
AREAS=""

# Check if the first argument is --local
if [ "$1" == "--local" ]; then
    URL="$LOCAL_URL"
    NAME="$2"
    EMAIL="$3"
    DOB="$4"
    LEVEL="$5"
    AREAS="$6"
else
    URL="$REMOTE_URL"
    NAME="$1"
    EMAIL="$2"
    DOB="$3"
    LEVEL="$4"
    AREAS="$5"
fi

# Convert areas from a comma-separated list to a JSON array
IFS=',' read -r -a AREAS_ARRAY <<< "$AREAS"
AREAS_JSON=$(printf '"%s",' "${AREAS_ARRAY[@]}" | sed 's/,$//')
AREAS_JSON="[${AREAS_JSON}]"

# Construct and send the curl command
curl -X POST "$URL" \
-H "Content-Type: application/json" \
-d "{
    \"name\": \"$NAME\",
    \"email\": \"$EMAIL\",
    \"DOB\": \"$DOB\",
    \"level\": \"$LEVEL\",
    \"areas\": $AREAS_JSON
}"
