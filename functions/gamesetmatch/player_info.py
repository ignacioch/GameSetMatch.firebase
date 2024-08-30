# player_info.py

from datetime import datetime
from typing import Optional
from enum import Enum

class Gender(Enum):
    MALE = "male"
    FEMALE = "female"

class Level(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    PRO = "pro"

class Info:
    """
    A class to represent the player's personal information and authentication details.

    Attributes
    ----------
    name : str
        The name of the player.
    email : str
        The email address of the player.
    profile_picture_url : str
        The URL of the player's profile picture.
    date_of_birth : datetime
        The date of birth of the player.
    phone : str
        The phone number of the player.
    gender : Gender
        The gender of the player.
    self_reported_level : Level
        The self-reported skill level of the player.
    facebook_id : str, optional
        The unique Facebook ID of the player.
    google_id : str, optional
        The unique Google ID of the player.
    twitter_id : str, optional
        The unique Twitter ID of the player.
    password_hash : str, optional
        The hashed password for email/password login.
    default_location_id : str, optional
        The Firestore reference ID to the default location document.

    Methods
    -------
    __init__(name, email, profile_picture_url, date_of_birth, phone, gender, self_reported_level,
             facebook_id=None, google_id=None, twitter_id=None, password_hash=None, default_location_id=None)
        Initializes the Info instance with the provided attributes.
    """

    def __init__(self, name: str, email: str, profile_picture_url: str, date_of_birth: datetime, phone: str,
                 gender: Gender, self_reported_level: Level, facebook_id: Optional[str] = None,
                 google_id: Optional[str] = None, twitter_id: Optional[str] = None,
                 password_hash: Optional[str] = None, default_location_id: Optional[str] = None):
        """
        Constructs all the necessary attributes for the Info object.

        Parameters
        ----------
        name : str
            The name of the player.
        email : str
            The email address of the player.
        profile_picture_url : str
            The URL of the player's profile picture.
        date_of_birth : datetime
            The date of birth of the player.
        phone : str
            The phone number of the player.
        gender : Gender
            The gender of the player.
        self_reported_level : Level
            The self-reported skill level of the player.
        facebook_id : str, optional
            The unique Facebook ID of the player.
        google_id : str, optional
            The unique Google ID of the player.
        twitter_id : str, optional
            The unique Twitter ID of the player.
        password_hash : str, optional
            The hashed password for email/password login.
        default_location_id : str, optional
            The Firestore reference ID to the default location document.
        """
        self.name = name
        self.email = email
        self.profile_picture_url = profile_picture_url
        self.date_of_birth = date_of_birth
        self.phone = phone
        self.gender = gender
        self.self_reported_level = self_reported_level
        self.facebook_id = facebook_id
        self.google_id = google_id
        self.twitter_id = twitter_id
        self.password_hash = password_hash
        self.default_location_id = default_location_id

