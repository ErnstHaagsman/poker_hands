from collections import Counter, deque
from dataclasses import dataclass
from enum import Enum
from typing import List, Set, Union

from poker.card import Card, RANK_ORDER, Rank


class HandType(Enum):
    ROYAL_FLUSH = 10
    STRAIGHT_FLUSH = 9
    FOUR_OF_A_KIND = 8
    FULL_HOUSE = 7
    FLUSH = 6
    STRAIGHT = 5
    THREE_OF_A_KIND = 4
    TWO_PAIRS = 3
    PAIR = 2
    HIGH_CARD = 1


@dataclass(init=False, order=True)
class PokerHand:
    type: HandType
    cards: List[Card]

    def __init__(self, cards: Set[Card]):
        """
        Takes a list of up to 7 cards, and takes the most valuable 5-card Poker
        hand from those cards.
        """

        ordered_cards = sorted(cards, key=lambda card: card.rank, reverse=True)
        rank_counts = Counter([card.rank for card in cards]).most_common()
        suit_counts = Counter([card.suit for card in cards]).most_common()

        # The hands need to be checked in order from most to least valuable
        # to always get the most valuable result

        # We have a Flush if we have at least 5 cards of the most common
        # type
        is_flush = suit_counts[0][1] >= 5

        # If we have a flush, let's see if we have a royal flush or straight
        # flush
        if is_flush:
            # most_common returns a list of (elem, count) tuples
            flush_suit = suit_counts[0][0]
            flush_cards = [card for card in ordered_cards
                           if card.suit == flush_suit]

            straight = _get_straight(flush_cards)

            if straight:
                # Determine if it's royal
                if straight[0].rank == Rank.ACE:
                    self.type = HandType.ROYAL_FLUSH
                else:
                    self.type = HandType.STRAIGHT_FLUSH
                self.cards = straight
                return

        # Do we have four of a kind?
        is_four = rank_counts[0][1] == 4
        if is_four:
            four_rank = rank_counts[0][0]
            four_cards = [card for card in ordered_cards
                          if card.rank == four_rank]

            four_cards.extend(_get_kickers(ordered_cards, four_cards))
            self.type = HandType.FOUR_OF_A_KIND
            self.cards = four_cards
            return

        # Full house
        has_three = rank_counts[0][1] == 3
        if has_three:
            three_rank = rank_counts[0][0]
            three_cards = [card for card in ordered_cards
                          if card.rank == three_rank]

            has_two = rank_counts[1][1] >= 2
            if has_two:
                two_rank = rank_counts[1][0]
                # There's a (albeit small) chance that there are two possible
                # sets of 2 cards to choose from
                if len(rank_counts) > 2 and rank_counts[2][1] >= 2:
                    if RANK_ORDER.index(two_rank) < rank_counts[2][0]:
                        two_rank = rank_counts[2][0]

                two_cards = [card for card in ordered_cards
                              if card.rank == two_rank]
                three_cards.extend(two_cards)

                self.type = HandType.FULL_HOUSE
                self.cards = three_cards
                return

        if is_flush:
            # If we have a bog-standard flush, wonderful, we already did
            # all the work for the straight and royal flushes
            self.type = HandType.FLUSH
            self.cards = flush_cards
            return

        straight = _get_straight(ordered_cards)
        if straight:
            self.type = HandType.STRAIGHT
            self.cards = straight
            return

        if has_three:
            # We already got the three_cards in the full house logic
            # We just need to get kickers rather than attempt to fill the
            # house

            three_cards.extend(_get_kickers(ordered_cards, three_cards))
            self.type = HandType.THREE_OF_A_KIND
            self.cards = three_cards
            return

        # Pair and two pair
        has_pair = rank_counts[0][1] >= 2
        if has_pair:
            first_rank = rank_counts[0][0]
            pair_cards = [card for card in ordered_cards
                          if card.rank == first_rank]

            # Check for a second pair
            second_pair = rank_counts[1][1] >= 2
            if second_pair:
                second_rank = rank_counts[1][0]
                second_cards = [card for card in ordered_cards
                                if card.rank == second_rank]

                if first_rank > second_rank:
                    pair_cards.extend(second_cards)
                else:
                    second_cards.extend(pair_cards)
                    pair_cards = second_cards
                self.type = HandType.TWO_PAIRS
            else:
                self.type = HandType.PAIR

            pair_cards.extend(_get_kickers(ordered_cards, pair_cards))
            self.cards = pair_cards
            return

        # We've checked all types. If nothing returned yet, we have a high
        # card. Good luck bluffing!
        self.type = HandType.HIGH_CARD
        self.cards = ordered_cards[0:5]




def _get_kickers(cards: List[Card], exclude: List[Card]) -> List[Card]:
    """
    Takes a list of cards, ordered descending by rank.
    Returns the highest cards except the excluded cards, in descending order
    """
    needed_count = 5 - len(exclude)
    kickers = []

    # We need the highest value cards left
    for card in cards:
        if card in exclude:
            continue

        kickers.append(card)
        if len(kickers) == needed_count:
            return kickers


def _get_straight(cards: List[Card]) -> Union[List[Card], None]:
    """
    Takes a list of cards, ordered descending by rank.
    Returns the highest straight in the list of cards. If no straight is
    present, returns None

    This function disregards the suit. If you're looking for a straight
    flush, pass it a list of cards of the desired suit only.

    :return:
    """

    # Let's iterate through the cards, if we find 5 cars in a row with
    # an index one number lower than the last, we have a straight

    # We'll create a deque to hold the straight we're building
    # Put a card in there, append until we have 5 cards
    # But clear the deque if the difference in order from the last card
    # is greater than 1
    # We'll append to the left of the deck, so we can always check the zeroth
    # element
    potential_straight = deque()
    potential_straight.appendleft(cards[0])

    for card in cards[1:]:
        diff = RANK_ORDER.index(potential_straight[0].rank) - \
               RANK_ORDER.index(card.rank)

        if diff == 0:
            # The same rank, ignore this card
            continue
        elif diff == 1:
            # Going down with a step size of 1, like a straight should
            potential_straight.appendleft(card)
        else:
            # Step size bigger than one, clear, and start again
            potential_straight.clear()
            potential_straight.appendleft(card)

        if len(potential_straight) == 5:
            return list(reversed(potential_straight))

    # If we haven't returned a straight, there wasn't any :(
    return None
