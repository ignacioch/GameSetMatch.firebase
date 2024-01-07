import logging
import requests
import pytest

BASE_URL = "http://localhost:5001/gamesetmatch-ef350/us-central1"
ADD_MATCH_URL = f"{BASE_URL}/addMatch"
GET_MATCH_URL = f"{BASE_URL}/getMatchDetails"
DELETE_MATCH_URL = f"{BASE_URL}/deleteMatch"

# Create a logger object
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set the appropriate level

logging.basicConfig(level=logging.DEBUG) # Configuring root logger

# Store the match IDs for cleanup
matches_to_cleanup = []

@pytest.fixture(scope="module", autouse=True)
def cleanup_matches():
    # Setup code (before yield) can be used if needed
    yield
    # Teardown code (after yield)
    for match_id in matches_to_cleanup:
        logger.info(f"Cleaning up test.Deleting {match_id}")
        requests.post(DELETE_MATCH_URL, json={"match_id": match_id})

'''
    Helper functions
'''
def get_match_out_of_match_response(response):
    assert response.status_code == 200
    response_content = response.json()
    logger.info(response_content)
    assert 'match' in response_content  # Ensure the response contains 'match'
    match = response_content['match']
    return match

def add_match():
    match_data = {
        "player_a_id": "player1",
        "player_b_id": "player2",
        "score": "6-3, 6-4",
        "match_date": "2023-03-28",
        "location": "Court 1"
    }
    response = requests.post(ADD_MATCH_URL, json=match_data)
    return get_match_out_of_match_response(response)

def get_all_matches():
    response = requests.get(GET_MATCH_URL)
    assert response.status_code == 200
    return response.json()

def delete_match(match_id):
    response = requests.post(DELETE_MATCH_URL, json={"match_id": match_id})
    assert response.status_code == 200

'''
Adding a test without providing a match_id.
'''
def test_add_new_match_without_match_id():
    match = add_match()
    assert 'match_id' in match # assert match has match_id
    match_id = match['match_id']
    matches_to_cleanup.append(match_id)

'''
Adding a match and updating the score
'''
def test_add_and_update_match():
    # Add a new match
    match = add_match()
    original_score = match['score']

    # Update the score of the added match
    new_score = "6-4, 6-4"
    match["score"] = new_score
    response = requests.post(ADD_MATCH_URL, json=match)
    updated_match = get_match_out_of_match_response(response)
    
    # Verify that the score is updated
    assert updated_match['score'] == new_score
    assert updated_match['score'] != original_score
    for field in updated_match :
        assert field in match
        if field != "score" :
            assert match[field] == updated_match[field]


'''
Get all matches. Add a match. Make sure total matches has increased by one.
Delete the match we added. Make sure match doesn't exist and total matches are back to original.
'''
def test_match_workflow_end_to_end():
    # Get all existing matches
    initial_matches = get_all_matches()
    initial_count = len(initial_matches)
    logger.debug(f"Database has {initial_count} existing matches.")
    # Add a new match
    new_match = add_match()
    new_match_id = new_match["match_id"]
    logger.info(f"Added match: {new_match_id}")

    # Get all matches again, expect one more match
    updated_matches = get_all_matches()
    logger.info(f"Matches after adding: {updated_matches}")
    assert len(updated_matches) == initial_count + 1
    assert any(match["match_id"] == new_match_id for match in updated_matches)

    # Delete the added match
    delete_match(new_match_id)

    # Get all matches again, expect the count to be back to original
    final_matches = get_all_matches()
    assert len(final_matches) == initial_count
    assert all(match["match_id"] != new_match_id for match in final_matches)

# Run the test
if __name__ == "__main__":
    pytest.main()
