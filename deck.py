import random

from card import Card

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
        # reshuffle.
        newdeck = Deck()

        self.cards = newdeck.cards
        return self.draw()


