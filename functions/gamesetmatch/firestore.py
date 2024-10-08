from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

from datetime import datetime
import logging
from typing import List, Dict, Any

#import .logger

from .player import Player
from .match import Match
from .league import League
from .types import MATCHES_COLLECTION,PLAYERS_COLLECTION,LEAGUES_COLLECTION, LeagueFields, PlayerFields, MatchFields

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set to DEBUG or INFO as needed

''' 
    Read/write into players collection as a single transaction
'''
@firestore.transactional
def writePlayerToFirestore(transaction,firestore_client, player:Player):
    players_collection = firestore_client.collection(PLAYERS_COLLECTION)
    #query = players_collection.where(field_path="email", op_string="==", value=email)
    query = players_collection.where(filter=FieldFilter(PlayerFields.EMAIL.value,"==",player.email))
    results = query.get(transaction=transaction)
    
    if results:
        raise ValueError(f"Player with email={player.email} already exists.")

    # Create a new player document with an auto-generated ID
    new_player_ref = players_collection.document()
    player.id = new_player_ref.id  # Update the player's id
    transaction.set(new_player_ref, player.to_dict())

    return player  # Return the updated player object


def getPlayerDetailsFromFirestore(firestore_client, player_id=None, name=None, email=None):
    players_collection = firestore_client.collection(PLAYERS_COLLECTION)
    query = players_collection.limit(1)  # Adjust the limit as needed

    if player_id:
        query = query.where(PlayerFields.ID.value, '==', player_id)
    if name:
        query = query.where(PlayerFields.NAME.value, '==', name)
    if email:
        query = query.where(PlayerFields.EMAIL.value, '==', email)

    results = query.stream()
    for doc in results:
        return doc.to_dict()  # Return the first matching document

    return None  # Return None if no player found


''' 
    Read/write into matches collection as a single transaction
'''
@firestore.transactional
def addMatchToFirestore(transaction, firestore_client, match_info:Match):
        player_a_id = match_info.player_a_id
        player_b_id = match_info.player_b_id
        score = match_info.score
        match_date = match_info.match_date
        location = match_info.location

        match_id = match_info.match_id #optional
        matches_collection = firestore_client.collection(MATCHES_COLLECTION)

        if match_id:
            match_doc = matches_collection.document(match_id).get(transaction=transaction)
            if match_doc.exists:
                # Update only if the score is different
                if match_doc.to_dict().get(MatchFields.SCORE.value) != score:
                    logger.debug(f"Updating score for match {match_id} to {score}")
                    logger.debug(f"New match {match_info.to_dict()}")
                    transaction.update(matches_collection.document(match_id), match_info.to_dict())
            else:
                # If match_id is provided but doesn't exist, create a new match with that ID
                transaction.set(matches_collection.document(match_id), match_info.to_dict())
        else:
            # Logic for adding a new match without a match_id
            # Do I need just that or should I try and find the match with the other parameters?
            new_match_ref = matches_collection.document()
            match_info.match_id = new_match_ref.id
            transaction.set(new_match_ref, match_info.to_dict())
        
        return  match_info

'''
Adds a match to a league. A match is added under groups, onto the correct subgroup.
'''
@firestore.transactional
def addMatchToLeagueFirestore(transaction, firestore_client,match_info: Match, league_id):
    league_ref = firestore_client.collection(LEAGUES_COLLECTION).document(league_id)
    league_doc = league_ref.get(transaction=transaction)

    if not league_doc.exists:
        raise ValueError("League not found")

    league_data = league_doc.to_dict()
    logger.debug(f"Fetched league information {league_data}")
    current_round = league_data["current_round"]
    logger.info(f"league_id={league_id}. Adding match={match_info}  to round={current_round}")
    pass

def deletePlayerFromFirestore(firestore_client, player_id):
    player_ref = firestore_client.collection(PLAYERS_COLLECTION).document(player_id)
    player_ref.delete()

def deleteMatchFromFirestore(firestore_client, match_id):
    match_ref = firestore_client.collection(MATCHES_COLLECTION).document(match_id)
    match_ref.delete()

def getMatchDetailsFromFirestore(firestore_client, match_id=None, player_id=None):
    matches_collection = firestore_client.collection(MATCHES_COLLECTION)
    logger.debug(f"getMatchDetailsFromFirestore:match_id={match_id}:player_id:{player_id}")
    if match_id:
        # Query for a specific match by match_id
        query = matches_collection.where(MatchFields.MATCH_ID.value, '==', match_id)
    elif player_id:
        # Query for matches involving the specified player
        query = matches_collection.where(PlayerFields.PLAYER_A_ID.value, '==', player_id).where(PlayerFields.PLAYER_B_ID.value, '==', player_id)
    else:
        # If no criteria provided, select all matches
        query = matches_collection.order_by(MatchFields.MATCH_DATE.value, direction=firestore.Query.DESCENDING)

    logger.debug(f"Query: {query}")

    results = query.stream()
    matches = [doc.to_dict() for doc in results]
    logger.debug(f"Matches from Firestore: {matches}")

    return matches

def addPlayerToLeagueFirestore(player_id: str, league_id: str) -> Dict[str, Any]:
    firestore_client = firestore.client()

    # Transaction to ensure atomicity of operations
    @firestore.transactional
    def update_in_transaction(transaction, player_ref, league_ref):
        # Check if player exists and update their leagues list
        player_doc = player_ref.get(transaction=transaction)
        if player_doc.exists:
            player_data = player_doc.to_dict()
            player_leagues = player_data.get(LEAGUES_COLLECTION, [])
            if league_id not in player_leagues:
                player_leagues.append(league_id)
                transaction.update(player_ref, {LEAGUES_COLLECTION: player_leagues})
            else:
                raise ValueError(f"Player already in league {league_id}")
        else:
            raise ValueError("Player not found")

        # Update the league's unallocated players
        league_doc = league_ref.get(transaction=transaction)
        if league_doc.exists:
            league_data = league_doc.to_dict()
            unallocated_players = league_data.get(LeagueFields.UNALLOCATED_PLAYERS.value, [])
            if player_id not in unallocated_players:
                unallocated_players.append(player_id)
                transaction.update(league_ref, {LeagueFields.UNALLOCATED_PLAYERS.value: unallocated_players})
            # No error if player is already in unallocatedPlayers
        else:
            raise ValueError("League not found")

    # References to the player and league documents
    player_ref = firestore_client.collection(PLAYERS_COLLECTION).document(player_id)
    league_ref = firestore_client.collection(LEAGUES_COLLECTION).document(league_id)

    # Execute the transaction
    transaction = firestore_client.transaction()
    update_in_transaction(transaction, player_ref, league_ref)

    # Return updated league information
    updated_league_doc = league_ref.get()
    if updated_league_doc.exists:
        return updated_league_doc.to_dict()
    else:
        raise ValueError("Failed to retrieve updated league info")

@firestore.transactional
def createLeagueFirestore(transaction,firestore_client, league:League):
    leagues_collection = firestore_client.collection(LEAGUES_COLLECTION)
    query = leagues_collection.where(filter=FieldFilter(LeagueFields.AREA.value,"==",league.area))
    results = query.get(transaction=transaction)
    
    if results:
        raise ValueError(f"There is already a league for area={player.area})")

    # Create a new league document with an auto-generated ID
    new_league_ref = leagues_collection.document()
    league.league_id = new_league_ref.id # Update the league's id
    transaction.set(new_league_ref, league.to_dict())

    return league

def fetchPendingPlayersForLeague(league_id: str):
    """
    Fetches players waiting to be allocated to groups for the specified league.
    
    Args:
        league_id (str): Unique identifier of the league.
    
    Returns:
        List[Player]: List of unallocated Player objects.
    """
    db = firestore.client()
    league_ref = db.collection(LEAGUES_COLLECTION).document(league_id)
    league_doc = league_ref.get()
    if league_doc.exists:
        unallocated_players_ids = league_doc.to_dict().get(LeagueFields.UNALLOCATED_PLAYERS.value, [])
        players = [fetchPlayerDetails(player_id) for player_id in unallocated_players_ids]  # Implement fetchPlayerDetails
        return players
    else:
        raise ValueError("League not found")

def startRoundInLeagueFirestore(league_id: str, sorted_groups):
    """
    Updates the league with new groups, sets it as running, and increments the current round.
    
    Args:
        league_id (str): Unique identifier of the league.
        sorted_groups (List[List[Player]]): Nested list of player groups.
    
    Returns:
        dict: Updated league information.
    """
    db = firestore.client()
    league_ref = db.collection(LEAGUES_COLLECTION).document(league_id)
    league_doc = league_ref.get()
    
    if not league_doc.exists:
        raise ValueError("League not found")
    
    league_data = league_doc.to_dict()
    league_data[LeagueFields.RUNNING.value] = True
    league_data[LeagueFields.CURRENT_ROUND.value] += 1
    league_data[LeagueFields.GROUPS.value] = {f"group_{i+1}": [player.id for player in group] for i, group in enumerate(sorted_groups)}
    
    league_ref.update(league_data)
    return league_data

def fetch_players_info(player_ids: List[str]) -> List[Dict]:
    """
    Fetches detailed information for each player given their IDs.

    Args:
        player_ids (List[str]): List of player IDs.

    Returns:
        List[Dict]: A list of dictionaries containing player information.
    """
    firestore_client = firestore.client()
    players_collection = firestore_client.collection(PLAYERS_COLLECTION)
    players_info = []

    for player_id in player_ids:
        player_doc = players_collection.document(player_id).get()
        if player_doc.exists:
            player_info = player_doc.to_dict()
            players_info.append(player_info)

    return players_info


