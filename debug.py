from urllib.request import urlopen
from datetime import datetime
import re
import app

url = "https://die.yhessno.com/game_history"

def scrapeGameData():
    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    pattern = "<td.*?>.*?</td.*?>"
    games_results = re.findall(pattern, html, re.IGNORECASE)
    games_data = []
    for i in range(0, games_results.__len__(), 4):
        timestamp = re.sub("<.*?>", "", games_results[i]) # Remove HTML tags
        team1 = re.sub("<.*?>", "", games_results[i + 1]).split(' ')
        score = re.sub("<.*?>", "", games_results[i + 2]).split(' ')
        team2 = re.sub("<.*?>", "", games_results[i + 3]).split(' ')
        team1_player1, team1_player2 = team1[0], team1[2]
        team2_player1, team2_player2 = team2[0], team2[2]
        team1_score, team2_score = score[0], score[2]
        format = '%Y-%m-%d %H:%M'
        timestamp = datetime.strptime(timestamp, format)
        
        games_data.append({
            'team1_player1': team1_player1,
            'team1_player2': team1_player2,
            'team2_player1': team2_player1,
            'team2_player2': team2_player2,
            'team1_score' : team1_score,
            'team2_score' : team2_score,
            'timestamp': timestamp
        })

    return games_data

if __name__ == "__main__":
    choice = input('(DEBUG) This will scrape game data from the main page and add it to the firestore, continue? (Y/N)')
    if (choice == 'Y'):
        games_data = scrapeGameData()
        print(games_data)
        app.save_games_data_to_firebase(games_data)
    else:
        print('Did not scrape and add data')