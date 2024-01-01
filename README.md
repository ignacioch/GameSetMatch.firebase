# GameSetMatch.firebase

## Description

GameSetMatch is a cloud-based application providing an API to manage player profiles and match records for a gaming platform. It allows users to register players, add match records, retrieve player and match details, and delete player profiles or match records.

## Getting Started

### Dependencies

- `Python 3.8` or higher (suggested `Python3.11`)
- Firebase
- Firestore
- Google Cloud Firestore Python library

### Installing

1. Clone the repo and navigate to project directory
2. Setup a virtual environment and activate it

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
```

3. Install required Python dependencies

```bash
pip install -r requirements.txt
```

### Configuration

- Set up a Firebase project and initialize Firestore.
- Configure the Firebase Admin SDK with your project credentials.

## Testing

To run tests, use the following command:

```bash
pytest
```

Ensure you have the test dependencies installed(step 3 above) and Firebase emulators running if necessary. To start the emulator run : 

```bash
firebase emulators:start --project gamesetmatch-ef350
```

## Example requests


- Register a Player

```bash
curl -X POST [API_ENDPOINT]/registerPlayer -H "Content-Type: application/json" -d '{"name": "John Doe", "email": "john@example.com", "DOB": "1990-01-01", "level": "beginner"}'
```

- Add a Match
```bash
curl -X POST [API_ENDPOINT]/addMatch -H "Content-Type: application/json" -d '{"player_a_id": "1", "player_b_id": "2", "score": "6-3, 6-4", "date": "2023-03-28", "location": "Court 1"}'
```

- Get Player Details
```bash
curl -X POST [API_ENDPOINT]/getPlayerDetails -H "Content-Type: application/json" -d '{"player_id": "1"}'
```

- Delete a Player

```bash
curl -X POST [API_ENDPOINT]/deletePlayer -H "Content-Type: application/json" -d '{"player_id": "1"}'
```

- Delete a Match
```bash
curl -X POST [API_ENDPOINT]/deleteMatch -H "Content-Type: application/json" -d '{"match_id": "1"}'
```

## Deployment

Make your changes and then run :

```bash
firebase deploy --only functions
```

Once your functions are being deployed - you can send `curl` requests. For those to be publicly available though, you need to go on [Google Cloud Console](https://console.cloud.google.com/functions/list?env=gen2&project=gamesetmatch-ef350&tab=source) > Permissions > and add `allUsers` and `Cloud Function Invoker`.

