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
from typing import Dict,Any

# local imports
from .player import Player
from .match import Match
#import .logger
from .firestore import writePlayerToFirestore,addMatchToFirestore,getPlayerDetailsFromFirestore,deletePlayerFromFirestore,deleteMatchFromFirestore,getMatchDetailsFromFirestore,addPlayerToLeagueFirestore,createLeagueFirestore,startRoundInLeagueFirestore,fetchPendingPlayersForLeague

app = initialize_app(options={"projectId":"gamesetmatch-ef350"})

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set to DEBUG or INFO as needed

def registerPlayer(req: https_fn.Request) -> https_fn.Response:
    """
    Registers a new player and adds their information to the Firestore database.
    
    This function parses JSON data from the incoming HTTP POST request and creates
    a new player entry in Firestore. The JSON payload must include the following fields:
    - name (str): The name of the player.
    - email (str): The email of the player.
    - DOB (str): The date of birth of the player, in "YYYY-MM-DD" format.
    - level (str): The skill level of the player.
    - areas (list of str, optional): An array of strings, each representing an area ID where the player is interested in participating.

    Args:
        req (https_fn.Request): The request object containing JSON data with the player's information.

    Returns:
        https_fn.Response: A JSON response containing the newly created player's data,
        including their unique Firestore ID, or an error message with an appropriate
        HTTP status code on failure. The response includes the player's name, email,
        date of birth (DOB), level, and areas of interest.
    """

    # Parse JSON data from request body
    request_json = req.get_json()
    logger.debug(f"Incoming request_raw={request_json}")
    if not request_json:
        return https_fn.Response("Invalid request", status=400)
    
    name = request_json["name"]
    email = request_json["email"]
    dob = request_json["DOB"]
    level = request_json["level"]
    areas = request_json.get("areas")  # Expecting an array of area IDs

    player = Player(name, email, dob, level, areas)
    logger.info(f"Incoming request={player}")
    
    # Check for missing parameters
    if not all([name, email, dob, level]) or 'areas' not in request_json:
        return https_fn.Response("Required parameters NOT provided", status=400)

    firestore_client: google.cloud.firestore.Client = firestore.client()
            
    try:
        saved_player = writePlayerToFirestore(firestore_client.transaction(), firestore_client, player)
        logger.info(f"Player {saved_player.id}:{saved_player.name} added successfully.")
        return https_fn.Response(json.dumps({"player": saved_player.to_dict()}), status=200, content_type="application/json")
    except ValueError as e:
        return https_fn.Response(str(e), status=400)

def _addNonLeagueMatch(request_json) -> https_fn.Response:
    """
    Adds a new match record to the Firestore database.

    Extracts match details from the JSON payload of an HTTP POST request. It requires
    'player_a_id', 'player_b_id', 'score', 'date', and 'location' fields, and optionally
    accepts a 'match_id'.

    Args:
        request_json (JSON): The request object containing JSON data for the match.

    Returns:
        https_fn.Response: A JSON response containing the newly added match's data,
        including its Firestore ID, or an error message with an appropriate HTTP
        status code on failure
    """

    player_a_id = request_json.get("player_a_id")
    player_b_id = request_json.get("player_b_id")
    score = request_json.get("score")
    match_id = request_json.get("match_id")  # Can be None
    match_date = request_json.get("match_date")
    location = request_json.get("location")

    match_info = Match(player_a_id, player_b_id, score, match_date, location, match_id)
    logger.info(f"Adding Match. type=NoLeague match={match_info}")

    valid, error_message, error_code = match_info.is_valid_match()
    if not valid:
        return https_fn.Response(error_message, status=error_code)
        
    firestore_client: google.cloud.firestore.Client = firestore.client()
        
    # Check if both players exist
    if "match_id" not in match_info.to_dict() and not getPlayerDetailsFromFirestore(firestore_client,match_info.player_a_id):
        return https_fn.Response(f"Player A (ID= {match_info.player_a_id}) does not exist", status=400)
    if "match_id" not in match_info.to_dict() and not getPlayerDetailsFromFirestore(firestore_client,match_info.player_b_id):
        return https_fn.Response(f"Player B (ID= {match_info.player_b_id}) does not exist", status=400)
    # Add match
    new_match = addMatchToFirestore(firestore_client.transaction(), firestore_client, match_info)

    logger.info(f"Match {new_match.match_id} added successfully.")
    return https_fn.Response(json.dumps({"match": new_match.to_dict()}), status=200, content_type="application/json")

def _addLeagueMatch(request_json) -> https_fn.Response:
    """
    Adds a match that belongs to a league.
    """


def addMatch(req: https_fn.Request) -> https_fn.Response:
    """
    Adds a new match record to the Firestore database.

    Extracts match details from the JSON payload of an HTTP POST request. It requires
    'player_a_id', 'player_b_id', 'score', 'date', and 'location' fields, and optionally
    accepts a 'match_id'.

    Args:
        req (https_fn.Request): The request object containing JSON data for the match.

    Returns:
        https_fn.Response: A JSON response containing the newly added match's data,
        including its Firestore ID, or an error message with an appropriate HTTP
        status code on failure.
    """
    # Parse JSON data from request body
    request_json = req.get_json()
    """Add match data to the Firestore database."""
    try:
        # Extracting match data from request
        logger.debug(f"Incoming request_raw={request_json}")
        if not request_json:
            return https_fn.Response("Invalid request", status=400)

        # Extract from request
        league_id = request_json.get("league_id")  # This can be None
        if league_id is None :
            return _addNonLeagueMatch(request_json)
        
    except Exception as e:
        logging.error(f"Error adding match: {str(e)}")
        return https_fn.Response(f"Error: {str(e)}", status=500)


def getPlayerDetails(req: https_fn.Request) -> https_fn.Response:
    """
    Retrieves details of a specific player from the Firestore database.

    Accepts a JSON payload in an HTTP POST request with either 'player_id', 'name', or
    'email' fields to specify the player to be retrieved.

    Args:
        req (https_fn.Request): The request object containing JSON data to identify the player.

    Returns:
        https_fn.Response: A JSON response containing the requested player's details, or
        a 'Player not found' message with a 404 status code if the player does not exist.
    """
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


def deletePlayer(req: https_fn.Request) -> https_fn.Response:
    """
    Deletes a player from the Firestore database.

    Requires a JSON payload in an HTTP POST request with the 'player_id' field
    to specify which player to delete.

    Args:
        req (https_fn.Request): The request object containing JSON data with 'player_id'.

    Returns:
        https_fn.Response: A confirmation message upon successful deletion, or an error
        message with an appropriate HTTP status code on failure.
    """
    data = req.get_json()
    player_id = data.get("player_id") if data else None
    logger.info(f"deletePlayer called for id={player_id}")

    if not player_id:
        return https_fn.Response("Player ID is required", status=400)

    firestore_client: google.cloud.firestore.Client = firestore.client()
    try:
        deletePlayerFromFirestore(firestore_client, player_id)
        return https_fn.Response(f"Player {player_id} deleted successfully.", status=200)
    except Exception as e:
        return https_fn.Response(f"Error: {str(e)}", status=500)


def deleteMatch(req: https_fn.Request) -> https_fn.Response:
    """
    Deletes a match record from the Firestore database.

    Requires a JSON payload in an HTTP POST request with the 'match_id' field
    to specify which match to delete.

    Args:
        req (https_fn.Request): The request object containing JSON data with 'match_id'.

    Returns:
        https_fn.Response: A confirmation message upon successful deletion, or an error
        message with an appropriate HTTP status code on failure.
    """
    data = req.get_json()
    match_id = data.get("match_id") if data else None
    logger.info(f"deleteMatch called for id={match_id}")

    if not match_id:
        return https_fn.Response("Match ID is required", status=400)

    firestore_client: google.cloud.firestore.Client = firestore.client()
    try:
        deleteMatchFromFirestore(firestore_client, match_id)
        return https_fn.Response(f"Match {match_id} deleted successfully.", status=200)
    except Exception as e:
        return https_fn.Response(f"Error: {str(e)}", status=500)

def getMatchDetails(req: https_fn.Request) -> https_fn.Response:
    """
    Retrieves details of a specific match or matches involving a specific player
    from the Firestore database.

    Accepts query parameters in an HTTP GET request with 'match_id' or 'player_id'
    fields to specify the match(es) to be retrieved.

    Returns:
        https_fn.Response: A JSON response containing the requested match's details, or
        a 'No matches found' message with a 404 status code if no matches meet the criteria.
    """
    logger.debug("removeme")
    match_id = req.args.get("match_id")
    player_id = req.args.get("player_id")
    logger.debug(f"getMatchDetails:match_id={match_id}:player_id={player_id}")
    firestore_client: google.cloud.firestore.Client = firestore.client()
    match_details = getMatchDetailsFromFirestore(firestore_client, match_id, player_id)

    if match_details or (player_id is None and match_id is None):
        return https_fn.Response(json.dumps(match_details), status=200)
    else:
        return https_fn.Response("No matches found", status=404)

def addPlayerToLeague(req: https_fn.Request) -> https_fn.Response:
    """
    Adds a player to a specified league by updating the Firestore database.

    This endpoint expects a JSON payload with 'player_id' and 'league_id'.
    It validates the existence of both IDs, adds the player to the league if not already added,
    and updates the league's unallocated players list.

    Args:
        req (https_fn.Request): The incoming request with JSON payload containing 'player_id' and 'league_id'.
    
    Fields:
        - player_id (str): The ID of the player
        - league_id (str): The ID of the league they are entering

    Returns:
        https_fn.Response: A JSON response with updated league information or an error message.
    """
    request_json: Dict[str, Any] = req.get_json(silent=True) or {}
    player_id: str = request_json.get("player_id", "")
    league_id: str = request_json.get("league_id", "")

    if not player_id or not league_id:
        return https_fn.Response("Player ID and League ID are required", status=400)

    try:
        league_info: Dict[str, Any] = addPlayerToLeagueFirestore(player_id, league_id)
        return https_fn.Response(json.dumps({"league_info": league_info}), status=200, content_type="application/json")
    except ValueError as e:
        return https_fn.Response(str(e), status=400)


def createLeague(req: https_fn.Request) -> https_fn.Response:
    """
    Creates a new league with specified details and adds it to the Firestore database.

    This function parses JSON data from the incoming HTTP POST request to create a new league.
    It requires 'league_name', 'area_id', 'start_date', and 'end_date' fields in the JSON payload.

    Args:
        req (https_fn.Request): The request object containing JSON data.

    Fields:
        - league_name (str): The name of the league to be created.
        - area_id (str): The identifier of the area where the league is located.
        - start_date (str): The start date of the league, in "YYYY-MM-DD" format.
        - end_date (str): The end date of the league, in "YYYY-MM-DD" format.

    Returns:
        https_fn.Response: A JSON response containing the newly created league's details,
        including its unique Firestore ID and other provided information,
        or an error message with an appropriate HTTP status code on failure.
    """

    # Extracts data from the request JSON payload
    request_json = req.get_json()
    league_name = request_json.get("league_name") # Eg Northern Sector Round 1
    area_id = request_json.get("area")  # This is the id of the area the league is created for
    start_date = request_json.get("start_date")  # Expects format: "YYYY-MM-DD"
    end_date = request_json.get("end_date")      # Expects format: "YYYY-MM-DD"

    # Validates the presence of mandatory fields
    if not league_name or not area_id:
        return https_fn.Response("League name and area are required", status=400)

    # Attempts to create the league in Firestore and return its details
    try:
        league_info = createLeagueFirestore(league_name, area_id, start_date, end_date)
        return https_fn.Response(json.dumps({"league_info": league_info}), status=200, content_type="application/json")
    except ValueError as e:
        return https_fn.Response(str(e), status=400)

def startRound(req: https_fn.Request) -> https_fn.Response:
    """
    Starts a new round in an existing league by organizing unallocated players into groups.

    This function initiates a new round in a league specified by the league_id in the request.
    It checks if there are unallocated players in the league; if so, it organizes these players into groups
    based on their levels and updates the league's current round and status to running. The function also
    ensures that leagues without unallocated players do not start a new round and returns an error instead.

    
    Args:
        req (https_fn.Request): The request object containing JSON data.
        
    Fields:
        - league_id (str): The unique identifier of the league to start a new round for.
    
    Returns:
        https_fn.Response: A JSON response containing information about the update, including:
        - A success message and details of the new round if the operation is successful.
        - An error message with an appropriate HTTP status code if the operation fails,
          such as when there are no unallocated players or the league does not exist.
    
    Raises:
        ValueError: If the league does not have unallocated players or if the league_id does not correspond to an existing league.

    """
    
    request_json = req.get_json()
    league_id = request_json.get("league_id")
    
    if not league_id:
        return https_fn.Response("League ID is required", status=400)
    
    try:
        players : List[Player] = fetchPendingPlayersForLeague(league_id)
        logger.debug(f"Will assign {players} into groups.")
        if not players:
            return https_fn.Response("No unallocated players to start a round", status=400)
        
        sorted_groups = Player.sort_and_group_players(players)
        logger.debug(f"Sorted_groups:{sorted_groups}")
        league_info = startRoundInLeagueFirestore(league_id, sorted_groups)
        logger.debug(f"League Updated. New value={league_info}")
        return https_fn.Response(json.dumps({"message": "Round started successfully",
                                             "league_info": league_info}), 
                                 status=200, content_type="application/json")
    except ValueError as e:
        return https_fn.Response(str(e), status=400)






