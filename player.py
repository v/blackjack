from hand import Hand
from strategy import basic_strategy

class Player():
    def __init__(self, name, bankroll):
        self.hand = Hand()
        self.bankroll = bankroll
        self.name = name
        self.bet = 0

    def play_hand(self, dealer_card):
        while True:
            recommend = basic_strategy(self.hand.value(), dealer_card.value(), self.hand.is_soft())

            if len(self.hand.cards) == 2:
                move = raw_input("%s: %s - hit/stand/double? (we recommend %s) " % (self.name, self.hand, recommend)).lower()
            else:
                # for simplicity. This is not true for soft 18.
                if recommend == 'double':
                    recommend = 'hit'

                move = raw_input("%s: %s - hit/stand? (we recommend %s) " % (self.name, self.hand, recommend)).lower()

            if move.startswith('h'):
                return 'hit'
            elif move.startswith('s'):
                return 'stand'
            elif move.startswith('d'):
                return 'double'

            print "Invalid move"

    def __str__(self):
        return '(%s, $%s)' % (self.name, self.bankroll)

    def is_bust(self):
        return self.hand.value() > 21



