from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

import logging

from player import Player
from match import Match

MATCHES_COLLECTIONS = "matches"
PLAYERS_COLLECTIONS = "players"

''' 
    Read/write into players collection as a single transaction
'''
@firestore.transactional
def writePlayerToFirestore(transaction,firestore_client, player:Player):
    players_collection = firestore_client.collection(PLAYERS_COLLECTIONS)
    #query = players_collection.where(field_path="email", op_string="==", value=email)
    query = players_collection.where(filter=FieldFilter("email","==",player.email))
    results = query.get(transaction=transaction)
    
    if results:
        raise ValueError(f"Player with email={player.email} already exists.")

    # Create a new player document with an auto-generated ID
    new_player_ref = players_collection.document()
    new_player_id = new_player_ref.id
    new_player = {"id": new_player_id, "name": player.name, "email": player.email, "DOB": player.dob, "level": player.level}
    
    # Set the new player data in the transaction
    transaction.set(new_player_ref, new_player)


def getPlayerDetailsFromFirestore(firestore_client, player_id=None, name=None, email=None):
    players_collection = firestore_client.collection(PLAYERS_COLLECTIONS)
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
        matches_collection = firestore_client.collection(MATCHES_COLLECTIONS)

        if match_id:
            match_doc = matches_collection.document(match_id).get(transaction=transaction)
            if match_doc.exists:
                # Update only if the score is different
                if match_doc.to_dict().get("score") != score:
                    transaction.update(matches_collection.document(match_id), {"score": score})
            else:
                # If match_id is provided but doesn't exist, create a new match with that ID
                transaction.set(matches_collection.document(match_id), match_info)
        else:
            # Logic for adding a new match without a match_id
            # Do I need just that or should I try and find the match with the other parameters?
            new_match_ref = matches_collection.document()
            match_info.match_id = new_match_ref.id
            transaction.set(new_match_ref, match_info.to_dict())

            # Check if match already exists
            ###### matches_collection = firestore_client.collection(MATCHES_COLLECTIONS)
            ###### match_query = matches_collection.where("player_a_id", "==", player_a_id)\
            ######                             .where("player_b_id", "==", player_b_id)\
            ######                             .where("date", "==", match_date)\
            ######                             .where("location", "==", location).limit(1)
            ###### match_docs = match_query.get(transaction=transaction)
            ###### if match_docs:
            ######     match_doc = next(iter(match_docs), None)
            ######     if match_doc and match_doc.to_dict().get("score") != score:
            ######         transaction.update(matches_collection.document(match_doc.id), {"score": score})
            ###### else:
            ######     # Create a new document reference with an auto-generated ID
            ######     new_match_ref = matches_collection.document()
            ######     # Add the generated match ID to the match data
            ######     match_info["match_id"] = new_match_ref.id
            ######     # Set the new match data in the transaction
            ######     transaction.set(new_match_ref, match_info)