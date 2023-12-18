from firebase_admin import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

import logging

MATCHES_COLLECTIONS = "matches"
PLAYERS_COLLECTIONS = "players"

''' 
    Read/write into players collection as a single transaction
'''
@firestore.transactional
def writePlayerToFirestore(transaction,firestore_client, player):
    players_collection = firestore_client.collection(PLAYERS_COLLECTIONS)
    [name,email,dob,level] = player
    #query = players_collection.where(field_path="email", op_string="==", value=email)
    query = players_collection.where(filter=FieldFilter("email","==",email))
    results = query.get(transaction=transaction)
    
    if results:
        raise ValueError(f"Player with email={email} already exists.")

    # Create a new player document with an auto-generated ID
    new_player_ref = players_collection.document()
    new_player_id = new_player_ref.id
    new_player = {"id": new_player_id, "name": name, "email": email, "DOB": dob, "level": level}
    
    # Set the new player data in the transaction
    transaction.set(new_player_ref, new_player)