# Die Rankings Web App

Die Rankings is a Flask web app that allows users to track rankings of players and teams in a game. Users can enter game results, view individual player rankings, view team rankings, and see the game history with options to edit and delete games.

## Features

- Enter game results
- View individual player rankings
- View team rankings
- View game history with options to edit and delete games

## Technologies

- Python
- Flask
- Firebase Firestore
- Bootstrap 5

## Setup

1. Clone this repository.
```
git clone https://github.com/benborszcz//Die-Rankings.git
```

2. Install the required packages.

```bash
pip install Flask firebase-admin
```

3. Replace the Firebase credentials file.

Replace the `path/to/firebase_credentials.json` in `app.py` with the path to your own Firebase project's credentials JSON file.

4. Run the Flask app.

```bash
python app.py
```

The web app should now be accessible at `http://127.0.0.1:5000/`.

## Deployment

To deploy the Flask app on a platform like Google Cloud, Heroku, or any other platform that supports Python and Flask applications, follow the platform-specific deployment instructions.

## License

This project is open-source and available under the MIT License. See the `LICENSE` file for more information.
