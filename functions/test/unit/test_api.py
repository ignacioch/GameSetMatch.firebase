import pytest
from unittest.mock import MagicMock
from gamesetmatch.api import getPlayerDetails

# Test case when player is found by player_id
def test_get_player_by_id(mock_get_player_document,test_player):
    player_id = '1234'
    player = getPlayerDetails(player_id=player_id, uid=None)  # Assume uid is None if searching by player_id
    assert player == test_player.to_dict()

# Test case when player is not found
def test_player_not_found(mock_get_player_document):
    # Mock Firestore to return None (player not found)
    mock_get_player_document.return_value = None

    player_id = '9999'  # Non-existent player_id
    result = getPlayerDetails(player_id=player_id, uid=None)

    # Check result is None, indicating no player found
    assert result is None


# Test case when searching by uid
def test_get_player_by_uid(mock_get_player_by_uid):
    # Mock Firestore response
    mock_get_player_by_uid.return_value = mock_player_data

    # Call the function with uid instead of player_id
    uid = 'abcd-1234'
    result = getPlayerDetails(player_id=None, uid=uid)  # Assume player_id is None if searching by uid

    # Check result is the mocked player data
    assert result == mock_player_data


# Test case when neither player_id nor uid is provided
def test_missing_player_id_and_uid():
    # Call the function with no player_id or uid
    result = getPlayerDetails(player_id=None, uid=None)

    # Check result is None (or you could raise an exception or return an error dict)
    assert result is None  # Or assert specific behavior if you're raising an error
