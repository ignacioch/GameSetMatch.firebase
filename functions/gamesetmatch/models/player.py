from gamesetmatch.models.player_info import PlayerInfo
from gamesetmatch.models.sport import Sport

class Player:
    def __init__(self, player_id: str, info: PlayerInfo):
        self.player_id = player_id
        self.info = info
        self.sports = {}
    
    def add_sport(self, sport_name: str, sport: Sport):
        self.sports[sport_name] = sport
    
    @classmethod
    def from_dict(cls, player_id: str, player_data: dict) -> 'Player':
        """
        Class method to create a Player object from a Firestore dictionary.
        Used mainly for testing.
        """
        # Create PlayerInfo object
        info = PlayerInfo.from_dict(player_data["info"])
        #    name=player_data["info"]["name"],
        #    email=player_data["info"]["email"],
        #    profile_picture_url=player_data["info"]["profile_picture_url"],
        #    date_of_birth=player_data["info"]["date_of_birth"]
        player = cls(player_id=player_id, info=info)

        # Populate sports

        # Populate sports
        for sport_name, sport_data in player_data.get("sports", {}).items():
            sport = Sport.from_dict(sport_data)
            player.add_sport(sport_name, sport)

        return player
    
    def to_dict(self) -> dict:
        """
        Converts the Player object into a dictionary format for JSON serialization.
        """
        return {
            "player_id": self.player_id,
            "info": self.info.to_dict(),
            "sports": {sport_name: sport.to_dict() for sport_name, sport in self.sports.items()}
        }

    def __str__(self):
        sports_str = ', '.join(f"{sport_name}: {str(sport)}" for sport_name, sport in self.sports.items())
        return f"Player(player_id={self.player_id}, info={self.info}, sports=[{sports_str}])"

    def __repr__(self):
        sports_repr = ', '.join(f"{sport_name}: {repr(sport)}" for sport_name, sport in self.sports.items())
        return f"Player(player_id={self.player_id}, info={repr(self.info)}, sports=[{sports_repr}])"