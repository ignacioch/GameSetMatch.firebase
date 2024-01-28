from .score import Score

class Match:
    def __init__(self, player_a_id, player_b_id, score, match_date, location, match_id=None):
        self.player_a_id = player_a_id
        self.player_b_id = player_b_id
        self.score = score if isinstance(score, Score) else Score(score)
        self.match_date = match_date
        self.location = location
        self.match_id = match_id

    def to_dict(self):
        return {
            "player_a_id": self.player_a_id,
            "player_b_id": self.player_b_id,
            "score": self.score.to_dict(),
            "match_date": self.match_date,
            "location": self.location,
            "match_id": self.match_id  # This can be None
        }

    def __str__(self):
        return (f"Match(player_a_id={self.player_a_id}, player_b_id={self.player_b_id}, "
                f"score={self.score}, match_date={self.match_date}, "
                f"location={self.location}, match_id={self.match_id})")

    def __repr__(self):
        return self.__str__()
