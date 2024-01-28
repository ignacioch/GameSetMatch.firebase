# test_score.py
import pytest
from gamesetmatch.score import Score

def test_initialization():
    score = Score()
    assert score.to_dict() == {}

def test_add_first_set_score():
    score = Score()
    score.add_first_set_score(6, 4)
    assert score.to_dict() == {"set1": {"player_a": 6, "player_b": 4}}

def test_add_all_set_scores():
    score = Score()
    score.add_first_set_score(6, 4)
    score.add_second_set_score(4, 6)
    score.add_third_set_score(7, 5)
    score.add_fourth_set_score(5, 7)
    score.add_fifth_set_score(6, 3)
    expected_scores = {
        "set1": {"player_a": 6, "player_b": 4},
        "set2": {"player_a": 4, "player_b": 6},
        "set3": {"player_a": 7, "player_b": 5},
        "set4": {"player_a": 5, "player_b": 7},
        "set5": {"player_a": 6, "player_b": 3}
    }
    assert score.to_dict() == expected_scores