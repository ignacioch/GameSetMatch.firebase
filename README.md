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

1. Clone the repo and navigate to project directory (or `/functions` if you prefer)
2. Setup a virtual environment and activate it

```bash
cd cli/functions
python -m venv venv
source venv/bin/activate  # On Windows, use venv\Scripts\activate
```

3. Install required Python dependencies

```bash
pip install -r requirements.txt --index-url https://pypi.org/simple
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

For details around the requests, follow the [Wiki](https://github.com/ignacioch/GameSetMatch.firebase/wiki/Requests)


## Deployment

Make your changes and then run :

```bash
firebase deploy --only functions
```

Once your functions are being deployed - you can send `curl` requests. For those to be publicly available though, you need to go on [Google Cloud Console](https://console.cloud.google.com/functions/list?env=gen2&project=gamesetmatch-ef350&tab=source) > Permissions > and add `allUsers` and `Cloud Function Invoker`.

