class League:
    def __init__(self, league_name, location, current_round, groups, archive):
        self.league_name = league_name
        self.location = location
        self.current_round = current_round
        self.groups = groups  # List of group IDs or objects
        self.archive = archive  # List of archived round data

    def to_dict(self):
        return {
            "league_name": self.league_name,
            "location": self.location,
            "current_round": self.current_round,
            "groups": [group.to_dict() for group in self.groups],
            "archive": self.archive
        }

    # Add methods as needed for league operations
