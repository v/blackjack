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


