#!/bin/bash

# Example run
# --------------
# ./addAndVerifyPlayer.sh --local --uid "1234" --player_data '{"name": "John Doe", "email": "john.doe@example.com", "profile_picture_url": "http://example.com/johndoe.jpg", "date_of_birth": "1990-01-01", "tel_number":"+123-456-789", "areas":[10,20], "level": "beginner"}' --user_data '{"uid": "1234", "displayName": "John Doe", "photoUrl": "http://example.com/photo.jpg", "email": "john.doe@example.com"}'
# ---------------

# Function to show script usage
# Function to show script usage
show_usage() {
    echo "Usage: $0 --local | --remote --uid <uid> --player_data '<player_json>' --user_data '<user_json>'"
    echo "  --local            Test against the local Firebase emulator."
    echo "  --remote           Test against the deployed Firebase function."
    echo "  --uid <uid>        Unique identifier for the player."
    echo "  --player_data      JSON data for player to be added."
    echo "  --user_data        JSON data for user to be added."
    exit 1
}

# Check if correct number of arguments is passed
if [ "$#" -lt 7 ]; then
    show_usage
fi

LOCAL_BASE_URL="http://localhost:5001/gamesetmatch-ef350/us-central1"
DEPLOYED_BASE_URL="https://us-central1-gamesetmatch-ef350.cloudfunctions.net"

# Initialize variables for the environment, UID, player data, and user data
BASE_URL=""
PLAYER_DATA=""
USER_DATA=""

# Process the arguments
case "$1" in
    --local)
        BASE_URL=$LOCAL_BASE_URL
        ;;
    --remote)
        BASE_URL=$DEPLOYED_BASE_URL
        ;;
    *)
        echo "Invalid environment argument."
        show_usage
        ;;
esac

# Extract the UID, player data, and user data
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

case "$6" in
    --user_data)
        if [ -z "$7" ]; then
            echo "User data value is missing."
            show_usage
        fi
        USER_DATA="$7"
        ;;
    *)
        echo "Invalid user data argument."
        show_usage
        ;;
esac

# Add the user using POST request
user_response=$(curl -s -w "\nHTTP Status: %{http_code}\n" -X POST -H "Content-Type: application/json" -d "$USER_DATA" "$BASE_URL/addUser")
user_http_status=$(echo "$user_response" | grep "HTTP Status" | awk '{print $3}')

# Output the add user response
echo "Add User Response:"
echo "$user_response"

# Check if the user was added successfully
if [ "$user_http_status" -ne 200 ]; then
    echo "Failed to add user."
    exit 1
fi

# Add the player using POST request
add_response=$(curl -s -w "\nHTTP Status: %{http_code}\n" -X POST -H "Content-Type: application/json" -d "{
  \"uid\": \"$UID_VAR\", 
  \"info\": $PLAYER_DATA
}" "$BASE_URL/addPlayer")
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
get_response=$(curl -s -w "\nHTTP Status: %{http_code}\n" "$BASE_URL/getPlayerDetails?uid=$UID_VAR")
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
# If fetched_player_data is empty, print an error and exit
if [ -z "$fetched_player_data" ]; then
    echo "Error: 'info' field is empty in the response." >&2
    exit 1
fi

# Extract the player info data from the input
input_player_data=$(echo "$PLAYER_DATA" | jq -c '.')

# Debugging output to compare fetched and input data
echo "Fetched Player Data: $fetched_player_data"
echo "Input Player Data: $input_player_data"

# Compare the added player data with the fetched player data
if [[ "$input_player_data" == "$fetched_player_data" ]]; then
    echo "Player details match. Test successful."
else
    echo "Player details do not match. Test failed."
    exit 1
fi