import os
from player import Player
from team import Team
from game import Game

class Tracking:
    def __init__(self, filename):
        self.filename = filename
        self.players = []
        self.teams = []

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if ',' in line:
                        name1, name2, wins, games = line.strip().split(',')
                        player1 = self.get_player(name1)
                        player2 = self.get_player(name2)
                        team = Team(player1, player2, int(wins), int(games))
                        self.teams.append(team)
                    else:
                        name, elo = line.strip().split()
                        self.players.append(Player(name, int(elo)))

    def save_data(self):
        with open(self.filename, 'w') as f:
            for player in self.players:
                f.write(f"{player.name} {player.elo}\n")
            for team in self.teams:
                f.write(f"{team.player1.name},{team.player2.name},{team.wins},{team.games}\n")


    def update_data(self, game):
        team1 = game.team1
        team2 = game.team2


        winner = team1
        loser = team2

        if game.score[0] < game.score[1]:
            winner = team2
            loser = team1
          
        winner.add_game()
        winner.add_win()
        loser.add_game()

        k_factor = 32
        point_diff = game.point_difference()

        winner_elo = (winner.player1.elo + winner.player2.elo) / 2
        loser_elo = (loser.player1.elo + loser.player2.elo) / 2
        rating_diff = winner_elo - loser_elo

        for winning_player, losing_player in [(winner.player1, loser.player1), (winner.player2, loser.player2)]:
            expected_outcome = 1 / (1 + 10**(-rating_diff / 400))
            rating_change = int(k_factor * (1 - expected_outcome) * (point_diff / 20))
            winning_player.update_elo(rating_change)
            losing_player.update_elo(-rating_change)


        self.save_data()
        game.save_data()


    def get_player(self, name):
        ret = None
        for player in self.players:
            if player.name == name:
                ret = player
                return ret
        self.players.append(Player(name))
        return self.players[-1]

    def get_team(self, player1, player2):
        ret = None
        for team in self.teams:
            if (team.player1.name == player1.name and team.player2.name == player2.name) or (team.player1.name == player2.name and team.player2.name == player1.name):
                ret = team
                return ret
        self.teams.append(Team(player1, player2))
        return self.teams[-1]

    def display_data(self):
        print("\n\nIndividual Rankings:")
        for player in sorted(self.players, key=lambda x: x.elo, reverse=True):
            print(player)

        print("\n\nTeam Rankings:")
        for team in sorted(self.teams, key=lambda x: x.wins, reverse=True):
            print(team)