#!/bin/bash

# Validate number of arguments
if [ "$#" -ne 4 ]; then
    echo "Usage: $0 name email dob level"
    exit 1
fi

# Assign arguments to variables
NAME="$1"
EMAIL="$2"
DOB="$3"
LEVEL="$4"

# URL of the Cloud Function
URL="http://localhost:5001/gamesetmatch-ef350/us-central1/registerPlayer"

# Construct and send the curl command
curl -X POST "$URL" \
-H "Content-Type: application/json" \
-d "{\"name\": \"$NAME\", \"email\": \"$EMAIL\", \"DOB\": \"$DOB\", \"level\": \"$LEVEL\"}"
