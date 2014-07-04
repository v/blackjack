from hand import Hand
from player import Player


class Dealer(Player):
    def __init__(self):
        self.hand = Hand()
        self.name = "Dealer"
        self.bet = 0
        self.bankroll = 1e7

    def play_hand(self):
        if self.hand.value() < 17:
            return 'hit'
        return 'stand'

    def __str__(self):
        return "Dealer"


