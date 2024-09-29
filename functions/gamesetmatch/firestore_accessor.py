# python imports
import logging
import os
from typing import Optional, Dict, Any

# 3rd party imports
from firebase_admin import firestore, initialize_app, credentials

#local imports
from gamesetmatch.models.player import Player
from gamesetmatch.models.player_info import PlayerInfo
from gamesetmatch.models.tennis_match import TennisMatch
from gamesetmatch.models.league import League

# Initialize logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Define your project ID
PROJECT_ID = "gamesetmatch-ef350"

''' Things I tried to make ADC work
#if os.getenv('FUNCTIONS_EMULATOR'):
    # In the emulator, no credentials are needed
#    initialize_app()
#else:
#    # Production environment, use credentials / exported variable
#    cred_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
#    cred = credentials.Certificate(cred_path)
#    initialize_app(cred)

# Use Google Cloud's Application Default Credentials
#cred = credentials.ApplicationDefault()
'''
# In the end, I had to download the JSON key and add it to a folder that's not pushed to remove
# but is within the functions directory so GCC has access to it.
# relative path - not an absolute path
cred = credentials.Certificate('credentials/gamesetmatch-ef350-669e6b17d9a2.json')
initialize_app(cred)

# Initialize Firestore client
firestore_client = firestore.client()

def get_player_document(player_id: str) -> Optional[Player]:
    """
    Retrieves a player's document from the Firestore database.

    Args:
        player_id (str): The unique identifier of the player.

    Returns:
        Optional[Player]: A Player object if found, otherwise None.
    """
    try:
        player_ref = firestore_client.collection('players').document(player_id)
        player_doc = player_ref.get()
        
        if player_doc.exists:
            player_data = player_doc.to_dict()
            return Player.from_dict(player_id, player_data)  # Use from_dict to map data to Player object
        logger.info(f"No player found with player_id={player_id}")
        return None

    except Exception as e:
        logger.error(f"Error retrieving player details for player_id={player_id}: {e}")
        raise

def get_player_by_uid(uid: str) -> Optional[Player]:
    """
    Retrieves a player's document from the Firestore database.

    Args:
        uuid (str): The unique user identifier of the player.

    Returns:
        Optional[Dict[str, Any]]: A dictionary containing the player's details if they exist,
                                  otherwise None.
    """
    try:
        players_ref = firestore_client.collection('players')
        query = players_ref.where('uid', '==', uid).limit(1)
        results = query.get()

        for doc in results:
            player_data = doc.to_dict()
            return Player.from_dict(doc.id, player_data)
        logger.info(f"No player found with uid={uid}")
        return None
    except Exception as e:
        logger.error(f"Error retrieving player details for uid={uid}: {e}")
        raise
