#3rd party API imports
from firebase_functions import https_fn
from firebase_admin import firestore, initialize_app
#from firebase_functions import logger
from google.cloud.firestore_v1.base_query import FieldFilter

# python lib imports
from datetime import datetime
import logging
import json
from typing import Dict,Any

app = initialize_app(options={"projectId":"gamesetmatch-ef350"})

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set to DEBUG or INFO as needed

def getPlayerDetails(req: https_fn.Request) -> https_fn.Response:
    request_json = req.get_json()

    player_details = None
    if player_details:
        return https_fn.Response(json.dumps(player_details), status=200)
    else:
        return https_fn.Response("Player not found", status=404)