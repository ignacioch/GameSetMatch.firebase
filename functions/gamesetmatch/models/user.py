from dataclasses import dataclass

@dataclass
class User:
    uid: str
    displayName: str
    photoUrl: str
    email: str

    @classmethod
    def from_dict(cls, data: dict) -> 'User':
        return cls(
            uid=data["uid"],
            displayName=data["displayName"],
            photoUrl=data["photoUrl"],
            email=data["email"]
        )

    def to_dict(self) -> dict:
        return {
            "uid": self.uid,
            "displayName": self.displayName,
            "photoUrl": self.photoUrl,
            "email": self.email
        }