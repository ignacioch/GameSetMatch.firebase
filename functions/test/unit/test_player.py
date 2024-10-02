import pytest
from gamesetmatch.models.player import Player
from gamesetmatch.models.player_info import PlayerInfo
from gamesetmatch.models.sport import Sport
from gamesetmatch.models.category import Category
from gamesetmatch.models.match import Match
from gamesetmatch.models.league import League

@pytest.fixture
def mock_player_data():
    return {
        "info": {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "profile_picture_url": "http://example.com/johndoe.jpg",
            "date_of_birth": "1990-01-01"
        },
        "sports": {
            "tennis": {
                "sport_name": "tennis",
                "singles": {
                    "matches": {
                        "match1": {
                            "match_id": "match1",
                            "opponent": "Opponent A",
                            "score": "6-3, 6-4",
                            "result": "win",
                            "date": "2024-01-01",
                            "surface": "clay"
                        }
                    },
                    "leagues": [
                        {"league_id": "league1", "name": "Tennis League A"}
                    ]
                },
                "doubles": {
                    "matches": {},
                    "leagues": []
                }
            }
        }
    }

def test_player_from_dict(mock_player_data):
    player_id = "1234"
    
    # Create Player object using from_dict
    player = Player.from_dict(player_id, mock_player_data)
    
    assert player.player_id == player_id
    assert player.info.name == "John Doe"
    assert player.info.email == "john.doe@example.com"
    assert player.sports["tennis"].sport_name == "tennis"

    # Check matches and leagues
    assert len(player.sports["tennis"].singles.matches) == 1
    assert player.sports["tennis"].singles.matches["match1"].match_id == "match1"

def test_player_to_dict(mock_player_data):
    player_id = "1234"
    player = Player.from_dict(player_id, mock_player_data)
    
    player_dict = player.to_dict()
    
    assert player_dict["player_id"] == player_id
    assert player_dict["info"]["name"] == "John Doe"
    assert player_dict["sports"]["tennis"]["sport_name"] == "tennis"

    # Check matches and leagues
    assert player_dict["sports"]["tennis"]["singles"]["matches"]["match1"]["match_id"] == "match1"

def test_player_str_repr(mock_player_data):
    player_id = "1234"
    player = Player.from_dict(player_id, mock_player_data)
    
    # String and repr assertions
    assert str(player) == f"Player(player_id=1234, info={player.info}, sports=[tennis: {str(player.sports['tennis'])}])"
    assert repr(player) == f"Player(player_id=1234, info={repr(player.info)}, sports=[tennis: {repr(player.sports['tennis'])}])"
