import pytest
from unittest.mock import MagicMock,patch
from gamesetmatch.models.player import Player

# Apply the patching for Firebase Admin SDK early using pytest's hooks
def pytest_configure():
    # Patch the Firebase Admin SDK initialization
    patch('firebase_admin.credentials.Certificate', return_value=MagicMock()).start()
    patch('firebase_admin.initialize_app', return_value=MagicMock()).start()
    patch('firebase_admin.firestore.client', return_value=MagicMock()).start()

# Fixture for mocking the Request object
@pytest.fixture
def mock_request():
    mock_request = MagicMock()
    # You can customize 'args' for different tests
    mock_request.args = {}
    return mock_request

# Mock Firestore accessor calls for get_player_by_uid
@pytest.fixture
def mock_get_player_by_uid(mocker):
    return mocker.patch('gamesetmatch.api.get_player_by_uid')