#!/bin/bash

# Set the deployed URL (replace with your actual Firebase function URL)
DEPLOYED_URL="https://us-central1-gamesetmatch-ef350.cloudfunctions.net/getPlayerDetails"

# Set the local emulator URL (default port 5001, adjust if necessary)
LOCAL_URL="http://localhost:5001/gamesetmatch-ef350/us-central1/getPlayerDetails"

# Function to show script usage
show_usage() {
    echo "Usage: $0 --local | --remote <player_id>"
    echo "  --local    Test against the local Firebase emulator."
    echo "  --remote   Test against the deployed Firebase function."
    echo "  <player_id> The ID of the player to fetch."
    exit 1
}

# Check if the correct number of arguments is passed
if [ "$#" -ne 2 ]; then
    show_usage
fi

# Get the player ID from the second argument
PLAYER_ID="$2"

# Determine the environment based on the argument
case "$1" in
    --local)
        URL=$LOCAL_URL
        echo "Testing on the local emulator..."
        ;;
    --remote)
        URL=$DEPLOYED_URL
        echo "Testing on the deployed Firebase function..."
        ;;
    *)
        echo "Invalid argument."
        show_usage
        ;;
esac

# Make the GET request and store the response
response=$(curl -s -w "\nHTTP Status: %{http_code}\n" "$URL?player_id=$PLAYER_ID")

# Output the response
echo "$response"
