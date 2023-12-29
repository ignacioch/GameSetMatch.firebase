import requests
import pytest

# URLs of the Cloud Functions
REGISTER_PLAYER_URL="http://localhost:5001/gamesetmatch-ef350/us-central1/registerPlayer"
ADD_MATCH_URL="http://localhost:5001/gamesetmatch-ef350/us-central1/addMatch"
GET_MATCH_DETAILS_URL="http://localhost:5001/gamesetmatch-ef350/us-central1/getMatchDetails"
DELETE_PLAYER_URL="http://localhost:5001/gamesetmatch-ef350/us-central1/deletePlayer"
DELETE_MATCH_URL="http://localhost:5001/gamesetmatch-ef350/us-central1/deleteMatch"

def test_end_to_end_workflow():
    # Register Player 1
    player1_data = {"name": "John Doe", "email": "john@example.com", "DOB": "1990-01-01", "level": "beginner"}
    response = requests.post(REGISTER_PLAYER_URL, json=player1_data)
    assert response.status_code == 200
    player1_id = response.json()["player"]["id"]

    # Register Player 2
    player2_data = {"name": "Jane Doe", "email": "jane@example.com", "DOB": "1992-02-02", "level": "intermediate"}
    response = requests.post(REGISTER_PLAYER_URL, json=player2_data)
    assert response.status_code == 200
    player2_id = response.json()["player"]["id"]

    # Add a Match
    match_data = {
        "player_a_id": player1_id, 
        "player_b_id": player2_id, 
        "score": "6-3, 6-4", 
        "date": "2023-03-28", 
        "location": "Court 1"
    }
    response = requests.post(ADD_MATCH_URL, json=match_data)
    assert response.status_code == 200
    match_id = response.json()["match"]["match_id"]

    # Delete Player 1
    response = requests.post(DELETE_PLAYER_URL, json={"player_id": player1_id})
    assert response.status_code == 200

    # Delete Player 2
    response = requests.post(DELETE_PLAYER_URL, json={"player_id": player2_id})
    assert response.status_code == 200

    # Delete the Match
    response = requests.post(DELETE_MATCH_URL, json={"match_id": match_id})
    assert response.status_code == 200

# Run the test
if __name__ == "__main__":
    pytest.main()
