from dataclasses import dataclass
from enum import Enum


class Suit(Enum):
    SPADES = 'spades'
    DIAMONDS = 'diamonds'
    CLUBS = 'clubs'
    HEARTS = 'hearts'

class Rank(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 'T'
    JACK = 'J'
    QUEEN = 'Q'
    KING = 'K'
    ACE = 'A'

    def __gt__(self, other):
        return RANK_ORDER.index(self) > RANK_ORDER.index(other)

    def __lt__(self, other):
        return RANK_ORDER.index(self) < RANK_ORDER.index(other)

    def __ge__(self, other):
        return RANK_ORDER.index(self) >= RANK_ORDER.index(other)

    def __le__(self, other):
        return RANK_ORDER.index(self) <= RANK_ORDER.index(other)

RANK_ORDER = [
    Rank.TWO,
    Rank.THREE,
    Rank.FOUR,
    Rank.FIVE,
    Rank.SIX,
    Rank.SEVEN,
    Rank.EIGHT,
    Rank.NINE,
    Rank.TEN,
    Rank.JACK,
    Rank.QUEEN,
    Rank.KING,
    Rank.ACE
]

@dataclass(frozen=True)
class Card:
    suit: Suit
    rank: Rank
