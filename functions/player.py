class Player:
    def __init__(self, name, email, dob, level):
        self.name = name
        self.email = email
        self.dob = dob
        self.level = level
        self.id = id  # Optional ID attribute

    def to_dict(self):
        return {
            "id":self.id,
            "name": self.name,
            "email": self.email,
            "DOB": self.dob,
            "level": self.level
        }
    
    def __str__(self):
        return f"Player(name={self.name}, email={self.email}, DOB={self.dob}, level={self.level})"

    def __repr__(self):
        return self.__str__()
