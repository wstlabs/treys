from collections import OrderedDict

# unicode suit chars for pretty printing 
PRETTY = {
    1 : "\u2660", # spades
    2 : "\u2764", # hearts
    4 : "\u2666", # diamonds
    8 : "\u2663"  # clubs
}

# hearts and diamonds
REDS = set([2, 4])
SUITINTS = (1,2,4,8)
RANKS = '23456789TJQKA'

PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]

CHAR_RANK_TO_INT_RANK = OrderedDict(zip(RANKS, range(0,13)))
CHAR_SUIT_TO_INT_SUIT = OrderedDict(zip('shdc',[1,2,4,8]))

class Card ():
    """
    Static class that handles cards. We represent cards as 32-bit integers, so
    there is no object instantiation - they are just ints. Most of the bits are
    used, and have a specific meaning. See below:

                                    Card:

                          bitrank     suit rank   prime
                    +--------+--------+--------+--------+
                    |xxxbbbbb|bbbbbbbb|cdhsrrrr|xxpppppp|
                    +--------+--------+--------+--------+

        1) p = prime number of rank (deuce=2,trey=3,four=5,...,ace=41)
        2) r = rank of card (deuce=0,trey=1,four=2,five=3,...,ace=12)
        3) cdhs = suit of card (bit turned on based on suit of card)
        4) b = bit turned on depending on rank of card
        5) x = unused

    This representation will allow us to do very important things like:
    - Make a unique prime prodcut for each hand
    - Detect flushes
    - Detect straights

    and is also quite performant.
    """

    # the basics

    # converstion from string => int


    @staticmethod
    def make(string):
        """
        Converts Card string to binary integer representation of card, inspired by:

        http://www.suffecool.net/poker/evaluator.html
        """

        rank_char = string[0]
        suit_char = string[1]
        rank_int = CHAR_RANK_TO_INT_RANK[rank_char]
        suit_int = CHAR_SUIT_TO_INT_SUIT[suit_char]
        rank_prime = PRIMES[rank_int]

        bitrank = 1 << rank_int << 16
        suit = suit_int << 12
        rank = rank_int << 8

        return bitrank | suit | rank | rank_prime

def genseq():
    """An iterator which yields freshly-minted cards in (rank,suit) order."""
    for r in RANKS:
        for s in CHAR_SUIT_TO_INT_SUIT.keys():
            yield Card.make(r+s)

_suit2char = 'xshxdxxxc'
def suit2char(suit):
    if suit in SUITINTS:
        return _suit2char[suit]
    else:
        raise ValueError("invalid suit int")

def char2rank(char):
    pass

def char2suit(char):
    pass

def get_rank_int(card):
    return (card >> 8) & 0xF

def get_suit_int(card):
    return (card >> 12) & 0xF

def get_bitrank_int(card):
    return (card >> 16) & 0x1FFF

def get_prime(card):
    return card & 0x3F


def prime_product_from_hand(cards):
    """
    Expects a list of cards in integer form.
    """
    product = 1
    for n in cards:
        product *= (n & 0xFF)
    return product

def prime_product_from_rankbits(rankbits):
    """
    Returns the prime product using the bitrank (b)
    bits of the hand. Each 1 in the sequence is converted
    to the correct prime and multiplied in.

    Params:
        rankbits = a single 32-bit (only 13-bits set) integer representing
                the ranks of 5 _different_ ranked cards
                (5 of 13 bits are set)

    Primarily used for evaulating flushes and straights,
    two occasions where we know the ranks are *ALL* different.

    Assumes that the input is in form (set bits):

                          rankbits
                    +--------+--------+
                    |xxxbbbbb|bbbbbbbb|
                    +--------+--------+

    """
    product = 1
    for i in range(0,13):
        # if the ith bit is set
        if rankbits & (1 << i):
            product *= PRIMES[i]
    return product


# The next two comment lines were from the original 'deuces':
# for mac, linux: http://pypi.python.org/pypi/termcolor
# can use for windows: http://pypi.python.org/pypi/colorama
def _resolve_colored():
    """
    This bit of logic was carved out of the original pretty-print function to
    make the latter a bit more understandable.  The description might be:
    'If termcolor is available, return the impored 'colored' method, whose
    existence is also used as a boolean flag in the calling context as to
    the availability of the termcolor package.'

    Which is a bit muddled, by my tastes.  Basically we need to rethink how
    we manage this colorization business. But for now, let's at least keep
    this try-catch business in a separate method.
    """
    try:
        from termcolor import colored
        return colored
    except ImportError:
        pass

def _pretty_card(card):
    """Expects a card in integer form, and returns a nice string for pretty-printing."""
    suit = get_suit_int(card)
    rank = get_rank_int(card)
    s = PRETTY[suit]
    _colored = _resolve_colored()
    if _colored and suit in REDS:
        s = _colored(s, "red")
    r = RANKS[rank]
    return str(r)+str(s)

def _pretty_list(cards):
    """Expects a list (or iterable) of cards in integer form, and returns a nice string for pretty-printing"""
    return ",".join(_pretty_card(c) for c in cards)

def pretty(x):
    """Returns a nice string representation for pretty printing, expecting either a single card
    (in integer form) or a list of cards."""
    if isinstance(x,int):
        return _pretty_card(x)
    elif isinstance(x,list):
        return _pretty_list(x)
    else:
        raise TypeError("need a single (integer) card, or a list of cards")

def int_to_str(card):
    rank = get_rank_int(card)
    suit = get_suit_int(card)
    return RANKS[rank] + suit2char(suit)


# DEPRECATED
# From the original 'deuces', but never used or tested.
def __int_to_binary(card):
    """
    For debugging purposes. Displays the binary number as a
    human readable string in groups of four digits.
    """
    bstr = bin(card)[2:][::-1] # chop off the 0b and THEN reverse string
    output = list("".join(["0000" +"\t"] * 7) +"0000")

    for i in range(len(bstr)):
        output[i + int(i/4)] = bstr[i]

    # output the string to console
    output.reverse()
    return "".join(output)

# DEPRECATED
# From the original 'deuces', but never used or tested.
def __hand_to_binary(card_strs):
    """
    Expects a list of cards as strings and returns a list
    of integers of same length corresponding to those strings.
    """
    bhand = []
    for c in card_strs:
        bhand.append(Card.make(c))
    return bhand

