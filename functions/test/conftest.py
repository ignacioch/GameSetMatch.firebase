import pytest
from unittest.mock import MagicMock,patch
from gamesetmatch.models.player import Player

# Apply the patching for Firebase Admin SDK early using pytest's hooks
def pytest_configure():
    # Patch the Firebase Admin SDK initialization
    patch('firebase_admin.credentials.Certificate', return_value=MagicMock()).start()
    patch('firebase_admin.initialize_app', return_value=MagicMock()).start()
    patch('firebase_admin.firestore.client', return_value=MagicMock()).start()

# Mock Firestore accessor calls for get_player_by_uid
@pytest.fixture
def mock_get_player_by_uid(mocker):
    return mocker.patch('gamesetmatch.firestore_accessor.get_player_by_uid')

# Fixture for mocking the Request object
@pytest.fixture
def mock_request():
    mock_request = MagicMock()
    # You can customize 'args' for different tests
    mock_request.args = {}
    return mock_request

# Mock Firestore accessor calls for get_player_document
# Create a real Player object for testing
@pytest.fixture
def test_player():
    player_data = {
        "player_id": "1234",
        "info": {
            "name": "John Doe",
            "email": "john.doe@example.com",
            "profilePictureUrl": "http://example.com/johndoe.jpg",
            "dateOfBirth": "1990-01-01T00:00:00Z"
        },
        "tennis": {
            "singles": {
                "matches": [],
                "leagues": []
            }
        }
    }
    player = Player.from_dict("1234", player_data)
    return player

# Mock Firestore accessor calls for get_player_document to return the real Player object
@pytest.fixture
def mock_get_player_document(mocker, test_player):
    # Mock get_player_document to return the mocked document
    mock = mocker.patch('gamesetmatch.firestore_accessor.get_player_document', return_value=test_player)
    return mock