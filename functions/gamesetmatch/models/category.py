from gamesetmatch.models.match import Match
from gamesetmatch.models.league import League

class Category:
    def __init__(self, matches: dict[str, 'Match'], leagues: list['League']):
        self.matches = matches  # Dictionary with match ID as key, Match object as value
        self.leagues = leagues

    @classmethod
    def from_dict(cls, category_data: dict) -> 'Category':
        matches = {match_id: Match.from_dict(match_data) for match_id, match_data in category_data["matches"].items()}
        leagues = [League.from_dict(league) for league in category_data["leagues"]]
        return cls(matches=matches, leagues=leagues)

    def to_dict(self) -> dict:
        return {
            "matches": {match_id: match.to_dict() for match_id, match in self.matches.items()},
            "leagues": [league.to_dict() for league in self.leagues]
        }

    def __str__(self):
        matches_str = ', '.join([f"{match_id}: {str(match)}" for match_id, match in self.matches.items()])
        leagues_str = ', '.join([str(league) for league in self.leagues])
        return f"Category(matches=[{matches_str}], leagues=[{leagues_str}])"

    def __repr__(self):
        matches_repr = ', '.join([f"{match_id}: {repr(match)}" for match_id, match in self.matches.items()])
        leagues_repr = ', '.join([repr(league) for league in self.leagues])
        return f"Category(matches=[{matches_repr}], leagues=[{leagues_repr}])"
