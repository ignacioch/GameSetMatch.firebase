from typing import List, Optional, Dict
from faker import Faker
import random
from .utils import generate_random_hex_int 
from .types import PlayerFields

class Player:
    # Define constants for group sizes at the class level
    BASE_GROUP_SIZE = 5
    MAX_GROUP_SIZE = 8
    MIN_GROUP_SIZE = 3

    def __init__(self, name: str, email: str, dob: str, level: str, areas: List[str], ranking: int= 0) -> None:
        self.name: str = name
        self.email: str = email
        self.dob: str = dob
        self.level: str = level  # String representation of self-evaluation
        self.areas: List[str] = areas
        self.id: Optional[str] = None  # Optional ID attribute
        self.ranking: int = ranking  # Ranking 

    def to_dict(self) -> dict:
        return {
            PlayerFields.ID.value: self.id,
            PlayerFields.NAME.value: self.name,
            PlayerFields.EMAIL.value: self.email,
            PlayerFields.DOB.value: self.dob,
            PlayerFields.LEVEL.value: self.level,
            PlayerFields.AREAS.value: self.areas,  # Include areas in the dictionary representation
            PlayerFields.RANKING.value: self.ranking
        }
    
    def __str__(self) -> str:
        return (f"Player(name={self.name}, email={self.email}, DOB={self.dob}, "
                f"level={self.level}, areas={self.areas}, ranking={self.ranking})")

    def __repr__(self) -> str:
        return self.__str__()

    @staticmethod
    def distribute_players(player_count: int) -> List[int]:
        """
        Calculates the distribution of players into groups based on predefined size limits.

        Args:
            player_count (int): The total number of players to be distributed.

        Returns:
            List[int]: A list where each element represents the number of players in a group.
        """
        group_sizes = [Player.BASE_GROUP_SIZE] * (player_count // Player.BASE_GROUP_SIZE)
        leftover_players = player_count % Player.BASE_GROUP_SIZE
        if leftover_players > Player.MIN_GROUP_SIZE or len(group_sizes) == 0:
            group_sizes.append(leftover_players)    
            return group_sizes
        i = 0
        # Distribute leftover players to the first groups, increasing their size towards the maximum limit.
        while leftover_players > 0 :
            for i in range(len(group_sizes)):
                if leftover_players > 0:
                    group_sizes[i] += 1
                    leftover_players -= 1

        # If there are still leftover players after maximizing existing groups, create a new group for them.
        if leftover_players > 0:
            group_sizes.append(leftover_players)

        return group_sizes
    
    @staticmethod
    def sort_and_group_players(players_info: List['Player']) -> Dict[str, List[str]]:
        """
        Sorts players by their ranking and groups them into evenly sized groups, respecting the group size limits.

        Args:
            players_info (List[Dict]): A list of dictionaries, each representing a player and containing at least
                                       an 'id' key and a 'ranking' key.

        Returns:
            Dict[str, List[str]]: A dictionary where each key is a group name and each value is a list of player IDs
                                   in that group.
        """
        # Sort players by their ranking in descending order to group by skill level.
        sorted_players = sorted(players_info, key=lambda player: player.ranking, reverse=True)
        group_sizes = Player.distribute_players(len(sorted_players))
        groups = {}
        start_index = 0
        for i, size in enumerate(group_sizes):
            group_name = f"group_{i+1}"
            groups[group_name] = [player.id for player in sorted_players[start_index:start_index + size]]
            start_index += size

        return groups
    


    @staticmethod
    def create_dummy_player(id: str = None, rankingIn: int = None, city: str = None) -> 'Player':
        """
        Creates a dummy Player object with random data for testing purposes.

        Returns:
            Player: An instance of the Player class filled with random data.
        """
        fake = Faker()
        name = fake.name()
        email = fake.email()
        dob = fake.date_of_birth(minimum_age=18, maximum_age=40).strftime("%Y-%m-%d")
        level = random.choice(['beginner', 'intermediate', 'advanced', 'expert'])
        areas = [city] if city else [fake.city() for _ in range(random.randint(1, 3))]  # Randomly assign 1 to 3 areas
        ranking = rankingIn if rankingIn else fake.random_int(min=1, max=1000)

        p = Player(name, email, dob, level, areas, ranking)
        p.id = id if id else generate_random_hex_int
        return p
    
    
