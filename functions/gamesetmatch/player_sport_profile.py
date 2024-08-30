# player_sport_profile.py

from typing import List

class PlayerSportProfile:
    """
    A class to represent the player's sport-specific profile details.

    Attributes
    ----------
    pts : int
        The points accumulated by the player in the sport.
    global_ranking : int
        The global ranking of the player in the sport.
    leagues : list of str
        List of Firestore references to league documents.
    matches : list of str
        List of Firestore references to match documents.

    Methods
    -------
    __init__(pts, global_ranking, leagues, matches)
        Initializes the PlayerSportProfile instance with the provided attributes.
    """

    def __init__(self, pts: int, global_ranking: int, leagues: List[str], matches: List[str]):
        """
        Constructs all the necessary attributes for the PlayerSportProfile object.

        Parameters
        ----------
        pts : int
            The points accumulated by the player in the sport.
        global_ranking : int
            The global ranking of the player in the sport.
        leagues : list of str
            List of Firestore references to league documents.
        matches : list of str
            List of Firestore references to match documents.
        """
        self.pts = pts
        self.global_ranking = global_ranking
        self.leagues = leagues
        self.matches = matches
