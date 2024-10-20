#!/bin/bash

# Function to show script usage
show_usage() {
    echo "Usage: $0 --local | --remote --uid <uid> --player_data '<player_json>'"
    echo "  --local            Test against the local Firebase emulator."
    echo "  --remote           Test against the deployed Firebase function."
    echo "  --uid <uid>        Unique identifier for the player."
    echo "  --player_data      JSON data for player to be added."
    exit 1
}

# Check if correct number of arguments is passed
if [ "$#" -lt 5 ]; then
    show_usage
fi

DEPLOYED_ADD_URL="https://us-central1-gamesetmatch-ef350.cloudfunctions.net/addPlayer"
LOCAL_ADD_URL="http://localhost:5001/gamesetmatch-ef350/us-central1/addPlayer"
DEPLOYED_GET_URL="https://us-central1-gamesetmatch-ef350.cloudfunctions.net/getPlayerDetails"
LOCAL_GET_URL="http://localhost:5001/gamesetmatch-ef350/us-central1/getPlayerDetails"

# Initialize variables for the environment, UID, and player data
ADD_URL=""
GET_URL=""
PLAYER_DATA=""

# Process the arguments
case "$1" in
    --local)
        ADD_URL=$LOCAL_ADD_URL
        GET_URL=$LOCAL_GET_URL
        ;;
    --remote)
        ADD_URL=$DEPLOYED_ADD_URL
        GET_URL=$DEPLOYED_GET_URL
        ;;
    *)
        echo "Invalid environment argument."
        show_usage
        ;;
esac

# Extract the UID and player data
case "$2" in
    --uid)
        if [ -z "$3" ]; then
            echo "UID value is missing."
            show_usage
        fi
        UID_VAR="$3"
        ;;
    *)
        echo "Invalid UID argument."
        show_usage
        ;;
esac

case "$4" in
    --player_data)
        if [ -z "$5" ]; then
            echo "Player data value is missing."
            show_usage
        fi
        PLAYER_DATA="$5"
        ;;
    *)
        echo "Invalid player data argument."
        show_usage
        ;;
esac

# Add the player using POST request
add_response=$(curl -s -w "\nHTTP Status: %{http_code}\n" -X POST -H "Content-Type: application/json" -d "{
  \"uid\": \"$UID_VAR\", 
  \"info\": $PLAYER_DATA
}" "$ADD_URL")
add_http_status=$(echo "$add_response" | grep "HTTP Status" | awk '{print $3}')

# Output the add player response
echo "Add Player Response:"
echo "$add_response"

# Check if the player was added successfully
if [ "$add_http_status" -ne 200 ]; then
    echo "Failed to add player."
    exit 1
fi

# Get the player details using GET request
get_response=$(curl -s -w "\nHTTP Status: %{http_code}\n" "$GET_URL?uid=$UID_VAR")
get_http_status=$(echo "$get_response" | grep "HTTP Status" | awk '{print $3}')

# Output the get player response
echo "Get Player Response:"
echo "$get_response"

# Check if the player details were fetched successfully
if [ "$get_http_status" -ne 200 ]; then
    echo "Failed to fetch player details."
    exit 1
fi

# Extract the fetched player data from the response
fetched_player_data=$(echo "$get_response" | jq -c '.info')

# Extract the player info data from the input
input_player_data=$(echo "$PLAYER_DATA" | jq -c '.')

# Compare the added player data with the fetched player data
if [[ "$input_player_data" == "$fetched_player_data" ]]; then
    echo "Player details match. Test successful."
else
    echo "Player details do not match. Test failed."
    exit 1
fi
