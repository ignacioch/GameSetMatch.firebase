from enum import Enum

MATCHES_COLLECTION = "matches"
PLAYERS_COLLECTION = "players"
LEAGUES_COLLECTION  = "leagues" 

class LeagueFields(Enum):
    LEAGUE_ID = "league_id"
    LEAGUE_NAME = "league_name"
    AREA = "area"
    RUNNING = "running"
    CURRENT_ROUND = "current_round"
    UNALLOCATED_PLAYERS = "unallocated_players"
    DATES = "dates"
    START_DATE = "start"
    END_DATE = "end"
    ID = "league_id"
    GROUPS = "groups"
    ARCHIVED = "archived"

class PlayerFields(Enum):
    EMAIL = "email"
    ID = "id"
    NAME = "name"
    RANKING = "ranking"
    DOB = "DOB"
    LEVEL = "level"
    AREAS = "areas"

class MatchFields(Enum):
    PLAYER_A_ID = "player_a_id"
    PLAYER_B_ID = "player_b_id"
    SCORE = "score"
    MATCH_DATE = "match_date"
    LOCATION = "location"
    MATCH_ID = "match_id"
    LEAGUE_ID = "league_id"
    GROUP = "group"
