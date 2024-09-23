#3rd party API imports
from firebase_functions import https_fn

#local imports
from gamesetmatch.firestore_accessor import get_player_document

# python lib imports
import logging
from typing import Dict,Optional,Any

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set to DEBUG or INFO as needed

def getPlayerDetails(player_id: str) -> Optional[Dict[str, Any]]: 
    """
    Retrieves the details of a specific player from the Firestore database.
    
    Args:
        player_id (str): The unique identifier of the player.

    Returns:
        Optional[Dict[str, Any]]: A dictionary containing the player's details if they exist, 
                                  otherwise None.
    """
    try:
        player_details = get_player_document(player_id)
        return player_details

    except Exception as e:
        logger.error(f"Error in getPlayerDetails for player_id={player_id}: {e}")
        raise
        