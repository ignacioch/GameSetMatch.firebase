# test_match.py
import pytest
from gamesetmatch.match import Match
from gamesetmatch.score import Score

def test_initialization_with_score():
    score = Score({"set1": {"player_a": 6, "player_b": 4}})
    match = Match("player1", "player2", score, "2023-03-28", "Court 1", "match123")
    assert match.player_a_id == "player1"
    assert match.player_b_id == "player2"
    assert match.score.to_dict() == {"set1": {"player_a": 6, "player_b": 4}}
    assert match.match_date == "2023-03-28"
    assert match.location == "Court 1"
    assert match.match_id == "match123"

def test_to_dict_method():
    score = Score({"set1": {"player_a": 6, "player_b": 4}})
    match = Match("player1", "player2", score, "2023-03-28", "Court 1", "match123")
    expected_dict = {
        "player_a_id": "player1",
        "player_b_id": "player2",
        "score": {"set1": {"player_a": 6, "player_b": 4}},
        "match_date": "2023-03-28",
        "location": "Court 1",
        "match_id": "match123"
    }
    assert match.to_dict() == expected_dict

# Additional tests can be added for more scenarios and edge cases
