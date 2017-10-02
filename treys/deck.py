from random import shuffle
from .card import pretty, genseq

class Deck:
    """
    Class representing a deck. The first time we create, we seed the static
    deck with the list of unique card integers. Each object instantiated simply
    makes a copy of this object and shuffles it.
    """
    _FULL_DECK = []

    def __init__(self):
        self.shuffle()

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        return pretty(self.cards)

    def shuffle(self):
        self.cards = Deck.fresh()
        shuffle(self.cards)

    def pick(self):
        if len(self) < 1:
            raise RuntimeError("can't pick from an empty deck")
        return self.cards.pop()

    def draw(self, n=1):
        if n == 1:
            return self.cards.pop(0)
        cards = []
        for i in range(n):
            cards.append(self.pick())
        return cards


    @staticmethod
    def fresh():
        """Returns a newly minted deck, in canonical order."""
        return list(genseq())

