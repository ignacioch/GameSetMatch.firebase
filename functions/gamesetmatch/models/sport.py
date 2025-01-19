from gamesetmatch.models.category import Category

class Sport:
    def __init__(self, sport: str, singles: Category, doubles: Category):
        self.sport_name = sport
        self.singles = singles
        self.doubles = doubles

    @classmethod
    def from_dict(cls, sport_data: dict) -> 'Sport':
        sport_name = sport_data["sport_name"]
        singles = Category.from_dict(sport_data["singles"])
        doubles = Category.from_dict(sport_data["doubles"])
        return cls(sport=sport_name, singles=singles, doubles=doubles)

    def to_dict(self) -> dict:
        return {
            "sport_name": self.sport_name,
            "singles": self.singles.to_dict(),
            "doubles": self.doubles.to_dict()
        }

    def __str__(self):
        return f"Sport({self.sport_name}: singles={str(self.singles)}, doubles={str(self.doubles)})"

    def __repr__(self):
        return f"Sport({self.sport_name}: singles={repr(self.singles)}, doubles={repr(self.doubles)})"
