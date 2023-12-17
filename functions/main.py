# Welcome to Cloud Functions for Firebase for Python!
# To get started, simply uncomment the below code or create your own.
# Deploy with `firebase deploy`

from firebase_functions import https_fn
from firebase_admin import firestore, initialize_app
#from firebase_functions import logger
import logger
from google.cloud.firestore_v1.base_query import FieldFilter

import logging

app = initialize_app(options={"projectId":"gamesetmatch-ef350"})
#
#
# @https_fn.on_request()
# def on_request_example(req: https_fn.Request) -> https_fn.Response:
#     return https_fn.Response("Hello world!")

@https_fn.on_request()
def registerPlayer(req: https_fn.Request) -> https_fn.Response:
    """Take the text parameter passed to this HTTP endpoint and insert it into
    a new document in the messages collection."""
    # Parse JSON data from request body
    request_json = req.get_json()
    logger.debug(f"Incoming request_raw={request_json}")
    if not request_json:
        return https_fn.Response("Invalid request", status=400)
    
    name = request_json["name"]
    email = request_json["email"]
    dob = request_json["DOB"]
    level = request_json["level"]

    logger.info(f"Incoming request={[name, email, dob, level]}")
    
    # Check for missing parameters
    if not all([name, email, dob, level]):
        return https_fn.Response("Required parameters NOT provided", status=400)

    firestore_client: google.cloud.firestore.Client = firestore.client()

    ''' 
        Adding function for read/write into a single transaction
    '''
    @firestore.transactional
    def writePlayerToFirestore(transaction,firestore_client):
        players_collection = firestore_client.collection("players")
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
        
    
    try:
        writePlayerToFirestore(firestore_client.transaction(),firestore_client)
        return https_fn.Response(f"Player {name} added successfully.")
    except ValueError as e:
        return https_fn.Response(str(e), status=400)