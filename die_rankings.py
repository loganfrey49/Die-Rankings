import os
from player import Player
from team import Team
from game import Game
from game_data import GameData

class DieRankings:
    def __init__(self, filename, games_filename):
        self.filename = filename
        self.games_filename = games_filename
        self.players = {}
        self.teams = {}
        self.game_data = []
    
    def save_game_data(self):
        with open(self.games_filename, 'w') as f:
            for game_data in self.game_data:
                winner_names = ' '.join([player.name for player in game_data.game.winners])
                loser_names = ' '.join([player.name for player in game_data.game.losers])
                winner_score, loser_score = game_data.game.winner_score, game_data.game.loser_score
                elo_changes = ' '.join([f"{player.name}:{change}" for player, change in game_data.elo_changes])
                f.write(f"{winner_names} {winner_score} {loser_names} {loser_score} {elo_changes}\n")

    def load_rankings(self):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    if ',' in line:
                        name1, name2, wins, games = line.strip().split(',')
                        team_key = f"{name1}-{name2}"
                        self.teams[team_key] = Team(Player(name1), Player(name2), int(wins), int(games))
                    else:
                        name, elo = line.strip().split()
                        self.players[name] = Player(name, int(elo))

    def save_rankings(self):
        with open(self.filename, 'w') as f:
            for player in self.players:
                f.write(f"{player.name} {player.elo}\n")
            for team in self.teams.values():
                name1, name2 = [player.name for player in team.players]
                f.write(f"{name1},{name2},{team.wins},{team.games}\n")

    def update_rankings(self, game):
        winners, losers = game.winners, game.losers
        winner_score, loser_score = game.winner_score, game.loser_score

        for name in winners + losers:
            if name not in self.players:
                self.players[name] = Player(name)

        # Update winning team
        team_key_win = '-'.join(sorted([player.name for player in winners]))
        if team_key_win not in self.teams:
            self.teams[team_key_win] = Team(*winners)
        self.teams[team_key_win].add_win()
        self.teams[team_key_win].add_game()

        # Update losing team
        team_key_lose = '-'.join(sorted([player.name for player in losers]))
        if team_key_lose not in self.teams:
            self.teams[team_key_lose] = Team(*losers)
        self.teams[team_key_lose].add_game()

        k_factor = 32
        point_diff = winner_score - loser_score

        for winner, loser in [(winners[0], losers[0]), (winners[1], losers[1])]:
            rating_diff = winner.elo - loser.elo
            expected_outcome = 1 / (1 + 10**(-rating_diff / 400))
            rating_change = int(k_factor * (1 - expected_outcome) * (point_diff / 10))
            winner.update_elo(rating_change)
            loser.update_elo(-rating_change)

        elo_changes = {(winners[0], rating_change), (winners[1], rating_change), (losers[0], -rating_change), (losers[1], -rating_change)}
        
        self.game_data.append(GameData(game, elo_changes))

    def display_rankings(self):
        print("Individual Rankings:")
        sorted_players = sorted(self.players.values(), key=lambda x: x.elo, reverse=True)
        for player in sorted_players:
            print(f"{player.name}: {player.elo}")

        print("\nTeam Rankings:")
        sorted_teams = sorted(self.teams.values(), key=lambda x: x.wins, reverse=True)
        for team in sorted_teams:
            win_pct = round((team.wins / team.games) * 100, 2)
            print(f"{team.players[0].name}-{team.players[1].name}: {team.wins} wins, {team.games} games, {win_pct}% win rate")