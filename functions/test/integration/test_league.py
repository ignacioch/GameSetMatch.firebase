import requests
import pytest
from test import utils

# URLs of the Cloud Functions
CREATE_LEAGUE_URL="http://localhost:5001/gamesetmatch-ef350/us-central1/createLeague"

@pytest.mark.integration
@pytest.mark.league
def test_create_league():
    