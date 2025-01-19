class League:
    def __init__(self, league_id: str, name: str):
        self.league_id = league_id
        self.name = name

    @classmethod
    def from_dict(cls, league_data: dict) -> 'League':
        return cls(
            league_id=league_data["league_id"],
            name=league_data["name"]
        )

    def to_dict(self) -> dict:
        return {
            "league_id": self.league_id,
            "name": self.name
        }

    def __str__(self):
        return f"League(league_id={self.league_id}, name={self.name})"

    def __repr__(self):
        return f"League(league_id={self.league_id}, name={self.name})"
