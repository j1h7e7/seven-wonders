from game import Game
from player_ai_basic import *

class Tournament:
    def __init__(self, ais):
        self.ais = ais
        self.scores = {x:0 for x in ais}

    def run_game(self):
        players = [self.ais[name](name) for name in self.ais]
        game = Game()
        game.add_players(*players)

        result = game.run_game()
        for name in self.ais:
            self.scores[name]+=result[name]
    
    def run_tournament(self, n=100):
        for i in range(n):
            if i % int(n/10) == 0: print(i)
            self.run_game()

        for name in self.scores: self.scores[name] /= n

if __name__ == "__main__":
    players = {
        "Random1": RandomPlayer,
        "Random2": RandomPlayer,
        "Random3": RandomPlayer,
        "Random4": RandomPlayer,
        "Random5": RandomPlayer,
        "Random6": RandomPlayer,
        "Random7": RandomPlayer
    }
    
    TO = Tournament(players)
    TO.run_tournament()
    print(TO.scores)