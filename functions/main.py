import gamesetmatch.api_old as api_old

from firebase_functions import https_fn

# python lib imports
import logging
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set to DEBUG or INFO as needed


@https_fn.on_request()
def getPlayerDetails(req: https_fn.Request) -> https_fn.Response:
    """
    Retrieves details of a specific player from the Firestore database.
    
    If the player exists, it returns a 200 status code with the player's data.
    If the player does not exist, it returns a 404 status code.

    TODO : shall it also search by email/name?

    Args:
        req (https_fn.Request): The request object containing the query parameter 'player_id'.

    Returns:
        https_fn.Response: A JSON response containing the player's details if they exist,
        or a 404 status code with an appropriate message if they don't.
    """
    return api.getPlayerDetails