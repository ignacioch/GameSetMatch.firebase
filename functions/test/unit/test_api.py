import pytest
from gamesetmatch import api  # Replace with the actual module name
from gamesetmatch import player

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

@pytest.mark.addPlayerTest
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
    if side_effect != "No Call":
        mock_addPlayerToLeagueFirestore.assert_called_once_with(input_data["player_id"], input_data["league_id"])
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.get_json() == expected_response
    else:
        assert expected_response in response.get_data(as_text=True)



# Sample league info to be returned on successful creation
sample_league_info_create_league = {
    "league_name": "North City League",
    "area": "North City",
    "running": False,
    "current_round": 0,
    "unallocatedPlayers": [],
    "league_id": "new_league_id"
}

# Test data for parametrization
test_data_create_league = [
    ({"league_name": "North City League", "area": "North City", "start_date": "2024-02-02", "end_date": "2024-04-02"}, 200, {"league_info": sample_league_info_create_league}, None),
    ({}, 400, "League name and area are required", "No Call"), # Indicates no call to the mocked function
    ({"league_name": "North City League", "area": "North City", "start_date": "2024-02-02", "end_date": "2024-04-02"}, 400, "Error message", ValueError("Error message")),
]

@pytest.mark.createLeagueTest
@pytest.mark.parametrize("input_data, expected_status, expected_response, side_effect", test_data_create_league)
def test_create_league(mocker, input_data, expected_status, expected_response, side_effect):
    # Mock Firestore function
    mock_createLeagueFirestore = mocker.patch('gamesetmatch.api.createLeagueFirestore', return_value=sample_league_info_create_league if not side_effect else None)
    if side_effect and side_effect != "No Call":
        mock_createLeagueFirestore.side_effect = side_effect

    # Mock request
    mock_request = mocker.Mock()
    mock_request.get_json.return_value = input_data

    # Call the function
    response = api.createLeague(mock_request)

    # Assertions
    if side_effect != "No Call":
        mock_createLeagueFirestore.assert_called_once_with(input_data["league_name"], input_data["area"], input_data["start_date"], input_data["end_date"])
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.get_json() == expected_response
    else:
        assert expected_response in response.get_data(as_text=True)



'''
Start Round
'''

# Sample update info to be returned on successful round start
sample_start_round_info = {
    "message": "Round started successfully",
    "league_info": {
        "current_round": 1,
        "running": True,
    }
}

test_data_start_round = [
    # input_data, expected_status, expected_response, side_effect
    ({"league_id": "league123"}, 200, sample_start_round_info, None),
    ({}, 400, "League ID is required", "No Call"),
    ({"league_id": "league123"}, 400, "No unallocated players to start a round", "No Call"),
]

@pytest.mark.startRoundTest
@pytest.mark.parametrize("input_data, expected_status, expected_response, side_effect", test_data_start_round)
def test_start_round(mocker, input_data, expected_status, expected_response, side_effect):
    # Mock the Firestore functions
    mock_fetchPendingPlayersForLeague = mocker.patch('gamesetmatch.api.fetchPendingPlayersForLeague', return_value=[] if side_effect else [player.Player.create_dummy_player( rankingIn=1200, city="London"), player.Player.create_dummy_player( rankingIn=2200, city="London" )])
    mock_startRoundInLeagueFirestore = mocker.patch('gamesetmatch.api.startRoundInLeagueFirestore', return_value=sample_start_round_info["league_info"])

    # Adjust side effect for mock if specified
    if side_effect and side_effect != "No Call":
        mock_startRoundInLeagueFirestore.side_effect = side_effect

    # Mock request
    mock_request = mocker.Mock()
    mock_request.get_json.return_value = input_data

    # Call the function 
    response = api.startRound(mock_request)

    # Assertions
    if side_effect != "No Call":
        mock_startRoundInLeagueFirestore.assert_called_once()
    assert response.status_code == expected_status
    if expected_status == 200:
        assert response.get_json() == expected_response
    else:
        assert expected_response in response.get_data(as_text=True)

