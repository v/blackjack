import random, sys

class Card():
    SUITS_HUMAN = [u"\u2660", u"\u2665", u"\u2666", u"\u2663"]
    FACES_HUMAN = ['A'] + range(2, 11) + ['J', 'Q', 'K']

    SUITS = range(0, 4)
    FACES = range(0, 13)

    def __init__(self, suit, face):
        self.suit = suit
        self.face = face

    def is_ace(self):
        return self.face == 0

    def value(self):
        # faces are 0 indexed
        return min(self.face, 9) + 1

    def __unicode__(self):
        return u"%s%s" % (self.FACES_HUMAN[self.face], self.SUITS_HUMAN[self.suit])

    def __str__(self):
        return unicode(self).encode('utf-8')

class Deck():
    def __init__(self):
        self.cards = []

        for suit in Card.SUITS:
            for face in Card.FACES:
                self.cards.append(Card(suit, face))

        random.shuffle(self.cards)

    def draw(self):
        if self.cards:
            return self.cards.pop()
        newdeck = Deck()

        self.cards = newdeck.cards
        return self.draw()


class Hand():
    def __init__(self):
        self.cards = []

    def is_soft(self):
        value = 0
        has_ace = False

        for card in self.cards:
            if card.is_ace():
                has_ace = True

            value += card.value()

        return has_ace and value <= 11

    def value(self):
        value = 0
        has_ace = False

        for card in self.cards:
            value += card.value()

            if card.is_ace():
                has_ace = True

        if has_ace and value <= 11:
            value += 10

        return value

    def __unicode__(self):
        soft = ' soft ' if self.is_soft() else ' '

        return u"[%s] (value:%s%s)" % (', '.join(map(unicode, self.cards)), soft, self.value())

    def __str__(self):
        return unicode(self).encode('utf-8')

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
                move = raw_input("%s: %s - hit/stand/double? (we recommend %s) " % (self.name, self.hand, recommend))
            else:
                # for simplicity. This is not true for soft 18.
                if recommend == 'double':
                    recommend = 'hit'

                move = raw_input("%s: %s - hit/stand? (we recommend %s) " % (self.name, self.hand, recommend))

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

def basic_strategy(player_total, dealer_value, soft):
    """ This is a simple implementation of Blackjack's
        basic strategy. It is used to recommend actions
        for the player. """

    if 4 <= player_total <= 8:
        return 'hit'
    if player_total == 9:
        if dealer_value in [1,2,7,8,9,10]:
            return 'hit'
        return 'double'
    if player_total == 10:
        if dealer_value in [1, 10]:
            return 'hit'
        return 'double'
    if player_total == 11:
        if dealer_value == 1:
            return 'hit'
        return 'double'
    if soft:
        #we only double soft 12 because there's no splitting
        if player_total in [12, 13, 14]:
            if dealer_value in [5, 6]:
                return 'double'
            return 'hit'
        if player_total in [15, 16]:
            if dealer_value in [4, 5, 6]:
                return 'double'
            return 'hit'
        if player_total == 17:
            if dealer_value in [3, 4, 5, 6]:
                return 'double'
            return 'hit'
        if player_total == 18:
            if dealer_value in [3, 4, 5, 6]:
                return 'double'
            if dealer_value in [2, 7, 8]:
                return 'stand'
            return 'hit'
        if player_total >= 19:
            return 'stand'

    else:
        if player_total == 12:
            if dealer_value in [1, 2, 3, 7, 8, 9, 10]:
                return 'hit'
            return 'stand'
        if player_total in [13, 14, 15, 16]:
            if dealer_value in [2, 3, 4, 5, 6]:
                return 'stand'
            return 'hit'

        if player_total >= 17:
            return 'stand'



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
