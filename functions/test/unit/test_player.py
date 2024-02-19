# test_player.py
import pytest
from gamesetmatch.player import Player

# Sample data for testing
players_info = [
    Player.create_dummy_player(id="player1", rankingIn=1200, city="London"),
    Player.create_dummy_player(id="player2", rankingIn=1500, city="London"),
    Player.create_dummy_player(id="player3", rankingIn=900, city="London"),
    Player.create_dummy_player(id="player4", rankingIn=1800, city="London"),
    Player.create_dummy_player(id="player5", rankingIn=1100, city="London"),
    Player.create_dummy_player(id="player6", rankingIn=1300, city="London"),
    Player.create_dummy_player(id="player7", rankingIn=1000, city="London"),
    Player.create_dummy_player(id="player8", rankingIn=1600, city="London"),
    Player.create_dummy_player(id="player9", rankingIn=1400, city="London")
]

players_info_4 = [
    Player.create_dummy_player(id="player1", rankingIn=1200, city="London"),
    Player.create_dummy_player(id="player2", rankingIn=1500, city="London"),
    Player.create_dummy_player(id="player3", rankingIn=900, city="London"),
    Player.create_dummy_player(id="player4", rankingIn=1800, city="London")
]

players_info_13 = [
    Player.create_dummy_player(id="player1", rankingIn=1200, city="London"),
    Player.create_dummy_player(id="player2", rankingIn=1500, city="London"),
    Player.create_dummy_player(id="player3", rankingIn=900, city="London"),
    Player.create_dummy_player(id="player4", rankingIn=1800, city="London"),
    Player.create_dummy_player(id="player5", rankingIn=1100, city="London"),
    Player.create_dummy_player(id="player6", rankingIn=1300, city="London"),
    Player.create_dummy_player(id="player7", rankingIn=1000, city="London"),
    Player.create_dummy_player(id="player8", rankingIn=1600, city="London"),
    Player.create_dummy_player(id="player9", rankingIn=1400, city="London"),
    Player.create_dummy_player(id="player10", rankingIn=950, city="London"),
    Player.create_dummy_player(id="player11", rankingIn=1250, city="London"),
    Player.create_dummy_player(id="player12", rankingIn=1150, city="London"),
    Player.create_dummy_player(id="player13", rankingIn=1350, city="London")
]

@pytest.mark.player
@pytest.mark.parametrize("players_info, expected_groups", [
    # Test case with 4 players, expecting 1 group
    (players_info_4, {
        "group_1": ["player4", "player2", "player1", "player3"],
    }),
    # Test case with 9 players from previous example, expecting 2 groups
    (players_info, {
        "group_1": ["player4", "player8", "player2", "player9", "player6"],
        "group_2": ["player1", "player5", "player7", "player3"],
    }),
    ## Test case with 13 players, expecting 2 groups (7 + 6)
    (players_info_13, {
        "group_1": ["player4", "player8", "player2", "player9", "player13", "player6", "player11"],
        "group_2": ["player1", "player12", "player5", "player7", "player10", "player3"],
    }),
])
def test_sort_and_group_players(players_info, expected_groups):
    sorted_groups = Player.sort_and_group_players(players_info)
    assert sorted_groups == expected_groups

@pytest.mark.player
@pytest.mark.parametrize("player_count, expected_distribution", [
    (4, [4]),  # 4 players -> 1 group of 4
    (9, [5, 4]),  # 9 players -> 1 group of 5, 1 group of 4
    (13, [7, 6]),  # 13 players -> 1 group of 7, 1 group of 6
    (28, [6, 6, 6, 5, 5]),  # 28 players -> 3 groups of 6, 2 groups of 5
])
def test_distribute_players(player_count, expected_distribution):
    result = Player.distribute_players(player_count)
    assert result == expected_distribution, f"Expected distribution for {player_count} players is {expected_distribution}, got {result} instead."