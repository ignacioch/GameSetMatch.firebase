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