import gamesetmatch.api as api

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
    # GET request
    # Extract player_id from the query parameters
    logger.info(req)
    uid = req.args.get('uid')
    logger.info(f"Calling getPlayerDetails for uid={uid}")
    if not uid:
        logger.warning("uid parameter is missing.")
        return https_fn.Response("UID is required", status=400)

    try:
        # Call the api function to get the player details
        player_details = api.getPlayerDetails(uid=uid)
        
        if player_details is None:
            # Player not found, return 404
            logger.info(f"Player with uid={uid} not found.")
            return https_fn.Response(
                json.dumps({"message": "Player not found"}),
                status=200,
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

@https_fn.on_request()
def addPlayer(req: https_fn.Request) -> https_fn.Response:
    """
    Adds a new player to the Firestore database.

    This function expects a POST request with a JSON body containing player details.
    The player details should include:
      - uid (required): Unique identifier for the player.
      - info (required): A dictionary with player information like name and email.
      - level (required): Player's level (e.g., beginner, intermediate, advanced, pro).
      - tel_number (optional): The player's phone number.
      - area (optional): An integer representing the area ID.
      - sports (optional): A list of sports the player is interested in.

    Args:
        req (https_fn.Request): The request object containing player details in JSON format.

    Returns:
        https_fn.Response: A JSON response indicating success or error status.
    
    Example:
    (POST request)
    {
        "uid": "12345",
        "info": {
            "name": "John Doe",
            "email": "john.doe@example.com"
        },
        "level": "beginner",
        "tel_number": "123-456-7890",
        "area": 10,
        "sports": ["tennis", "pickleball"]
    }
    """
    # POST request
    # Parse the JSON request body
    logger.info(f"Received request: {req}")
    try:
        request_data = req.get_json()
        logger.info(f"Parsed request data: {request_data}")

        # Call the API layer to handle adding the player
        response_data = api.addPlayer(request_data)

        # Return success response
        logger.info(f"Player added successfully with data: {response_data}")
        return https_fn.Response(
            json.dumps({"message": response_data}),
            status=200,
            content_type="application/json"
        )
    except ValueError as e:
        # Handle validation errors
        logger.error(f"Validation error: {e}")
        return https_fn.Response(
            json.dumps({"error": str(e)}),
            status=400,
            content_type="application/json"
        )
    except Exception as e:
        # Handle other exceptions
        logger.error(f"Error adding player: {e}")
        return https_fn.Response(
            json.dumps({"error": "Internal Server Error"}),
            status=500,
            content_type="application/json"
        )