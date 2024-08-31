from typing import Optional, Dict, Any
from firebase_admin import firestore
import logging

# Initialize logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Initialize Firestore client
firestore_client = firestore.client()

def get_player_document(player_id: str) -> Optional[Dict[str, Any]]:
    """
    Retrieves a player's document from the Firestore database.

    Args:
        player_id (str): The unique identifier of the player.

    Returns:
        Optional[Dict[str, Any]]: A dictionary containing the player's details if they exist,
                                  otherwise None.
    """
    try:
        player_ref = firestore_client.collection('players').document(player_id)
        player_doc = player_ref.get()
        
        if player_doc.exists:
            return player_doc.to_dict()
        else:
            logger.info(f"No player found with ID: {player_id}")
            return None

    except Exception as e:
        logger.error(f"Error retrieving player details for player_id={player_id}: {e}")
        raise
