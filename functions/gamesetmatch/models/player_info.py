class PlayerInfo:
    def __init__(self, name: str, email: str, profile_picture_url: str, date_of_birth: str):
        self.name = name
        self.email = email
        self.profile_picture_url = profile_picture_url
        self.date_of_birth = date_of_birth
    
    def to_dict(self):
        return {
            "name": self.name,
            "email": self.email,
            "profile_picture_url": self.profile_picture_url,
            "date_of_birth": self.date_of_birth
        }

    def __str__(self):
        return f"PlayerInfo(name={self.name}, email={self.email}, profilePictureUrl={self.profile_picture_url}, dateOfBirth={self.date_of_birth})"

    def __repr__(self):
        return self.__str__()