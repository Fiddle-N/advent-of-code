import itertools

import pytest

from year_2023.day_07 import process


def test_hand_comparisons_with_different_types():
    hands = [
        ('AAAAA', process.Type.FIVE_OF_A_KIND),
        ('AA8AA', process.Type.FOUR_OF_A_KIND),
        ('23332', process.Type.FULL_HOUSE),
        ('TTT98', process.Type.THREE_OF_A_KIND),
        ('23432', process.Type.TWO_PAIR),
        ('A23A4', process.Type.ONE_PAIR),
        ('23456', process.Type.HIGH_CARD),
    ]
    for stronger_hand_input, weaker_hand_input in itertools.pairwise(hands):
        stronger_hand = process.Hand(stronger_hand_input[0])
        assert stronger_hand.type() == stronger_hand_input[1]

        weaker_hand = process.Hand(weaker_hand_input[0])
        assert weaker_hand.type() == weaker_hand_input[1]

        assert stronger_hand != weaker_hand
        assert stronger_hand > weaker_hand
        assert stronger_hand >= weaker_hand
        assert weaker_hand < stronger_hand
        assert weaker_hand <= stronger_hand


@pytest.mark.parametrize(
    'stronger_hand_input, weaker_hand_input, hand_type',
    [
        ('33332', '2AAAA', process.Type.FOUR_OF_A_KIND),
        ('77888', '77788', process.Type.FULL_HOUSE),
    ],
)
def test_hand_comparison_with_same_types(stronger_hand_input, weaker_hand_input, hand_type):
    stronger_hand = process.Hand(stronger_hand_input)
    weaker_hand = process.Hand(weaker_hand_input)
    assert stronger_hand.type() == weaker_hand.type() == hand_type
    assert stronger_hand > weaker_hand


def test_hand_type_with_joker_rule():
    hand = process.Hand('QJJQ2', joker_rule=True)
    assert hand.type() == process.Type.FOUR_OF_A_KIND


def test_all_joker_hand_type():
    hand = process.Hand('JJJJJ', joker_rule=True)
    assert hand.type() == process.Type.FIVE_OF_A_KIND


def test_camel_card_game():
    card_input = """\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""
    game = process.CamelCardGame(card_input)
    ranked = game.ranked()
    assert ranked == {
        1: process.HandBid(process.Hand('32T3K'), 765),
        2: process.HandBid(process.Hand('KTJJT'), 220),
        3: process.HandBid(process.Hand('KK677'), 28),
        4: process.HandBid(process.Hand('T55J5'), 684),
        5: process.HandBid(process.Hand('QQQJA'), 483),
    }
    assert process.total_winnings(ranked) == 6440


def test_camel_card_game_with_joker_rule():
    card_input = """\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""
    game = process.CamelCardGame(card_input, joker_rule=True)
    ranked = game.ranked()
    assert ranked == {
        1: process.HandBid(process.Hand('32T3K', joker_rule=True), 765),
        2: process.HandBid(process.Hand('KK677', joker_rule=True), 28),
        3: process.HandBid(process.Hand('T55J5', joker_rule=True), 684),
        4: process.HandBid(process.Hand('QQQJA', joker_rule=True), 483),
        5: process.HandBid(process.Hand('KTJJT', joker_rule=True), 220),
    }
    assert process.total_winnings(ranked) == 5905
