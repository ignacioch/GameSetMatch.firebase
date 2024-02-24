from gamesetmatch.score import Score
import pytest

@pytest.fixture
def valid_score_set1_64():
    return Score({"set1": {"player_a": 6, "player_b": 4}})  # Mock a valid score or adjust according to your Score class implementation

