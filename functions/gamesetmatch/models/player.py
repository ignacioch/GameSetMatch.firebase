from gamesetmatch.models.player_info import PlayerInfo

class Player:
    def __init__(self, player_id: str, info: PlayerInfo, tennis_matches: list, leagues: list):
        self.player_id = player_id
        self.info = info
        self.tennis_matches = tennis_matches
        self.leagues = leagues
    
    @classmethod
    def from_dict(cls, player_id: str, player_data: dict) -> 'Player':
        """
        Class method to create a Player object from a Firestore dictionary.
        """
        # Create PlayerInfo object
        info = PlayerInfo(
            name=player_data["info"]["name"],
            email=player_data["info"]["email"],
            profile_picture_url=player_data["info"]["profilePictureUrl"],
            date_of_birth=player_data["info"]["dateOfBirth"]
        )

        # Map Tennis Matches
        tennis_singles_matches = [
            TennisMatch(
                match_id=match_id,
                opponent=match["opponent"],
                score=match["score"],
                result=match["result"],
                date=match["date"],
                surface=match.get("surface", "unknown")
            )
            for match_id, match in player_data["tennis"]["singles"]["matches"].items()
        ]

        # Map Leagues
        tennis_leagues = [
            League(league_id=league_id, name="League Name")  # Adjust if you store more league info
            for league_id in player_data["tennis"]["singles"]["leagues"]
        ]

        # Construct and return Player object
        return cls(player_id=player_id, info=info, tennis_matches=tennis_singles_matches, leagues=tennis_leagues)
    
    def to_dict(self) -> dict:
        """
        Converts the Player object into a dictionary format for JSON serialization.
        """
        return {
            "player_id": self.player_id,
            "info": {
                "name": self.info.name,
                "email": self.info.email,
                "profilePictureUrl": self.info.profile_picture_url,
                "dateOfBirth": self.info.date_of_birth
            },
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