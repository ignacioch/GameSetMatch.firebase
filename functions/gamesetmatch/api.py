#3rd party API imports
from firebase_functions import https_fn

#local imports
from gamesetmatch.firestore_accessor import get_player_document, get_player_by_uid

# python lib imports
import logging
from typing import Dict,Optional,Any

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set to DEBUG or INFO as needed

def getPlayerDetails(player_id: Optional[str], uid: Optional[str]) -> Optional[dict]:
    """
    Retrieves the details of a specific player from the Firestore database.
    
    Args:
        player_id (str): The unique identifier of the player.

    Returns:
        Optional[Dict[str, Any]]: A dictionary containing the player's details if they exist, 
                                  otherwise None.
    """
    try:
        if player_id:
            player = get_player_document(player_id)
        elif uid:
            player = get_player_by_uid(uid)
        else:
            raise ValueError("Either player_id or uid must be provided")
        
        # Use the Player class's to_dict method for serialization
        if not player:
            return None
        return player.to_dict()


    except Exception as e:
        logger.error(f"Error in getPlayerDetails for player_id={player_id} or uid={uid}: {e}")
        raise
        