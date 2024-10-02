class Match:
    def __init__(self, match_id: str, opponent: str, score: str, result: str, date: str, surface: str = "unknown"):
        self.match_id = match_id
        self.opponent = opponent
        self.score = score
        self.result = result
        self.date = date
        self.surface = surface

    @classmethod
    def from_dict(cls, match_data: dict) -> 'Match':
        return cls(
            match_id=match_data["match_id"],
            opponent=match_data["opponent"],
            score=match_data["score"],
            result=match_data["result"],
            date=match_data["date"],
            surface=match_data.get("surface", "unknown")
        )

    def to_dict(self) -> dict:
        return {
            "match_id": self.match_id,
            "opponent": self.opponent,
            "score": self.score,
            "result": self.result,
            "date": self.date,
            "surface": self.surface
        }

    def __str__(self):
        return f"Match(match_id={self.match_id}, opponent={self.opponent}, score={self.score}, result={self.result}, date={self.date}, surface={self.surface})"

    def __repr__(self):
        return f"Match(match_id={self.match_id}, opponent={self.opponent}, score={self.score}, result={self.result}, date={self.date}, surface={self.surface})"
