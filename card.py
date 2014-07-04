class Card():
    # these unicode code points are the suits.
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


