import pytest
from unittest.mock import Mock
from gamesetmatch.api import getPlayerDetails
from gamesetmatch.models.player import Player,PlayerInfo


# Parametrized Test Case
@pytest.mark.parametrize(
    "player_id, uid, mock_player_data, expected_result, expected_exception",
    [
        # Test 1 : player is found
        (
            '1234',  
            None,
            {
                "player_id": "1234",
                "info": {
                    "name": "John Doe",
                    "email": "john.doe@example.com",
                    "profile_picture_url": "http://example.com/johndoe.jpg",
                    "date_of_birth": "1990-01-01T00:00:00Z"
                },
                "sports" : {}
            },
            {
                "player_id": "1234",
                "info": {
                    "name": "John Doe",
                    "email": "john.doe@example.com",
                    "profile_picture_url": "http://example.com/johndoe.jpg",
                    "date_of_birth": "1990-01-01T00:00:00Z"
                },
                "sports" : {}
            },
            None #No Exception
        ),
        # Test 2 : plaer is not found
        (
            '9999',  # Case where player is not found (return None)
            None,
            None,
            None,
            None #No Exception
        ),
        # Test 3 : uid not found
        (
            None,  
            'uid123', 
            None,
            None,
            None #No Exception
        ),
        # Test 4: both Missing
        (
            None,  
            None,
            None,
            None,
            ValueError
        ),
    ]
)
def test_get_player_details(mock_get_player_document, mock_get_player_by_uid, player_id, uid, mock_player_data, expected_result, expected_exception):
    # Create a mock Player object if mock_player_data is provided
    if mock_player_data:
        mock_player_info = PlayerInfo(**mock_player_data['info'])
        mock_player = Player(player_id=mock_player_data['player_id'], info=mock_player_info)
    else:
        mock_player = None

    # Set up the mocks based on whether player_id or uid is provided
    if player_id:
        mock_get_player_document.return_value = mock_player
    elif uid:
        mock_get_player_by_uid.return_value = mock_player
    
    # Check if we expect an exception
    if expected_exception:
        with pytest.raises(expected_exception):
            getPlayerDetails(player_id=player_id, uid=uid)
    else:
        result = getPlayerDetails(player_id=player_id, uid=uid)
        # Assert the result matches the expected result
        assert result == expected_result