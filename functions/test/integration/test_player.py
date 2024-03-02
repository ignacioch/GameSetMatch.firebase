import requests
import pytest
from test import utils

# URLs of the Cloud Functions
REGISTER_PLAYER_URL="http://localhost:5001/gamesetmatch-ef350/us-central1/registerPlayer"


@pytest.mark.integration
@pytest.mark.player
@pytest.mark.parametrize("total_players", [
    # Creating 10 players
    10 
])
def test_add_multiple_players(total_players):
    players = []
    for i in range(0,total_players):
        p = utils.create_dummy_player()
        players.append(p)
        response = requests.post(REGISTER_PLAYER_URL, json=utils.create_register_player_request_object(p))
        assert response.status_code == 200
        # the ID gets overriden by the one automatically created
        # when registering a new player
        assert response.json()["player"]["name"] == players[i].name
        assert response.json()["player"]["email"] == players[i].email
        # amend the stored reference in case it's needed
        players[i].id = response.json()["player"]["id"]


@pytest.mark.integration
@pytest.mark.player
def test_add_duplicate_player():
    players = []
    p = utils.create_dummy_player()
    response = requests.post(REGISTER_PLAYER_URL, json=utils.create_register_player_request_object(p))
    assert response.status_code == 200
    # the ID gets overriden by the one automatically created
    # when registering a new player
    assert response.json()["player"]["name"] == p.name
    assert response.json()["player"]["email"] == p.email
    # amend the stored reference in case it's needed
    p.id = response.json()["player"]["id"]

    response = requests.post(REGISTER_PLAYER_URL, json=utils.create_register_player_request_object(p))
    assert response.status_code == 400

    
    