import pytest
from gamesetmatch import api  # Replace with the actual module name

# Test data for parametrization
# Sample league info to be returned on successful addition
sample_league_info = {
    "league_name": "North City League",
    "location": "North City",
    # other fields...
}

test_data = [
    # Format: (input_data, expected_status, expected_message, side_effect)
    ({"player_id": "player1_id", "league_id": "league123"}, 200, {"league_info": sample_league_info}, None),
    ({}, 400, "Player ID and League ID are required", "No Call"),  # Indicates no call to the mocked function
    ({"player_id": "player1_id", "league_id": "league123"}, 400, "Error message", ValueError("Error message")),
]

@pytest.mark.parametrize("input_data, expected_status, expected_response, side_effect", test_data)
def test_add_player_to_league(mocker, input_data, expected_status, expected_response, side_effect):
    # Mock Firestore function
    mock_addPlayerToLeagueFirestore = mocker.patch('gamesetmatch.api.addPlayerToLeagueFirestore', return_value=sample_league_info if not side_effect else None)
    if side_effect:
        mock_addPlayerToLeagueFirestore.side_effect = side_effect

    # Mock request
    mock_request = mocker.Mock()
    mock_request.get_json.return_value = input_data

    # Call the function
    response = api.addPlayerToLeague(mock_request)

    # Assertions
    if side_effect is None:
        mock_addPlayerToLeagueFirestore.assert_called_once_with(input_data["player_id"], input_data["league_id"])
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.get_json() == expected_response
    else:
        assert expected_response in response.get_data(as_text=True)



# Sample league info to be returned on successful creation
sample_league_info_create_league = {
    "league_name": "North City League",
    "location": "North City",
    "running": False,
    "current_round": 0,
    "unallocatedPlayers": [],
    "league_id": "new_league_id"
}

# Test data for parametrization
test_data_create_league = [
    ({"league_name": "North City League", "location": "North City"}, 200, {"league_info": sample_league_info_create_league}, None),
    ({}, 400, "League name and location are required", "No Call"), # Indicates no call to the mocked function
    ({"league_name": "North City League", "location": "North City"}, 400, "Error message", ValueError("Error message")),
]

@pytest.mark.parametrize("input_data, expected_status, expected_response, side_effect", test_data_create_league)
def test_create_league(mocker, input_data, expected_status, expected_response, side_effect):
    # Mock Firestore function
    mock_createLeagueFirestore = mocker.patch('gamesetmatch.api.createLeagueFirestore', return_value=sample_league_info_create_league if not side_effect else None)
    if side_effect:
        mock_createLeagueFirestore.side_effect = side_effect

    # Mock request
    mock_request = mocker.Mock()
    mock_request.get_json.return_value = input_data

    # Call the function
    response = api.createLeague(mock_request)

    # Assertions
    if side_effect is None:
        mock_createLeagueFirestore.assert_called_once_with(input_data["league_name"], input_data["location"])
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.get_json() == expected_response
    else:
        assert expected_response in response.get_data(as_text=True)

