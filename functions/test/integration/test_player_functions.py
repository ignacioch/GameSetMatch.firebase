import requests
import pytest

BASE_URL = "http://localhost:5001/gamesetmatch-ef350/us-central1/"
REQUEST_GET_PLAYERS = BASE_URL + "getPlayerDetails"
REQUEST_REGISTER_PLAYER = BASE_URL + "registerPlayer"

def test_add_and_get_player():
    # Add a new player
    add_player_response = requests.post(
        REQUEST_REGISTER_PLAYER,
        json={
            "name": "Jane Doe",
            "email": "janedoe@example.com",
            "DOB": "1992-02-02",
            "level": "intermediate"
        }
    )
    assert add_player_response.status_code == 200

    # Get player details by email
    get_player_response = requests.post(
        REQUEST_GET_PLAYERS,
        json={
            "email": "janedoe@example.com"
        }
    )
    assert get_player_response.status_code == 200
    player_details = get_player_response.json()
    assert player_details["email"] == "janedoe@example.com"
    assert player_details["name"] == "Jane Doe"

