import pytest
from gamesetmatch.models.sport import Sport
from gamesetmatch.models.category import Category
from gamesetmatch.models.match import Match
from gamesetmatch.models.league import League

def test_sport_from_dict():
    sport_data = {
        "sport_name": "tennis",
        "singles": {
            "matches": {
                "match1": {
                    "match_id": "match1",
                    "opponent": "Opponent A",
                    "score": "6-3, 6-4",
                    "result": "win",
                    "date": "2024-01-01",
                    "surface": "clay"
                }
            },
            "leagues": [
                {"league_id": "league1", "name": "Tennis League A"}
            ]
        },
        "doubles": {
            "matches": {},
            "leagues": []
        }
    }

    sport = Sport.from_dict(sport_data)
    
    assert sport.sport_name == "tennis"
    assert "match1" in sport.singles.matches

def test_sport_to_dict():
    match = Match("match1", "Opponent A", "6-3, 6-4", "win", "2024-01-01", "clay")
    league = League("league1", "Tennis League A")
    singles = Category(matches={"match1": match}, leagues=[league])
    doubles = Category(matches={}, leagues=[])
    sport = Sport(sport="tennis", singles=singles, doubles=doubles)
    
    sport_dict = sport.to_dict()
    
    assert sport_dict["sport_name"] == "tennis"
    assert sport_dict["singles"]["matches"]["match1"]["opponent"] == "Opponent A"

def test_sport_str_repr():
    match = Match("match1", "Opponent A", "6-3, 6-4", "win", "2024-01-01", "clay")
    league = League("league1", "Tennis League A")
    singles = Category(matches={"match1": match}, leagues=[league])
    doubles = Category(matches={}, leagues=[])
    sport = Sport(sport="tennis", singles=singles, doubles=doubles)
    
    assert str(sport) == f"Sport(tennis: singles={str(singles)}, doubles={str(doubles)})"
    assert repr(sport) == f"Sport(tennis: singles={repr(singles)}, doubles={repr(doubles)})"