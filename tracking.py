import os
from player import Player
from team import Team
from game import Game


class Tracking:
    def __init__(self, filename = None):
        self.filename = filename
        self.players = []
        self.teams = []

    def load_data(self, game_history):

        self.players = []
        self.teams = []

        for game in game_history:
            team1 = self.get_team(self.get_player(game['team1_player1']), self.get_player(game['team1_player2']))
            team2 = self.get_team(self.get_player(game['team2_player1']), self.get_player(game['team2_player2']))
            game = Game(team1, team2, [int(game['team1_score']), int(game['team2_score'])])
            print(game)
            self.update_data(game)

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
        rating_diff = loser_elo - winner_elo

        """
        for winning_player, losing_player in [(winner.player1, loser.player1), (winner.player2, loser.player2)]:
            expected_outcome = 1 / (1 + 10**(-rating_diff / 100))
            rating_change = int(k_factor * (1 - expected_outcome) * (point_diff / 10))
            winning_player.update_elo(rating_change)
            losing_player.update_elo(-rating_change)
        """
        for winning_player in [winner.player1, winner.player2]:
            expected_outcome = 8 + (rating_diff / 10)
            rating_change = round(expected_outcome + (point_diff / 8))
            winning_player.update_elo(rating_change)
            

        for losing_player in [loser.player1, loser.player2]:
            expected_outcome = -8 - (rating_diff / 10)
            rating_change = round(expected_outcome - (point_diff / 8))
            losing_player.update_elo(rating_change)

        #self.save_data()
        #game.save_data()


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

