# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

#3rd party API imports
from firebase_functions import https_fn
from firebase_admin import firestore, initialize_app
#from firebase_functions import logger
from google.cloud.firestore_v1.base_query import FieldFilter

# python lib imports
import logging
import json

# local imports
from player import Player
from match import Match
import logger
from firestore import writePlayerToFirestore,addMatchToFirestore,getPlayerDetailsFromFirestore

app = initialize_app(options={"projectId":"gamesetmatch-ef350"})
#
#
# @https_fn.on_request()
# def on_request_example(req: https_fn.Request) -> https_fn.Response:
#     return https_fn.Response("Hello world!")

@https_fn.on_request()
def registerPlayer(req: https_fn.Request) -> https_fn.Response:
    """Take the text parameter passed to this HTTP endpoint and insert it into
    a new document in the players collection."""
    # Parse JSON data from request body
    request_json = req.get_json()
    logger.debug(f"Incoming request_raw={request_json}")
    if not request_json:
        return https_fn.Response("Invalid request", status=400)
    
    name = request_json["name"]
    email = request_json["email"]
    dob = request_json["DOB"]
    level = request_json["level"]

    player = Player(name, email, dob, level)
    logger.info(f"Incoming request={player}")
    
    # Check for missing parameters
    if not all([name, email, dob, level]):
        return https_fn.Response("Required parameters NOT provided", status=400)

    firestore_client: google.cloud.firestore.Client = firestore.client()
        
    try:
        writePlayerToFirestore(firestore_client.transaction(),firestore_client,player)
        return https_fn.Response(f"Player {name} added successfully.")
    except ValueError as e:
        return https_fn.Response(str(e), status=400)



@https_fn.on_request()
def addMatch(req: https_fn.Request) -> https_fn.Response:
    """Take the text parameter passed to this HTTP endpoint and insert it into
    a new document in the matches collection."""
    # Parse JSON data from request body
    request_json = req.get_json()

    """Add match data to the Firestore database."""
    try:
        # Extracting match data from request
        request_json = req.get_json()
        logger.debug(f"Incoming request_raw={request_json}")
        if not request_json:
            return https_fn.Response("Invalid request", status=400)

        # Extract match data
        player_a_id = request_json.get("player_a_id")
        player_b_id = request_json.get("player_b_id")
        score = request_json.get("score")
        match_id = request_json.get("match_id")  # Can be None
        match_date = request_json.get("date")
        location = request_json.get("location")

        match_info = Match(player_a_id, player_b_id, score, match_date, location, match_id)
        logger.info(f"Incoming request={match_info}")

        if "match_id" not in match_info.to_dict() and not all(value for key, value in match_info.items() if key != "match_id"):
            return https_fn.Response("Missing match parameters", status=400)


        firestore_client: google.cloud.firestore.Client = firestore.client()
        
        # Check if both players exist
        if "match_id" not in match_info.to_dict() and not getPlayerDetailsFromFirestore(firestore_client,match_info.player_a_id):
            return https_fn.Response(f"Player A (ID= {match_info.player_a_id}) does not exist", status=400)
        if "match_id" not in match_info.to_dict() and not getPlayerDetailsFromFirestore(firestore_client,match_info.player_b_id):
            return https_fn.Response(f"Player B (ID= {match_info.player_b_id}) does not exist", status=400)
        # Add match
        addMatchToFirestore(firestore_client.transaction(), firestore_client, match_info)

        return https_fn.Response("Match added successfully")

    except Exception as e:
        logging.error(f"Error adding match: {str(e)}")
        return https_fn.Response(f"Error: {str(e)}", status=500)



@https_fn.on_request()
def getPlayerDetails(req: https_fn.Request) -> https_fn.Response:
    request_json = req.get_json()

    player_id = request_json.get("player_id")
    name = request_json.get("name")
    email = request_json.get("email")

    firestore_client: google.cloud.firestore.Client = firestore.client()
    player_details = getPlayerDetailsFromFirestore(firestore_client, player_id, name, email)

    if player_details:
        return https_fn.Response(json.dumps(player_details), status=200)
    else:
        return https_fn.Response("Player not found", status=404)
