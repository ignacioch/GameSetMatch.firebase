#!/bin/bash

# URLs of the Cloud Functions
LOCAL_BASE_URL="http://localhost:5001/gamesetmatch-ef350/us-central1/"
REMOTE_BASE_URL="https://us-central1-gamesetmatch-ef350.cloudfunctions.net/"

# Check if the first argument is --local
if [ "$1" == "--local" ]; then
    URL="$LOCAL_BASE_URL"
else
    URL="$REMOTE_BASE_URL"
fi

# Concatenate the base URL with the specific endpoints
REGISTER_PLAYER_URL="${LOCAL_BASE_URL}registerPlayer"
ADD_MATCH_URL="${LOCAL_BASE_URL}addMatch"
GET_MATCH_DETAILS_URL="${LOCAL_BASE_URL}getMatchDetails"
DELETE_PLAYER_URL="${LOCAL_BASE_URL}deletePlayer"
DELETE_MATCH_URL="${LOCAL_BASE_URL}deleteMatch"

# Function to check response status
check_status() {
    if [ "$1" != "200" ]; then
        echo "Error: Request failed with status $1"
        exit 1
    fi
}

# Register two players
response=$(curl -s -w "%{http_code}" -o response.json -X POST "$REGISTER_PLAYER_URL" -H "Content-Type: application/json" -d '{"name": "John Doe", "email": "john@example.com", "DOB": "1990-01-01", "level": "beginner"}')
echo "Response from registering Player 1: $(cat response.json)"
check_status "$response"
player1_id=$(jq -r '.player.id' response.json)
echo "Player 1 Registered with ID: $player1_id"

response=$(curl -s -w "%{http_code}" -o response.json -X POST "$REGISTER_PLAYER_URL" -H "Content-Type: application/json" -d '{"name": "Jane Doe", "email": "jane@example.com", "DOB": "1992-02-02", "level": "intermediate"}')
echo "Response from registering Player 2: $(cat response.json)"
check_status "$response"
player2_id=$(jq -r '.player.id' response.json)
echo "Player 1 Registered with ID: $player2_id"

# Add a match between them
response=$(curl -s -w "%{http_code}" -o response.json -X POST "$ADD_MATCH_URL" -H "Content-Type: application/json" -d "{\"player_a_id\": \"$player1_id\", \"player_b_id\": \"$player2_id\", \"score\": \"6-3, 6-4\", \"date\": \"2023-03-28\", \"location\": \"Court 1\"}")
echo "Response from adding Match: $(cat response.json)"
check_status "$response"
match_id=$(jq -r '.match.match_id' response.json)
echo "Match added with ID: $match_id"

# Get match details
response=$(curl -s -w "%{http_code}" -o response.json -X POST "$GET_MATCH_DETAILS_URL" -H "Content-Type: application/json" -d "{\"match_id\": \"$match_id\"}")
echo "Response from getMatchDetails: $(cat response.json)"
check_status "$response"
match_details=$(cat response.json)
echo "Match Details: $match_details"

# Delete the players
response=$(curl -s -w "%{http_code}" -o response.json -H "Content-Type: application/json" -X POST "$DELETE_PLAYER_URL" -d "{\"player_id\": \"$player1_id\"}")
echo "Response from deletePlayer1: $(cat response.json)"
check_status "$response"
echo "Player 1 Deleted"

# Delete the players
response=$(curl -s -w "%{http_code}" -o response.json -H "Content-Type: application/json" -X POST "$DELETE_PLAYER_URL" -d "{\"player_id\": \"$player2_id\"}")
echo "Response from deletePlayer2: $(cat response.json)"
check_status "$response"
echo "Player 2 Deleted"

# Delete the match
response=$(curl -s -w "%{http_code}" -o response.json -H "Content-Type: application/json" -X POST "$DELETE_MATCH_URL" -d "{\"match_id\": \"$match_id\"}")
echo "Response from deleteMatch: $(cat response.json)"
check_status "$response"
echo "Match Deleted"

# Clean up
rm response.json
