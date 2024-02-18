# test_player.py
import pytest
from gamesetmatch.player import Player

# Sample data for testing
players_info = [
    {"id": "player1", "ranking": 1200},
    {"id": "player2", "ranking": 1500},
    {"id": "player3", "ranking": 900},
    {"id": "player4", "ranking": 1800},
    {"id": "player5", "ranking": 1100},
    {"id": "player6", "ranking": 1300},
    {"id": "player7", "ranking": 1000},
    {"id": "player8", "ranking": 1600},
    {"id": "player9", "ranking": 1400},
]

players_info_4 = [
    {"id": "player1", "ranking": 1200},
    {"id": "player2", "ranking": 1500},
    {"id": "player3", "ranking": 900},
    {"id": "player4", "ranking": 1800},
]

players_info_13 = [
    {"id": "player1", "ranking": 1200},
    {"id": "player2", "ranking": 1500},
    {"id": "player3", "ranking": 900},
    {"id": "player4", "ranking": 1800},
    {"id": "player5", "ranking": 1100},
    {"id": "player6", "ranking": 1300},
    {"id": "player7", "ranking": 1000},
    {"id": "player8", "ranking": 1600},
    {"id": "player9", "ranking": 1400},
    {"id": "player10", "ranking": 950},
    {"id": "player11", "ranking": 1250},
    {"id": "player12", "ranking": 1150},
    {"id": "player13", "ranking": 1350},
]

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


@pytest.mark.parametrize("player_count, expected_distribution", [
    (4, [4]),  # 4 players -> 1 group of 4
    (9, [5, 4]),  # 9 players -> 1 group of 5, 1 group of 4
    (13, [7, 6]),  # 13 players -> 1 group of 7, 1 group of 6
    (28, [6, 6, 6, 5, 5]),  # 28 players -> 3 groups of 6, 2 groups of 5
])
def test_distribute_players(player_count, expected_distribution):
    result = Player.distribute_players(player_count)
    assert result == expected_distribution, f"Expected distribution for {player_count} players is {expected_distribution}, got {result} instead."