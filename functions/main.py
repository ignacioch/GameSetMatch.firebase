import gamesetmatch.api_old as api_old

from firebase_functions import https_fn

# python lib imports
import logging
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set to DEBUG or INFO as needed

@https_fn.on_request()
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
    return api_old.getMatchDetails(req)

@https_fn.on_request()
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
    return api_old.addMatch(req)

@https_fn.on_request()
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
    return api_old.registerPlayer(req)

@https_fn.on_request()
def getPlayerDetailsLegacy(req: https_fn.Request) -> https_fn.Response:
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
    return api_old.getPlayerDetails(req)


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


@https_fn.on_request()
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
    return api_old.deletePlayer(req)

@https_fn.on_request()
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
    return api_old.deleteMatch(req)


@https_fn.on_request()
def addPlayerToLeague(req: https_fn.Request) -> https_fn.Response:
    """
    Endpoint to add a player to a league.

    Expects a POST request with a JSON payload containing 'player_id' and 'league_id'.
    Adds the player to the specified league and updates the league's list of players.

    Args:
        req (https_fn.Request): The request object containing JSON data.

    Returns:
        https_fn.Response: A JSON response confirming the addition of the player to the league,
        or an error message with an appropriate HTTP status code on failure.
    """
    return api_old.addPlayerToLeague(req)

@https_fn.on_request()
def createLeague(req: https_fn.Request) -> https_fn.Response:
    """
    Endpoint to create a league. This is meant to be called for just creating a new League

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
    return api_old.createLeague(req)

@https_fn.on_request()
def startRound(req: https_fn.Request) -> https_fn.Response:
    """
    Starts a new round in a league, creating groups from unallocated players.

    This function initiates a new round in a league specified by the league_id in the request.
    It checks if there are unallocated players in the league; if so, it organizes these players into groups
    based on their levels and updates the league's current round and status to running. The function also
    ensures that leagues without unallocated players do not start a new round and returns an error instead.

    Args:
        req (https_fn.Request): The request object containing JSON data.

    Fields:
        - league_id (str): The unique identifier of the league for which to start a new round.

    Returns:
        https_fn.Response: A JSON response containing information about the update, including:
        - A success message and details of the new round if the operation is successful.
        - An error message with an appropriate HTTP status code if the operation fails,
          such as when there are no unallocated players or the league does not exist.

    Raises:
        ValueError: If the league does not have unallocated players or if the league_id does not correspond to an existing league.
    """
    return api_old.startRound(req)



