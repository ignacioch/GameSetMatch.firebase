#3rd party API imports
from firebase_functions import https_fn

#local imports
from gamesetmatch.firestore_accessor import get_player_by_uid

# python lib imports
import logging
from typing import Dict,Optional,Any

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set to DEBUG or INFO as needed

def getPlayerDetails(uid: Optional[str]) -> Optional[dict]:
    """
    Retrieves the details of a specific player from the Firestore database by UID.

    Args:
        uid (str): The UID of the player (used as the document ID).

    Returns:
        Optional[dict]: The player's details if found, otherwise None.
    """
    if not uid:
        raise ValueError("UID must be provided")

    try:
        # Directly access the player document by UID (which is the document ID)
        player = get_player_by_uid(uid)
        
        if not player:
            logger.info(f"No player found with UID={uid}.")
            return None

        return player.to_dict()
    except Exception as e:
        logger.error(f"Error retrieving player details for UID={uid}: {e}")
        raise
        