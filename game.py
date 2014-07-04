import random

class Card():
    SUITS_HUMAN = ['clubs', 'spades', 'diamonds', 'hearts']
    FACES_HUMAN = ['ace'] + range(2, 11) + ['jack', 'queen', 'king']

    SUITS = range(0, 4)
    FACES = range(0, 13)



    def __init__(self, suit, face):
        self.suit = suit
        self.face = face

    def is_ace(self):
        return self.face == 1

    def value(self):
        # faces are 0 indexed
        return max(self.face, 9) + 1

    def __str__(self):
        return "%s of %s" % (self.FACES_HUMAN[self.face], self.SUITS_HUMAN[self.suit])

class Deck():
    def __init__(self):
        self.cards = []

        for suit in Card.SUITS:
            for face in Card.FACES:
                self.cards.append(Card(suit, face))

        #random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop()



class Hand():
    def __init__(self):
        self.cards = []

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

    def __str__(self):
        return "Hand: %s. Value: %s" % (','.join(map(str, self.cards)), self.value())

class Player():
    def __init__(self, name, bankroll):
        self.hand = Hand()
        self.bankroll = bankroll
        self.name = name

    def play_hand(self):
        move = raw_input("Hit or stand?")
        return move

    def __str__(self):
        return '%s, $%s' % (self.name, self.bankroll)



class Dealer():
    def __init__(self):
        self.hand = Hand()

    def play_hand(self):
        if self.hand.cards.value() < 17:
            return 'hit'

    def __str__(self):
        return "Dealer"

class Game():
    def __init__(self):
        self.deck = Deck()
        self.players = [Player('V', 100), Dealer()]
        self.dealer = self.players[-1]


    def play_turn(self):
        for i in range(2):
            for player in self.players:
                player.hand.cards.append(self.deck.draw())

                print "Player: %s, %s" % (player, player.hand)


        for player in self.players:
            while player.hand.value() <= 21:
                move = player.play_hand()

                if move == 'hit':
                    player.hand.cards.append(self.deck.draw())
                else:
                    break

                print "Player: %s, Hand: %s" %(player, player.hand)


def main():
    game = Game()
    game.play_turn()


if __name__ == '__main__':
    main()
