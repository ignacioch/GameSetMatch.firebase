class PlayerInfo:
    def __init__(self, name: str, email: str, profile_picture_url: str, date_of_birth: str):
        self.name = name
        self.email = email
        self.profile_picture_url = profile_picture_url
        self.date_of_birth = date_of_birth

    @classmethod
    def from_dict(cls, info_data: dict) -> 'PlayerInfo':
        """
        Creates a PlayerInfo object from a dictionary.
        """
        return cls(
            name=info_data.get("name"),
            email=info_data.get("email"),
            profile_picture_url=info_data.get("profile_picture_url"),
            date_of_birth=info_data.get("date_of_birth")
        )

    def to_dict(self) -> dict:
        """
        Converts the PlayerInfo object into a dictionary format.
        """
        return {
            "name": self.name,
            "email": self.email,
            "profile_picture_url": self.profile_picture_url,
            "date_of_birth": self.date_of_birth
        }

    def __str__(self):
        return f"PlayerInfo(name={self.name}, email={self.email}, profilePictureUrl={self.profile_picture_url}, dateOfBirth={self.date_of_birth})"

    def __repr__(self):
        return f"PlayerInfo(name={self.name}, email={self.email}, profilePictureUrl={self.profile_picture_url}, dateOfBirth={self.date_of_birth})"
