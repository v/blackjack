import random

from dealer import Dealer
from deck import Deck
from player import Player

class Game():
    def __init__(self):
        self.deck = Deck()

        self.players = []

        while True:
            try:
                num_players = int(raw_input('Enter number of players (1-6): '))
            except ValueError:
                continue

            if num_players < 1 or num_players > 6:
                print "Invalid number of players"
                continue

            for i in range(num_players):
                name = raw_input('Enter name of player %d: ' % (i + 1))
                bankroll = random.choice(range(100, 1001, 100))

                self.players.append(Player(name, bankroll))

                print "Welcome %s, you have a starting bankroll of $%s" % (name, bankroll)
            break


        self.dealer = Dealer()

    def start_round(self):
        """ place bets
            deal cards
            print cards """

        for player in self.players:
            if player.bankroll > 0:
                while True:
                    try:
                        player.bet = int(raw_input("%s: Your bankroll is $%s. Enter your bet: " % (player.name, player.bankroll)))
                    except ValueError:
                        continue

                    if player.bet <= 0:
                        # abort the game.
                        player.bet = 0
                        break

                    if player.bet <= player.bankroll:
                        break

                    print "Your bet cannot be larger than %s" % (player.bankroll)
            else:
                print "%s you have no more bankroll" % (player.name)


        for i in range(2):
            for player in self.players:
                if player.bet:
                    player.hand.cards.append(self.deck.draw())

            self.dealer.hand.cards.append(self.deck.draw())

        for player in self.players:
            if player.bet:
                print "%s - $%s bet: %s" % (player.name, player.bet, player.hand)

        print "Dealer - %s, [face down card]" % (self.dealer.hand.cards[0])


    def play_round(self):
        """ play out each player & dealer's hand.
            give out rewards. """

        for player in self.players:
            while player.bet and not player.is_bust():
                move = player.play_hand(self.dealer.hand.cards[0])

                if move in ['hit', 'double']:
                    if move == 'double':
                        if len(player.hand.cards) != 2:
                            print 'You cannot double now!'
                            continue

                        if player.bankroll < 2 * player.bet:
                            print '%s, your bankroll was too small, so you doubled for $%s' % (player.name, player.bankroll - player.bet)

                            player.bet += player.bankroll - player.bet
                        else:
                            player.bet *= 2

                    card = self.deck.draw()
                    player.hand.cards.append(card)

                    print "%s drew a %s." % (player.name, card)

                    if player.is_bust():
                        player.bankroll -= player.bet
                        self.dealer.bankroll += player.bet

                        player.bet = 0

                        print "Sorry %s, you busted! %s . Your bankroll is now $%s" % (player.name, player.hand, player.bankroll)
                        break



                elif move == 'stand':
                    break

                print "%s - $%s bet: %s" % (player.name, player.bet, player.hand)

                # you only get one card on a double.
                if move == 'double':
                    break

        print "Dealer reveals - %s" % (self.dealer.hand)

        while not self.dealer.is_bust():
            move = self.dealer.play_hand()

            if move == 'hit':
                card = self.deck.draw()
                self.dealer.hand.cards.append(card)
                print "Dealer drew a %s." % (card)
            elif move == 'stand':
                break

            print "Dealer - %s" % (self.dealer.hand)

        if self.dealer.is_bust():
            print "The dealer busted!"
            for player in self.players:
                if player.bet:
                    player.bankroll += player.bet
                    self.dealer.bankroll -= player.bet

                    print "%s wins $%s!" % (player.name, player.bet)

        else:
            for player in self.players:
                if player.bet:
                    if player.hand.value() > self.dealer.hand.value():
                        print "%s wins $%s!" % (player.name, player.bet)
                        player.bankroll += player.bet
                        self.dealer.bankroll -= player.bet

                    elif player.hand.value() < self.dealer.hand.value():
                        print "%s loses $%s." % (player.name, player.bet)
                        player.bankroll -= player.bet
                        self.dealer.bankroll += player.bet
                    else:
                        print "%s splits with the dealer." % (player.name)

    def end_round(self):
        """ reset player bets, cards and check if game continues """
        # reset round.
        for player in self.players:
            player.bet = 0
            player.hand.cards = []

        self.dealer.hand.cards = []


        while True:
            move = raw_input('Keep Going? (y/n): ').lower()

            if move.startswith('y'):
                return True
            elif move.startswith('n'):
                return False


def main():
    print ">>> Welcome to V's Blackjack Table. Advice is given out for free <<< \n"

    game = Game()

    while True:
        game.start_round()
        game.play_round()
        keep_going = game.end_round()

        if not keep_going:
            break
    print "\n>>> Thanks for playing at V\'s Casino! <<<"


if __name__ == '__main__':
    main()
