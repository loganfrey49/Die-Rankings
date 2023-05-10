from player import Player
from team import Team
from game import Game
import app
import math

players = []
teams = []
games = []

def load_data(game_history):

    # Sort the game_history by timestamp from earliest to latest
    game_history = sorted(game_history, key=lambda x: x['timestamp'])

    for game in game_history:
        team1 = get_team(get_player(game['team1_player1']), get_player(game['team1_player2']))
        team2 = get_team(get_player(game['team2_player1']), get_player(game['team2_player2']))
        game = Game(team1, team2, [int(game['team1_score']), int(game['team2_score'])])
        games.append(game)

def update_data():
    for game in games:
        team1 = game.team1
        team2 = game.team2

        winner = team1
        index_winner, index_loser = 0, 1
        loser = team2

        if game.score[0] < game.score[1]:
            winner = team2
            loser = team1
            index_winner, index_loser = 1, 0

        winner_elo = (winner.player1.elo + winner.player2.elo) / 2
        loser_elo = (loser.player1.elo + loser.player2.elo) / 2
        elo_result_winner, elo_result_loser = elo_calculation(winner_elo, loser_elo, game.score[index_winner], game.score[index_loser])
        winner.add_game()
        winner.add_win()
        loser.add_game()
        winner.player1.add_elo_game(elo_result_winner)
        winner.player2.add_elo_game(elo_result_winner)
        loser.player1.add_elo_game(elo_result_loser)
        loser.player2.add_elo_game(elo_result_loser)

    for player in players:
        player.calculate_elo()

    for team in teams:
        team.calculate_elo()

def elo_calculation(winner_elo, loser_elo, winner_score, loser_score):
    r = loser_score / (winner_score - 1)
    # rating diff
    x = 125 + 475 * math.sin(min(1, ((1 - r) / 0.5)) * 0.4 * math.pi) / math.sin(0.4 * math.pi)
    winner_result_elo = loser_elo + x
    loser_result_elo = winner_elo - x
    return winner_result_elo, loser_result_elo


def get_player(name):
    ret = None
    for player in players:
        if player.name == name:
            ret = player
            return ret
    players.append(Player(name))
    return players[-1]

def get_team(player1, player2):
    ret = None
    for team in teams:
        if (team.player1.name == player1.name and team.player2.name == player2.name) or (team.player1.name == player2.name and team.player2.name == player1.name):
            ret = team
            return ret
    teams.append(Team(player1, player2))
    return teams[-1]

def display_data():
    print("\n\nIndividual Rankings:")
    for player in sorted(players, key=lambda x: x.elo, reverse=True):
        print(player)

    print("\n\nTeam Rankings:")
    for team in sorted(teams, key=lambda x: x.wins, reverse=True):
        print(team)

if __name__ == "__main__":
    game_history = app.fetch_game_history_from_firebase()
    load_data(game_history)
    print('Data loaded.')
    choice = 'Y'
    while choice == 'Y':
        update_data()
        display_data()
        choice = input('Update rankings? (Y/N)')
