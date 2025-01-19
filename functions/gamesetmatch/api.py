#3rd party API imports
from firebase_functions import https_fn

#local imports
from gamesetmatch.firestore_accessor import get_player_by_uid, add_player_to_firestore, get_user_by_uid, add_user_to_firestore
from gamesetmatch.models.player import Player
from gamesetmatch.models.player_info import PlayerInfo
from gamesetmatch.models.user import User

# python lib imports
import logging
from typing import Dict,Optional,Any

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set to DEBUG or INFO as needed

def __validate_user_existence(uid: str):
    """
    Validates if a user with the given UID exists in the Firestore users collection.

    Args:
        uid (str): The UID of the user.

    Raises:
        ValueError: If the user does not exist.
    """
    user_doc = get_user_by_uid(uid)
    if not user_doc:
        logger.error(f"User with UID {uid} does not exist.")
        raise ValueError(f"User with UID {uid} does not exist.")

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


def addPlayer(request_data: dict) -> bool:
    """
    Adds a new player to Firestore using the provided data.

    Args:
        request_data (dict): A dictionary containing the player information.

    Returns:
        bool: True if the player was added successfully, False if the email is already in use.
    """
    # Validate request data
    # Validate request data
    logger.info(f"Validating request data: {request_data}")
    __validate_user_existence(request_data["uid"])

    if "uid" not in request_data:
        logger.error("UID is required to add a player.")
        raise ValueError("UID is required to add a player.")

    # Extract and validate other details
    player_id = request_data["uid"]
    info = PlayerInfo.from_dict(request_data["info"])

    # Check if a player with the same email already exists
    existing_player = get_player_by_uid(player_id)
    if existing_player:
        existing_info = existing_player.info.to_dict()
        if existing_info.get("email") == info.email:
            logger.warning(f"Player with email {info.email} already exists.")
            return False

    logger.info(f"Creating Player object with player_id={player_id}")

    # Create Player object
    player = Player(
        player_id=player_id,
        info=info
    )

    # Add player to Firestore
    logger.info(f"Adding player to Firestore: {player}")
    add_player_to_firestore(player)

    logger.info(f"Player with ID {player_id} added successfully.")
    return True


def addUser(request_data: dict) -> bool:
    """
    Adds a new user to Firestore using the provided data.

    Args:
        request_data (dict): A dictionary containing the user information.

    Returns:
        bool: True if the user was added successfully, False if the user already exists.
    """
    # Validate request data
    logger.info(f"Validating request data: {request_data}")
    if "uid" not in request_data:
        logger.error("UID is required to add a user.")
        raise ValueError("UID is required to add a user.")

    uid = request_data["uid"]

    # Check if user already exists
    existing_user = get_user_by_uid(uid)
    if existing_user:
        logger.warning(f"User with UID {uid} already exists.")
        return False

    # Create User object
    user = User.from_dict(request_data)

    # Add user to Firestore
    logger.info(f"Adding user with UID {uid} to Firestore")
    add_user_to_firestore(user)

    logger.info(f"User with UID {uid} added successfully.")
    return True