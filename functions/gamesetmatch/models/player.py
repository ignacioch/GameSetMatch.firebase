from gamesetmatch.models.player_info import PlayerInfo

class Player:
    def __init__(self, player_id: str, info: PlayerInfo):
        self.player_id = player_id
        self.info = info
        # starting with empty leagues and tennis_matches
        self.tennis_matches = []
        self.leagues = []
    
    @classmethod
    def from_dict(cls, player_id: str, player_data: dict) -> 'Player':
        """
        Class method to create a Player object from a Firestore dictionary.
        Used mainly for testing.
        """
        # Create PlayerInfo object
        info = PlayerInfo(
            name=player_data["info"]["name"],
            email=player_data["info"]["email"],
            profile_picture_url=player_data["info"]["profile_picture_url"],
            date_of_birth=player_data["info"]["date_of_birth"]
        )

        # Map Tennis Matches
        tennis_singles_matches = [
            TennisMatch(
                match_id=match_id.get("match_id","n/a"), #todo: how to handle match_id not existing
                opponent=match["opponent"],
                score=match["score"],
                result=match["result"],
                date=match["date"],
                surface=match.get("surface", "unknown")
            )
            for match in player_data["tennis"]["singles"]["matches"]
        ]

        # Map Leagues
        tennis_leagues = [
            League(
                league_id=league["league_id"], 
                name="League Name"
            )  # Adjust if you store more league info
            for league in player_data["tennis"]["singles"]["leagues"]
        ]

        # Construct and return Player object
        player = cls(player_id=player_id, info=info) #tennis_matches=tennis_singles_matches, leagues=tennis_leagues
        player.tennis_matches = tennis_singles_matches
        player.leagues = tennis_leagues
        return player
    
    def to_dict(self) -> dict:
        """
        Converts the Player object into a dictionary format for JSON serialization.
        """
        return {
            "player_id": self.player_id,
            "info": self.info.to_dict(), #PlayerInfo
            "tennis": {
                "singles": {
                    "matches": [
                        {
                            "match_id": match.match_id,
                            "opponent": match.opponent,
                            "score": match.score,
                            "result": match.result,
                            "date": match.date,
                            "surface": match.surface
                        } for match in self.tennis_matches
                    ],
                    "leagues": [league.league_id for league in self.leagues]
                }
            }
        }
    
    def __str__(self):
        return f"Player(player_id={self.player_id}, info={self.info}, tennis={self.tennis_matches})"

    def __repr__(self):
        return f"Player(player_id={self.player_id}, info={self.info}, tennis={self.tennis_matches})"
    
