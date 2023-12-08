import collections
import enum
from dataclasses import dataclass


class Card(enum.Enum):
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

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value


class CardWithJokerRule(enum.Enum):
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

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value


class Type(enum.Enum):
    HIGH_CARD = enum.auto()
    ONE_PAIR = enum.auto()
    TWO_PAIR = enum.auto()
    THREE_OF_A_KIND = enum.auto()
    FULL_HOUSE = enum.auto()
    FOUR_OF_A_KIND = enum.auto()
    FIVE_OF_A_KIND = enum.auto()

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value


class Hand:

    def __init__(self, cards, joker_rule=False) -> None:
        self.cards = cards
        card_count = collections.Counter(self.cards)
        if joker_rule:
            joker_count = card_count[CardWithJokerRule.JOKER]
            card_count_without_joker = {card: count for card, count in card_count.items() if card != CardWithJokerRule.JOKER}
            if card_count_without_joker:
                max_card_count = max(card_count_without_joker.items(), key=lambda entry: entry[1])
                card_count_without_joker[max_card_count[0]] += joker_count
                card_count = card_count_without_joker
        self._count = list(sorted(card_count.values()))

    @classmethod
    def from_string(cls, hand_str, joker_rule=False):
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
        cards = tuple(card_mapping[card] for card in hand_str)
        return cls(cards, joker_rule)

    def __repr__(self):
        return repr(self.cards)

    def _is_five_of_a_kind(self):
        return self._count == [5]

    def _is_four_of_a_kind(self):
        return self._count == [1, 4]

    def _is_full_house(self):
        return self._count == [2, 3]

    def _is_three_of_a_kind(self):
        return self._count == [1, 1, 3]

    def _is_two_pair(self):
        return self._count == [1, 2, 2]

    def _is_one_pair(self):
        return self._count == [1, 1, 1, 2]

    def _is_high_card(self):
        return self._count == [1, 1, 1, 1, 1]

    types = {
        _is_five_of_a_kind: Type.FIVE_OF_A_KIND,
        _is_four_of_a_kind: Type.FOUR_OF_A_KIND,
        _is_full_house: Type.FULL_HOUSE,
        _is_three_of_a_kind: Type.THREE_OF_A_KIND,
        _is_two_pair: Type.TWO_PAIR,
        _is_one_pair: Type.ONE_PAIR,
        _is_high_card: Type.HIGH_CARD,
    }

    def type(self):
        for type_fn, type_ in self.types.items():
            if type_fn(self):
                return type_
        raise ValueError('No types fit the hand')

    def __eq__(self, other):
        return self.cards == other.cards

    def __lt__(self, other):
        return (
            self.cards < other.cards
            if self.type() == other.type()
            else self.type() < other.type()
        )

    def __le__(self, other):
        return (
            self.cards <= other.cards
            if self.type() == other.type()
            else self.type() <= other.type()
        )


@dataclass(frozen=True)
class HandBid:
    hand: Hand
    bid: int


class CamelCardGame:

    def __init__(self, card_input, joker_rule=False):
        self.hand_bids = []
        for hand_bid in card_input.splitlines():
            hand_input, bid_input = hand_bid.split()
            hand = Hand.from_string(hand_input, joker_rule)
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
