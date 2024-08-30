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
    match = Match("player1", "player2", score, "2023-03-28", "Court 1", "match123", "league123", "group_1")
    expected_dict = {
        MatchFields.PLAYER_A_ID.value : "player1",
        MatchFields.PLAYER_B_ID.value: "player2",
        MatchFields.SCORE.value: {"set1": {"player_a": 6, "player_b": 4}},
        MatchFields.MATCH_DATE.value: "2023-03-28",
        MatchFields.LOCATION.value: "Court 1",
        MatchFields.MATCH_ID.value: "match123",
        MatchFields.LEAGUE_ID.value: "league123",
        MatchFields.GROUP.value: "group_1"
    }
    assert match.to_dict() == expected_dict
    

@pytest.mark.parametrize("player_a_id,player_b_id,match_date,location,match_id,expected_result, expected_error, expected_code", [
    ("player1", "player2", "2023-03-28", "Court 1", None, True, None, None),
    (None, "player2", "2023-03-28", "Court 1", None, False, "Adding new match requires all match parameters", 400),  # Missing player_a_id
    ("player1", None, "2023-03-28", "Court 1", None, False, "Adding new match requires all match parameters", 400),  # Missing player_b_id
    ("player1", "player2", None, "Court 1", None, False, "Adding new match requires all match parameters", 400),  # Missing match_date
    ("player1", "player2", "2023-03-28", None, None, False, "Adding new match requires all match parameters", 400),  # Missing location
    ("player1", "player2", "2023-03-28", "Court 1", "match123", True, None, None),  # With match_id, still valid
    ("player1", "player2", None, "Court 1", "match123", False, "Updating a match requires score to be provided", 400),  # Missing score when match_id is not none

])
def test_is_valid_match(player_a_id, player_b_id, match_date, location, match_id, expected_result, expected_error, expected_code, valid_score_set1_64):
    score = valid_score_set1_64 if match_date is not None else None  # Use score fixture here
    match = Match(player_a_id, player_b_id, score, match_date, location, match_id)
    valid, error_message, error_code = match.is_valid_match()
    assert valid == expected_result
    assert error_message == expected_error
    assert error_code == expected_code


@pytest.mark.parametrize("player_a_id,player_b_id,match_date,location,match_id,league_id, group, expected_result, expected_error, expected_code", [
    ("player1", "player2", "2023-03-28", "Court 1", None, "league123", "group_1", True, None, None),
    ("player1", "player2", "2023-03-28", "Court 1", None, "league123", None, False, "Adding new match for league requires all match league parameters", 400),  
])
def test_is_valid_league_match(player_a_id, player_b_id, match_date, location, match_id, league_id, group, expected_result, expected_error, expected_code, valid_score_set1_64):
    score = valid_score_set1_64 if match_date is not None else None  # Use score fixture here
    match = Match(player_a_id, player_b_id, score, match_date, location, match_id, league_id, group)
    valid, error_message, error_code = match.is_valid_match()
    assert valid == expected_result
    assert error_message == expected_error
    assert error_code == expected_code