from typing import List, Optional

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
