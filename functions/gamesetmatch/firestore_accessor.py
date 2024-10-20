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

def get_player_by_uid(uid: str) -> Optional[Player]:
    """
    Retrieves a player's document from the Firestore database.

    Args:
        uuid (str): The unique user identifier of the player.

    Returns:
        Optional[Player]: A Player object if found, otherwise None.
    """
    try:
        player_ref = firestore_client.collection('players').document(uid)
        player_doc = player_ref.get()

        if player_doc.exists:
            player_data = player_doc.to_dict()
            # Convert Firestore document data into a Player object
            return Player.from_dict(uid, player_data)
        else:
            logger.info(f"No player found with UID: {uid}")
            return None
    except Exception as e:
        logger.error(f"Error retrieving player details for uid={uid}: {e}")
        raise


def add_player_to_firestore(player: Player):
    """
    Adds a Player object to the Firestore database.

    Args:
        player (Player): The Player object to be added.
    """
    try:
        logger.info(f"Attempting to add player with ID {player.player_id} to Firestore.")
        player_ref = firestore_client.collection('players').document(player.player_id)
        player_ref.set(player.to_dict())
        logger.info(f"Player with ID {player.player_id} added successfully.")
    except Exception as e:
        logger.error(f"Error adding player with ID {player.player_id}: {e}")
        raise