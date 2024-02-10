import gamesetmatch.api as api

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
    return api.getMatchDetails(req)

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
    return api.addMatch(req)

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
    return api.registerPlayer(req)

@https_fn.on_request()
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
    return api.getPlayerDetails(req)


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
    return api.deletePlayer(req)

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
    return api.deleteMatch(req)


# In main.py
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
    return api.addPlayerToLeague(req)

@https_fn.on_request()
def createLeague(req: https_fn.Request) -> https_fn.Response:
    """
    Endpoint to create a league. This is meant to be called for just creating a new League
    """
    return api.createLeague(req)

@https_fn.on_request()
def startARound(req: https_fn.Request) -> https_fn.Response:
    """
    Starts a new round in a league, creating groups from unallocated players.

    Args:
        req (https_fn.Request): The request object containing JSON data with 'league_id'.

    Returns:
        https_fn.Response: A confirmation message upon successful update or an error
        message with an appropriate HTTP status code on failure.
    """
    return api.startARound(req)



