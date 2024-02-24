# test_match.py
import pytest
from gamesetmatch.match import Match
from gamesetmatch.score import Score
from gamesetmatch.types import MatchFields

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
        MatchFields.PLAYER_A_ID.value : "player1",
        MatchFields.PLAYER_B_ID.value: "player2",
        MatchFields.SCORE.value: {"set1": {"player_a": 6, "player_b": 4}},
        MatchFields.MATCH_DATE.value: "2023-03-28",
        MatchFields.LOCATION.value: "Court 1",
        MatchFields.MATCH_ID.value: "match123"
    }
    assert match.to_dict() == expected_dict

# Additional tests can be added for more scenarios and edge cases
