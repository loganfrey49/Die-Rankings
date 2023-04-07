# Die-Rankings

This web application is a simple ranking system for a dice game, allowing users to track individual and team rankings, game history, and more. The project utilizes Python, Flask, and Firebase for data storage and retrieval.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- Track individual and team rankings based on Elo rating
- Enter game results and update rankings accordingly
- Add new players to the system
- View game history with options to edit or delete games
- Utilizes Firebase for data storage and retrieval

## Installation

1. Clone the repo

```bash
git clone https://github.com/benborszcz/Die-Rankings.git
```

2. Install required packages

```bash
pip install -r requirements.txt
```

3. Set up your Firebase project and generate your own `die-rankings-firebase-admin.json` file. Replace the placeholder file in the project with your own.

4. Run the app locally

```bash
python app.py
```

5. (Optional) If you'd like to use Docker, build and run the Docker image:

```bash
docker build -t die-rankings .
docker run -p 8080:8080 die-rankings
```

## Usage

1. Navigate to the home page and start by adding new players to the system.

2. Enter game results to update rankings and view the individual and team rankings.

3. Browse the game history, with options to edit or delete games.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/someFeature`)
3. Commit your changes (`git commit -m 'Add someFeature'`)
4. Push to the branch (`git push origin feature/someFeature`)
5. Create a new Pull Request

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
