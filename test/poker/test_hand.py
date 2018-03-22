from poker.card import Card, Suit, Rank
from poker.hand import PokerHand, HandType


def test_royal_flush():
    cards = {
        Card(Suit.CLUBS, Rank.ACE),
        Card(Suit.CLUBS, Rank.KING),
        Card(Suit.CLUBS, Rank.QUEEN),
        Card(Suit.CLUBS, Rank.JACK),
        Card(Suit.CLUBS, Rank.TEN)
    }

    hand = PokerHand(cards)

    assert hand.type == HandType.ROYAL_FLUSH

def test_straight_flush():
    cards = {
        Card(Suit.SPADES, Rank.THREE),
        Card(Suit.SPADES, Rank.FOUR),
        Card(Suit.SPADES, Rank.FIVE),
        Card(Suit.SPADES, Rank.SIX),
        Card(Suit.SPADES, Rank.SEVEN)
    }

    hand = PokerHand(cards)

    assert hand.type == HandType.STRAIGHT_FLUSH

def test_four_of_a_kind():
    cards = {
        Card(Suit.HEARTS, Rank.TWO),
        Card(Suit.SPADES, Rank.JACK),
        Card(Suit.HEARTS, Rank.JACK),
        Card(Suit.CLUBS, Rank.JACK),
        Card(Suit.DIAMONDS, Rank.JACK)
    }

    hand = PokerHand(cards)

    assert hand.type == HandType.FOUR_OF_A_KIND

def test_full_house():
    cards = {
        Card(Suit.SPADES, Rank.TWO),
        Card(Suit.HEARTS, Rank.TWO),
        Card(Suit.CLUBS, Rank.QUEEN),
        Card(Suit.HEARTS, Rank.QUEEN),
        Card(Suit.SPADES, Rank.QUEEN)
    }

    hand = PokerHand(cards)

    assert hand.type == HandType.FULL_HOUSE

def test_flush():
    cards = {
        Card(Suit.DIAMONDS, Rank.THREE),
        Card(Suit.DIAMONDS, Rank.SIX),
        Card(Suit.DIAMONDS, Rank.NINE),
        Card(Suit.DIAMONDS, Rank.QUEEN),
        Card(Suit.DIAMONDS, Rank.KING),
    }

    hand = PokerHand(cards)

    assert hand.type == HandType.FLUSH

def test_straight():
    cards = {
        Card(Suit.SPADES, Rank.THREE),
        Card(Suit.DIAMONDS, Rank.FOUR),
        Card(Suit.SPADES, Rank.FIVE),
        Card(Suit.HEARTS, Rank.SIX),
        Card(Suit.CLUBS, Rank.SEVEN),
    }

    hand = PokerHand(cards)

    assert hand.type == HandType.STRAIGHT

def test_three_of_a_kind():
    cards = {
        Card(Suit.HEARTS, Rank.FOUR),
        Card(Suit.SPADES, Rank.TWO),
        Card(Suit.HEARTS, Rank.ACE),
        Card(Suit.SPADES, Rank.ACE),
        Card(Suit.DIAMONDS, Rank.ACE),
    }

    hand = PokerHand(cards)

    assert hand.type == HandType.THREE_OF_A_KIND

def test_two_pair():
    cards = {
        Card(Suit.SPADES, Rank.FOUR),
        Card(Suit.DIAMONDS, Rank.EIGHT),
        Card(Suit.HEARTS, Rank.EIGHT),
        Card(Suit.CLUBS, Rank.JACK),
        Card(Suit.SPADES, Rank.JACK),
    }

    hand = PokerHand(cards)

    assert hand.type == HandType.TWO_PAIRS

def test_pair():
    cards = {
        Card(Suit.SPADES, Rank.THREE),
        Card(Suit.CLUBS, Rank.SIX),
        Card(Suit.SPADES, Rank.SEVEN),
        Card(Suit.HEARTS, Rank.QUEEN),
        Card(Suit.DIAMONDS, Rank.QUEEN),
    }

    hand = PokerHand(cards)

    assert hand.type == HandType.PAIR

def test_high_card():
    cards = {
        Card(Suit.SPADES, Rank.FOUR),
        Card(Suit.DIAMONDS, Rank.SEVEN),
        Card(Suit.SPADES, Rank.NINE),
        Card(Suit.HEARTS, Rank.JACK),
        Card(Suit.CLUBS, Rank.KING),
    }

    hand = PokerHand(cards)

    assert hand.type == HandType.HIGH_CARD
