#!/bin/bash

# Validate number of arguments
if [ "$#" -ne 4 ]; then
    echo "Usage: $0 [--local] name email dob level"
    exit 1
fi

# URL of the Cloud Function
LOCAL_URL="http://localhost:5001/gamesetmatch-ef350/us-central1/registerPlayer"
REMOTE_URL="https://us-central1-gamesetmatch-ef350.cloudfunctions.net/registerPlayer"

# Check if the first argument is --local
# And Assign arguments to variables
if [ "$1" == "--local" ]; then
    URL="$LOCAL_URL"
    NAME="$2"
    EMAIL="$3"
    DOB="$4"
    LEVEL="$5"
else
    URL="$REMOTE_URL"
    NAME="$1"
    EMAIL="$2"
    DOB="$3"
    LEVEL="$4"
fi

# Construct and send the curl command
curl -X POST "$URL" \
-H "Content-Type: application/json" \
-d "{\"name\": \"$NAME\", \"email\": \"$EMAIL\", \"DOB\": \"$DOB\", \"level\": \"$LEVEL\"}"
