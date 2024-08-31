#3rd party API imports
from firebase_functions import https_fn
from firebase_admin import firestore, initialize_app
#from firebase_functions import logger
from google.cloud.firestore_v1.base_query import FieldFilter

# python lib imports
from datetime import datetime
import logging
import json
from typing import Dict,Optional,Any

app = initialize_app(options={"projectId":"gamesetmatch-ef350"})

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set to DEBUG or INFO as needed

firestore_client: google.cloud.firestore.Client = firestore.client()

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
        