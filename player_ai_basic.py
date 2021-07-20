from card import *
from player import Player

import random

class RandomPlayer(Player):
    def play(self, hand):
        if self.debug: print(self.name,"recieved the hand:",hand)

        cardtoplay = random.choice(hand)
        hand.remove(cardtoplay)

        if self.can_play_card(cardtoplay):
            self.play_card(cardtoplay)
        elif self.can_upgrade_wonder():
            self.build_wonder()
        else:
            self.sell_card(cardtoplay)

        return

class SellingPlayer(Player):
    def play(self, hand):
        if self.debug: print(self.name,"recieved the hand:",hand)

        cardtoplay = random.choice(hand)
        hand.remove(cardtoplay)
        self.sell_card(cardtoplay)

        return
            
