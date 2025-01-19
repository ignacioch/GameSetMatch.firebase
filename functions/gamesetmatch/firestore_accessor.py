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
from gamesetmatch.models.user import User
from gamesetmatch.constants import FirestoreCollections

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
        player_ref = firestore_client.collection(FirestoreCollections.PLAYERS.value).document(uid)
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

def get_user_by_uid(uid: str):
    """
    Retrieves a user's document from the Firestore database by UID.

    Args:
        uid (str): The UID of the user.

    Returns:
        DocumentSnapshot: The user document if found, otherwise None.
    """
    try:
        user_doc = firestore_client.collection(FirestoreCollections.USERS.value).document(uid).get()
        if user_doc.exists:
            return user_doc
        else:
            return None
    except Exception as e:
        logger.error(f"Error retrieving user with UID {uid}: {e}")
        raise

def add_player_to_firestore(player: Player):
    """
    Adds a Player object to the Firestore database.

    Args:
        player (Player): The Player object to be added.
    """
    try:
        logger.info(f"Attempting to add player with ID {player.player_id} to Firestore.")
        player_ref = firestore_client.collection(FirestoreCollections.PLAYERS.value).document(player.player_id)
        player_ref.set(player.to_dict())
        logger.info(f"Player with ID {player.player_id} added successfully.")
    except Exception as e:
        logger.error(f"Error adding player with ID {player.player_id}: {e}")
        raise


def add_user_to_firestore(user: User):
    """
    Adds a User document to the Firestore database.

    Args:
        user (User): The User object to be added.
    """
    try:
        logger.info(f"Attempting to add user with UID {user.uid} to Firestore.")
        user_ref = firestore_client.collection(FirestoreCollections.USERS.value).document(user.uid)
        user_data = user.to_dict()
        user_data['updated'] = firestore.SERVER_TIMESTAMP  # Add timestamp field
        user_ref.set(user_data)
        logger.info(f"User with UID {user.uid} added successfully.")
    except Exception as e:
        logger.error(f"Error adding user with UID {user.uid}: {e}")
        raise