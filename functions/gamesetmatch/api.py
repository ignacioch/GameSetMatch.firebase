#3rd party API imports
from firebase_functions import https_fn

#local imports
from gamesetmatch.firestore_accessor import get_player_by_uid, add_player_to_firestore
from gamesetmatch.models.player import Player
from gamesetmatch.models.player_info import PlayerInfo, Level

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


def addPlayer(request_data: dict) -> bool:
    """
    Adds a new player to Firestore using the provided data.

    Args:
        request_data (dict): A dictionary containing the player information.

    Returns:
        bool: True if the player was added successfully, False if the email is already in use.
    """
    # Validate request data
    logger.info(f"Validating request data: {request_data}")
    if "uid" not in request_data:
        logger.error("UID is required to add a player.")
        raise ValueError("UID is required to add a player.")

    # Extract and validate other details
    player_id = request_data["uid"]
    info = PlayerInfo.from_dict(request_data["info"])
    level = Level(request_data["level"])  # Validates that level is within Enum choices
    tel_number = request_data.get("tel_number")
    area = request_data.get("area")
    sports = request_data.get("sports", [])

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
        info=info,
        level=level,
        tel_number=tel_number,
        area=area,
        sports=sports
    )

    # Add player to Firestore
    logger.info(f"Adding player to Firestore: {player}")
    add_player_to_firestore(player)

    logger.info(f"Player with ID {player_id} added successfully.")
    return True