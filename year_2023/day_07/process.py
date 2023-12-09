import collections
import enum
import operator
from dataclasses import dataclass


class OrderedEnum(enum.Enum):
    """
    OrderedEnum recipe based on the recipe from python.org
    """

    def _comp(self, other, comp_fn):
        if self.__class__ is other.__class__:
            return comp_fn(self.value, other.value)
        return NotImplemented

    def __ge__(self, other):
        return self._comp(other, comp_fn=operator.ge)

    def __gt__(self, other):
        return self._comp(other, comp_fn=operator.gt)

    def __le__(self, other):
        return self._comp(other, comp_fn=operator.le)

    def __lt__(self, other):
        return self._comp(other, comp_fn=operator.lt)


class Card(OrderedEnum):
    ACE = 14
    KING = 13
    QUEEN = 12
    JACK = 11
    TEN = 10
    NINE = 9
    EIGHT = 8
    SEVEN = 7
    SIX = 6
    FIVE = 5
    FOUR = 4
    THREE = 3
    TWO = 2


class CardWithJokerRule(OrderedEnum):
    ACE = 14
    KING = 13
    QUEEN = 12
    TEN = 10
    NINE = 9
    EIGHT = 8
    SEVEN = 7
    SIX = 6
    FIVE = 5
    FOUR = 4
    THREE = 3
    TWO = 2
    JOKER = 1


class Type(OrderedEnum):
    HIGH_CARD = enum.auto()
    ONE_PAIR = enum.auto()
    TWO_PAIR = enum.auto()
    THREE_OF_A_KIND = enum.auto()
    FULL_HOUSE = enum.auto()
    FOUR_OF_A_KIND = enum.auto()
    FIVE_OF_A_KIND = enum.auto()


class Hand:

    def __init__(self, cards_str, joker_rule=False) -> None:
        self.joker_rule = joker_rule
        card_cls = CardWithJokerRule if joker_rule else Card
        card_mapping = {
            'A': card_cls.ACE,
            'K': card_cls.KING,
            'Q': card_cls.QUEEN,
            'T': card_cls.TEN,
            '9': card_cls.NINE,
            '8': card_cls.EIGHT,
            '7': card_cls.SEVEN,
            '6': card_cls.SIX,
            '5': card_cls.FIVE,
            '4': card_cls.FOUR,
            '3': card_cls.THREE,
            '2': card_cls.TWO,
            'J': CardWithJokerRule.JOKER if joker_rule else Card.JACK
        }
        self.cards = tuple(card_mapping[card] for card in cards_str)

    def __repr__(self):
        return repr(self.cards)

    def type(self):
        card_count = collections.Counter(self.cards)

        if self.joker_rule:
            joker_count = card_count[CardWithJokerRule.JOKER]
            card_count_without_joker = {
                card: count for card, count in card_count.items() if card != CardWithJokerRule.JOKER
            }
            if card_count_without_joker:
                max_card_count = max(card_count_without_joker.items(), key=lambda entry: entry[1])
                card_count_without_joker[max_card_count[0]] += joker_count
                card_count = card_count_without_joker

        counts = list(sorted(card_count.values()))

        match counts:
            case [5]:
                return Type.FIVE_OF_A_KIND
            case [1, 4]:
                return Type.FOUR_OF_A_KIND
            case [2, 3]:
                return Type.FULL_HOUSE
            case [1, 1, 3]:
                return Type.THREE_OF_A_KIND
            case [1, 2, 2]:
                return Type.TWO_PAIR
            case [1, 1, 1, 2]:
                return Type.ONE_PAIR
            case [1, 1, 1, 1, 1]:
                return Type.HIGH_CARD
            case _:
                raise ValueError('No types fit the hand')

    def __eq__(self, other):
        return self.cards == other.cards

    def _comp(self, other, comp_fn):
        return (
            comp_fn(self.cards, other.cards)
            if self.type() == other.type()
            else comp_fn(self.type(), other.type())
        )

    def __ge__(self, other):
        return self._comp(other, comp_fn=operator.ge)

    def __gt__(self, other):
        return self._comp(other, comp_fn=operator.gt)

    def __le__(self, other):
        return self._comp(other, comp_fn=operator.le)

    def __lt__(self, other):
        return self._comp(other, comp_fn=operator.lt)


@dataclass(frozen=True)
class HandBid:
    hand: Hand
    bid: int


class CamelCardGame:

    def __init__(self, card_input, joker_rule=False):
        self.hand_bids = []
        for hand_bid in card_input.splitlines():
            hand_input, bid_input = hand_bid.split()
            hand = Hand(hand_input, joker_rule)
            self.hand_bids.append(HandBid(hand, int(bid_input)))

    def ranked(self):
        sorted_hand_bids = sorted(self.hand_bids, key=lambda hand_bid: hand_bid.hand)
        return {idx + 1: hand_bid for idx, hand_bid in enumerate(sorted_hand_bids)}


def read_file():
    with open("input.txt") as f:
        return f.read()


def total_winnings(ranked_hand_bids):
    return sum(rank * hand_bid.bid for rank, hand_bid in ranked_hand_bids.items())


def main() -> None:
    camel_card_input = read_file()
    camel_card_game = CamelCardGame(camel_card_input)
    print(
        f"Total winnings after ranking every hand:",
        total_winnings(camel_card_game.ranked()),
    )
    camel_card_game_with_joker_rule = CamelCardGame(camel_card_input, joker_rule=True)
    print(
        f"Total winnings after ranking every hand with joker rule:",
        total_winnings(camel_card_game_with_joker_rule.ranked()),
    )


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
