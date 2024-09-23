import gamesetmatch.api as api

from firebase_functions import https_fn

# python lib imports
import logging
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set to DEBUG or INFO as needed

#from dotenv import load_dotenv
# Add this line to check if FUNCTIONS_EMULATOR is set
import os
# Load environment variables from .env file
#load_dotenv()x

print(f"FUNCTIONS_EMULATOR is set: {os.getenv('FUNCTIONS_EMULATOR')}")

if os.getenv('FUNCTIONS_EMULATOR'):
    print("Running in the emulator")
else:
    print("Running in production")


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
    # GET request
    # Extract player_id from the query parameters
    player_id = req.args.get('player_id')

    if not player_id:
        logger.warning("player_id parameter is missing.")
        return https_fn.Response("player_id parameter is required", status=400)

    try:
        print("Initializing Firebase Admin SDK...")
        # Call the api function to get the player details
        player_details = api.getPlayerDetails(player_id)
        
        if player_details is None:
            # Player not found, return 404
            logger.info(f"Player with player_id={player_id} not found.")
            return https_fn.Response(
                json.dumps({"error": "Player not found"}),
                status=404,
                content_type="application/json"
            )

        # Player exists, return their details
        return https_fn.Response(
            json.dumps(player_details),
            status=200,
            content_type="application/json"
        )
    except Exception as e:
        logger.error(f"Error retrieving player details: {e}")
        return https_fn.Response("Internal Server Error", status=500)