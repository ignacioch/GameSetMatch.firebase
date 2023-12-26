import requests
import pytest

BASE_URL = "http://localhost:5001/gamesetmatch-ef350/us-central1/addMatch"

def test_add_new_match_without_match_id():
    response = requests.post(
        BASE_URL,
        json={
            "player_a_id": "player1",
            "player_b_id": "player2",
            "score": "6-3, 6-4",
            "date": "2023-03-28",
            "location": "Court 1"
        }
    )
    assert response.status_code == 200

def test_update_existing_match_with_match_id():
    response = requests.post(
        BASE_URL,
        json={
            "match_id": "abcd1234",
            "player_a_id": "player1",
            "player_b_id": "player2",
            "score": "6-4, 6-4",
            "date": "2023-03-28",
            "location": "Court 1"
        }
    )
    assert response.status_code == 200

def test_add_new_match_with_match_id():
    response = requests.post(
        BASE_URL,
        json={
            "match_id": "newMatch123",
            "player_a_id": "player3",
            "player_b_id": "player4",
            "score": "6-2, 6-3",
            "date": "2023-04-01",
            "location": "Court 2"
        }
    )
    assert response.status_code == 200

# Additional test cases as needed...

def test_delete_match():
    # Assuming match_id is known
    match_id = "match1"
    response = requests.post(f"{BASE_URL}/deleteMatch", data={"match_id": match_id})
    assert response.status_code == 200
