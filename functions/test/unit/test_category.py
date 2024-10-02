from gamesetmatch.models.match import Match
from gamesetmatch.models.category import Category
from gamesetmatch.models.league import League

def test_category_from_dict():
    category_data = {
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
    }

    category = Category.from_dict(category_data)
    
    assert "match1" in category.matches
    assert category.matches["match1"].opponent == "Opponent A"

def test_category_to_dict():
    match = Match("match1", "Opponent A", "6-3, 6-4", "win", "2024-01-01", "clay")
    league = League("league1", "Tennis League A")
    category = Category(matches={"match1": match}, leagues=[league])
    
    category_dict = category.to_dict()
    
    assert category_dict["matches"]["match1"]["opponent"] == "Opponent A"
    assert category_dict["leagues"][0]["name"] == "Tennis League A"

def test_category_str_repr():
    match = Match("match1", "Opponent A", "6-3, 6-4", "win", "2024-01-01", "clay")
    league = League("league1", "Tennis League A")
    category = Category(matches={"match1": match}, leagues=[league])
    
    assert str(category) == f"Category(matches=[match1: {str(match)}], leagues=[{str(league)}])"
    assert repr(category) == f"Category(matches=[match1: {repr(match)}], leagues=[{repr(league)}])"
