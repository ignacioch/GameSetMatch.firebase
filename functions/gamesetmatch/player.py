from typing import List, Optional, Dict

class Player:
    def __init__(self, name: str, email: str, dob: str, level: str, areas: List[str]) -> None:
        self.name: str = name
        self.email: str = email
        self.dob: str = dob
        self.level: str = level  # String representation of self-evaluation
        self.areas: List[str] = areas
        self.id: Optional[str] = None  # Optional ID attribute
        self.ranking: int = 0  # Ranking 

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "DOB": self.dob,
            "level": self.level,
            "areas": self.areas,  # Include areas in the dictionary representation
            "ranking": self.ranking
        }
    
    def __str__(self) -> str:
        return (f"Player(name={self.name}, email={self.email}, DOB={self.dob}, "
                f"level={self.level}, areas={self.areas}, ranking={self.ranking})")

    def __repr__(self) -> str:
        return self.__str__()
    
    @staticmethod
    def sort_and_group_players(players_info: List[Dict]) -> Dict[str, List[str]]:
        """
        Sorts and groups unallocated players by their ranking.

        Args:
            unallocated_players (List[str]): List of unallocated player IDs.

        Returns:
            Dict[str, List[str]]: A dictionary with group names as keys and lists of player IDs as values.
        """
        # Sort players by their ranking
        sorted_players = sorted(players_info, key=lambda x: x['ranking'], reverse=True)
    
        # Group sorted players into groups of 5 to 8
        groups = {}
        group_size = 5
        for i in range(0, len(sorted_players), group_size):
            group_name = f"group{i//group_size + 1}"
            groups[group_name] = [player['id'] for player in sorted_players[i:i+group_size]]
            if len(sorted_players) - i <= 8:
                group_size = 8

        return groups
    
    
