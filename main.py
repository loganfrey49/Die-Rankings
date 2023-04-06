from tracking import Tracking
from game import Game
import random

def test():
    filename = "die_rankings.txt"
    tracking = Tracking(filename)
    tracking.load_data()

    for i in range(1000):

        name_choices = ["Ben", "Mitch", "Logan", "Andy", "Mac", "Colin", "Alex", "Ryan"]
        random_names = random.sample(name_choices, 4)

        team1_player1 = random_names[0]
        team1_player2 = random_names[1]
        team2_player1 = random_names[2]
        team2_player2 = random_names[3]
        
        team1 = tracking.get_team(tracking.get_player(team1_player1), tracking.get_player(team1_player2))
        team2 = tracking.get_team(tracking.get_player(team2_player1), tracking.get_player(team2_player2))

        score1, score2 = 0, 0

        if random.randint(0,1) == 1:
            score1 = 11
            score2 = random.randint(0,score1-2)
        else:
            score2 = 11
            score1 = random.randint(0,score2-2)


        game = Game(team1, team2, [int(score1), int(score2)])

        tracking.update_data(game)
      

def main():
    filename = "die_rankings.txt"
    tracking = Tracking(filename)
    tracking.load_data()

    while True:
       
        team1_player1 = input("Team 1 Player 1: ")
        team1_player2 = input("Team 1 Player 2: ")
        team2_player1 = input("Team 2 Player 1: ")
        team2_player2 = input("Team 2 Player 2: ")

        team1 = tracking.get_team(tracking.get_player(team1_player1), tracking.get_player(team1_player2))
        team2 = tracking.get_team(tracking.get_player(team2_player1), tracking.get_player(team2_player2))
        
        score1 = input("Team 1 Score: ")
        score2 = input("Team 2 Score: ")
       
        game = Game(team1, team2, [int(score1), int(score2)])

        tracking.update_data(game)
        
        tracking.display_data()
        
        play_again = input("Play another game? (y/n): ")
        if play_again.lower() != 'y':
            break

     

if __name__ == "__main__":
    main()