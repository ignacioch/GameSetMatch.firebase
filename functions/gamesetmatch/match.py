from .score import Score
from .types import MatchFields

from enum import Enum
from typing import Optional


class MatchType(Enum):
    NEW_MATCH_NO_LEAGUE = 1
    UPDATE_MATCH_NO_LEAGUE = 2
    NEW_MATCH_LEAGUE = 3
    UPDATE_MATCH_LEAGUE = 4

class Match:
    def __init__(self, player_a_id, player_b_id, score, match_date, location, match_id=None, league_id=None, group=None):
        self.player_a_id = player_a_id
        self.player_b_id = player_b_id
        self.score = score if isinstance(score, Score) else Score(score)
        self.match_date = match_date
        self.location = location
        self.match_id = match_id
        self.league_id = league_id
        self.group = group

    def to_dict(self):
        return {
            MatchFields.PLAYER_A_ID.value: self.player_a_id,
            MatchFields.PLAYER_B_ID.value: self.player_b_id,
            MatchFields.SCORE.value: self.score.to_dict(),
            MatchFields.MATCH_DATE.value: self.match_date,
            MatchFields.LOCATION.value: self.location,
            MatchFields.MATCH_ID.value: self.match_id,  # This can be None
            MatchFields.LEAGUE_ID.value: self.league_id,  # This can be None
            MatchFields.GROUP.value: self.group,  # This can be None
        }

    def __str__(self):
        return (f"Match(player_a_id={self.player_a_id}, player_b_id={self.player_b_id}, "
                f"score={self.score}, match_date={self.match_date}, "
                f"location={self.location}, match_id={self.match_id}) "
                f"league_id={self.league_id}, group={self.group}")

    def __repr__(self):
        return self.__str__()

    def is_valid_match(self) -> (bool, Optional[str], Optional[int]):
        # The match is valid if it doesn't have an ID but everything else is provided
        # used by _addNonLeagueMatch - that means we have a new match to add
        if self.match_id is None and not all(value for key, value in self.__dict__.items() if (key != "match_id" and key!= "league_id" and key!= "group")):
            return False, "Adding new match requires all match parameters", 400
        # If it's an update a match_id and a score should be provided as a minimum
        elif self.match_id is not None and ("score" not in self.__dict__ or self.score.to_dict() is None or self.score.to_dict() == {}):
            return False, "Updating a match requires score to be provided", 400
        # When we add a match into a league
        elif self.league_id is not None and not all(value for key, value in self.__dict__.items() if key != "match_id"):
            return False, "Adding new match for league requires all match league parameters", 400
        return True, None, None
    

