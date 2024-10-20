from dataclasses import dataclass,field
from enum import Enum
from typing import List

class Level(Enum):
    BEGINNER = 'beginner'
    INTERMEDIATE = 'intermediate'
    ADVANCED = 'advanced'
    PRO = 'pro'

    def __str__(self):
        return str(self.value)

@dataclass
class PlayerInfo:
    name : str 
    email : str 
    profile_picture_url : str 
    date_of_birth : str
    tel_number : str
    areas : List[int]
    level : Level

    @classmethod
    def from_dict(cls, info_data: dict) -> 'PlayerInfo':
        """
        Creates a PlayerInfo object from a dictionary.
        """
        level = info_data.get("level")
        if isinstance(level, str) and level in ("beginner","intermediate","advanced","pro"):
            level = Level[level.upper()]
        elif not isinstance(level, Level):
            raise ValueError("Invalid level value")

        return cls(
            name=info_data.get("name"),
            email=info_data.get("email"),
            profile_picture_url=info_data.get("profile_picture_url"),
            date_of_birth=info_data.get("date_of_birth"),
            tel_number=info_data.get("tel_number"),
            areas=info_data.get("areas"),
            level=level
        )
            
    def to_dict(self)-> dict:
        """
        Converts the PlayerInfo object into a dictionary format.
        """
        return {
            "name": self.name,
            "email": self.email,
            "profile_picture_url": self.profile_picture_url,
            "date_of_birth": self.date_of_birth,
            "tel_number": self.tel_number,
            "areas": self.areas,
            "level": self.level.value
        }

    def __str__(self):
        return f"PlayerInfo(name={self.name}, email={self.email}, profile_picture_url={self.profile_picture_url}, date_of_birth={self.date_of_birth}, tel_number={self.tel_number}, areas={self.areas}, level={self.level.value})"

    def __repr__(self):
        return f"PlayerInfo(name={self.name}, email={self.email}, profile_picture_url={self.profile_picture_url}, date_of_birth={self.date_of_birth}, tel_number={self.tel_number}, areas={self.areas}, level={self.level.value})"
