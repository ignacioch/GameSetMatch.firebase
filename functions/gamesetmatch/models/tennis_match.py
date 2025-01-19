from gamesetmatch.models.match import Match

class TennisMatch(Match):
    def __init__(self, match_id: str, opponent: str, score: str, result: str, date: str, surface: str):
        super().__init__(match_id, opponent, score, result, date)
        self.surface = surface