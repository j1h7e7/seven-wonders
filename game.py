from card import *
from player import Player
import random
from player_ai_basic import RandomPlayer

class Game:
    def __init__(self):
        self.players = []
        self.dealer = Deck()
        self.boards = Boards()
        self.hands = []
        self.numplayers = 0

    def add_players(self, *players):
        self.players.extend(players)
        self.numplayers = len(self.players)

    def start_game(self):
        random.shuffle(self.players)

        # assign neighbors
        for i in range(self.numplayers):
            self.players[i].left_neighbor =  self.players[(i-1) % self.numplayers]
            self.players[i].right_neighbor = self.players[(i+1) % self.numplayers]

        # assign boards
        # for now we just give everyone the boring board
        for player in self.players:
            player.board = self.boards.base_board['wonder']
            player.resources = [[self.boards.base_board['starting']]]

    def play_turn(self, turnnum, direction):
        for i in range(self.numplayers):
            self.players[i].play(self.hands[(i+turnnum*direction) % self.numplayers])
        for player in self.players:
            player.resolve_effect()

    def play_age(self, agenum):
        deck = self.dealer.get_deck(self.numplayers, agenum)
        self.hands = [[] for _ in range(self.numplayers)]
        random.shuffle(deck)

        for hand in self.hands:
            for i in range(7): hand.append(deck.pop())

        direction = (1 if agenum == 2 else -1) # I don't remember lmao

        for i in range(6):
            self.play_turn(i, direction)

        self.do_military(agenum)

    def do_military(self, agenum):
        for i in range(self.numplayers):
            for direction in [-1,+1]:
                if self.players[i].swords < self.players[(i+direction) % self.numplayers].swords:
                    self.players[i].military.append(-1)
                if self.players[i].swords > self.players[(i+direction) % self.numplayers].swords:
                    self.players[i].military.append(agenum*2-1)

    def end_game(self):
        return {player.name:player.calculate_victory_points() for player in self.players}

    def run_game(self):
        self.start_game()
        self.play_age(1)
        self.play_age(2)
        self.play_age(3)
        return self.end_game()



if __name__=="__main__":
    game = Game()

    player1 = RandomPlayer("Player 1",True)
    player2 = RandomPlayer("Player 2",True)
    player3 = RandomPlayer("Player 3",True)

    game.add_players(player1,player2,player3)

    game.start_game()
    game.play_age(1)
    game.play_age(2)
    game.play_age(3)
    game.end_game()