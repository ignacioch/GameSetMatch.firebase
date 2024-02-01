from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

from datetime import datetime
import logging

#import .logger

from .player import Player
from .match import Match

MATCHES_COLLECTION = "matches"
PLAYERS_COLLECTION = "players"
LEAGUES_COLLECTION  = "leagues" 

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set to DEBUG or INFO as needed

''' 
    Read/write into players collection as a single transaction
'''
@firestore.transactional
def writePlayerToFirestore(transaction,firestore_client, player:Player):
    players_collection = firestore_client.collection(PLAYERS_COLLECTION)
    #query = players_collection.where(field_path="email", op_string="==", value=email)
    query = players_collection.where(filter=FieldFilter("email","==",player.email))
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
        query = query.where('id', '==', player_id)
    if name:
        query = query.where('name', '==', name)
    if email:
        query = query.where('email', '==', email)

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
                if match_doc.to_dict().get("score") != score:
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
        query = matches_collection.where('match_id', '==', match_id)
    elif player_id:
        # Query for matches involving the specified player
        query = matches_collection.where('player_a_id', '==', player_id).where('player_b_id', '==', player_id)
    else:
        logger.debug("here")
        # If no criteria provided, select all matches
        query = matches_collection.order_by('match_date', direction=firestore.Query.DESCENDING)

    logger.debug(f"Query: {query}")

    results = query.stream()
    matches = [doc.to_dict() for doc in results]
    logger.debug(f"Matches from Firestore: {matches}")

    return matches

def addPlayerToLeagueFirestore(player_id, league_id):
    firestore_client = firestore.client()

    # Transaction to ensure atomicity of operations
    @firestore.transactional
    def update_in_transaction(transaction, player_ref, league_ref):
        # Check if player exists and update their leagues list
        player_doc = player_ref.get(transaction=transaction)
        if player_doc.exists:
            player_data = player_doc.to_dict()
            player_leagues = player_data.get("leagues", [])
            if league_id not in player_leagues:
                player_leagues.append(league_id)
                transaction.update(player_ref, {"leagues": player_leagues})
            else:
                raise ValueError(f"Player already in league {league_id}")
        else:
            raise ValueError("Player not found")

        # Update the league's unallocated players
        league_doc = league_ref.get(transaction=transaction)
        if league_doc.exists:
            league_data = league_doc.to_dict()
            unallocated_players = league_data.get("unallocatedPlayers", [])
            if player_id not in unallocated_players:
                unallocated_players.append(player_id)
                transaction.update(league_ref, {"unallocatedPlayers": unallocated_players})
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

def createLeagueFirestore(league_name, location, start_date_str, end_date_str):
    firestore_client = firestore.client()
    league_ref = firestore_client.collection("Leagues").document()

    # Convert date strings to datetime.date objects
    start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()

    new_league_data = {
        "league_name": league_name,
        "location": location,
        "running": False,
        "current_round": 0,
        "unallocatedPlayers": [],
        "dates": {
            "start": start_date,
            "end": end_date
        }
    }

    league_ref.set(new_league_data)

    return {**new_league_data, "league_id": league_ref.id}

