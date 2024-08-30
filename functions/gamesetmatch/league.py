from faker import Faker
import random
from .utils import generate_random_hex_int
from .types import LeagueFields

class League:
    def __init__(self, league_name, area, start_date=None, end_date=None):
        self.league_name = league_name
        self.area = area # ID of the area the leagues is for
        self.unallocated_players = []
        self.running = False 
        self.groups = {}  # List of group IDs
        self.archived = archive  # List of archived round data
        if start_date and end_date :
            self.current_round = 1
            self.dates = {
                LeagueFields.START_DATE.value : start_date
                LeagueFields.END_DATE.value : end_date
            }
        else :
            self.current_round = 0
            self.dates = {}

    def to_dict(self):
        return {
            LeagueFields.LEAGUE_NAME.value : self.league_name,
            LeagueFields.AREA.value: self.area,
            LeagueFields.RUNNING.value : self.running,
            LeagueFields.CURRENT_ROUND.value: self.current_round,
            LeagueFields.UNALLOCATED_PLAYERS.value : self.unallocated_players,
            LeagueFields.DATES.value: self.dates,
            LeagueFields.GROUPS.value: self.groups,
            LeagueFields.ARCHIVED.value: self.archived
        }

    @staticmethod
    def create_dummy_league() -> 'League':
        """
        Creates a league with various parameters being passed.

        Returns:
            League: An Instance of the League class filled with random data
        """
        pass
