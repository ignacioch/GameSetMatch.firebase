#!/bin/bash

# Function to show script usage
show_usage() {
    echo "Usage: $0 --local | --remote --uid <uid>"
    echo "  --local            Test against the local Firebase emulator."
    echo "  --remote           Test against the deployed Firebase function."
    echo "  --player_id <id>   Pass the player_id to search by."
    echo "  --uid <uid>        Pass the uid to search by."
    exit 1
}

# Check if correct number of arguments is passed
if [ "$#" -lt 3 ]; then
    show_usage
fi

DEPLOYED_URL="https://us-central1-gamesetmatch-ef350.cloudfunctions.net/getPlayerDetails"
LOCAL_URL="http://localhost:5001/gamesetmatch-ef350/us-central1/getPlayerDetails"

# Initialize variables for the environment and query parameters
URL=""
QUERY_PARAM=""

# Process the arguments
case "$1" in
    --local)
        URL=$LOCAL_URL
        ;;
    --remote)
        URL=$DEPLOYED_URL
        ;;
    *)
        echo "Invalid environment argument."
        show_usage
        ;;
esac

# Check for either --player_id or --uid
case "$2" in
    --uid)
        if [ -z "$3" ]; then
            echo "uid value is missing."
            show_usage
        fi
        QUERY_PARAM="uid=$3"
        ;;
    *)
        echo "Invalid search parameter."
        show_usage
        ;;
esac

echo "$URL"
# Make the GET request and store the response
response=$(curl -s -w "\nHTTP Status: %{http_code}\n" "$URL?$QUERY_PARAM")

# Output the response
echo "$response"
