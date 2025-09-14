from advent_of_code.puzzles.day_22 import process


def test_deck_with_normal_rules():
    starting_decks = """\
Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10"""
    combat = process.Combat.from_text(starting_decks, mode='normal')
    combat.play_game()
    expected_intermediate_decks = {
        0: ((9, 2, 6, 3, 1), (5, 8, 4, 7, 10)),
        1: ((2, 6, 3, 1, 9, 5), (8, 4, 7, 10)),
        2: ((6, 3, 1, 9, 5), (4, 7, 10, 8, 2)),
        3: ((3, 1, 9, 5, 6, 4), (7, 10, 8, 2)),
        4: ((1, 9, 5, 6, 4), (10, 8, 2, 7, 3)),
        26: ((5, 4, 1), (8, 9, 7, 3, 2, 10, 6)),
        27: ((4, 1), (9, 7, 3, 2, 10, 6, 8, 5)),
        28: ((1,), (7, 3, 2, 10, 6, 8, 5, 9, 4)),
    }
    actual_intermediate_decks = process.Combat.log

    for idx, actual in enumerate(actual_intermediate_decks):
        if (expected := expected_intermediate_decks.get(idx)) is None:
            continue
        assert expected == actual

    assert not combat.player_1.win_state
    assert combat.player_1.score == 0
    assert combat.player_2.win_state
    assert combat.player_2.deck == (3, 2, 10, 6, 8, 5, 9, 4, 7, 1)
    assert combat.player_2.score == 306


def test_deck_with_recursive_rules():
    starting_decks = """\
Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10"""
    combat = process.Combat.from_text(starting_decks, mode='recursive')
    combat.play_game()

    expected_intermediate_decks = [
        ((9, 2, 6, 3, 1), (5, 8, 4, 7, 10)),
        ((2, 6, 3, 1, 9, 5), (8, 4, 7, 10)),
        ((6, 3, 1, 9, 5), (4, 7, 10, 8, 2)),
        ((3, 1, 9, 5, 6, 4), (7, 10, 8, 2)),
        ((1, 9, 5, 6, 4), (10, 8, 2, 7, 3)),
        ((9, 5, 6, 4), (8, 2, 7, 3, 10, 1)),
        ((5, 6, 4, 9, 8), (2, 7, 3, 10, 1)),
        ((6, 4, 9, 8, 5, 2), (7, 3, 10, 1)),
        ((4, 9, 8, 5, 2), (3, 10, 1, 7, 6)),
        ((9, 8, 5, 2), (10, 1, 7)),
        ((8, 5, 2), (1, 7, 10, 9)),
        ((5, 2, 8, 1), (7, 10, 9)),
        ((2, 8, 1), (10, 9, 7, 5)),
        ((8, 1), (9, 7, 5, 10, 2)),
        ((1,), (7, 5, 10, 2, 9, 8)),
        ((9, 8, 5, 2), (10, 1, 7, 6, 3, 4)),
        ((8, 5, 2), (1, 7, 6, 3, 4, 10, 9)),
        ((5, 2, 8, 1), (7, 6, 3, 4, 10, 9)),
        ((2, 8, 1), (6, 3, 4, 10, 9, 7, 5)),
        ((8, 1), (3, 4, 10, 9, 7, 5)),
        ((1, 8, 3), (4, 10, 9, 7, 5)),
        ((8,), (10, 9, 7, 5)),
        ((8, 3), (10, 9, 7, 5, 4, 1)),
        ((3,), (9, 7, 5, 4, 1, 10, 8)),
        ((8, 1), (3, 4, 10, 9, 7, 5, 6, 2)),
        ((1, 8, 3), (4, 10, 9, 7, 5, 6, 2)),
        ((8,), (10, 9, 7, 5)),
        ((8, 3), (10, 9, 7, 5, 6, 2, 4, 1)),
        ((3,), (9, 7, 5, 6, 2, 4, 1, 10, 8)),
    ]
    actual_intermediate_decks = process.Combat.log
    for expected, actual in zip(expected_intermediate_decks, actual_intermediate_decks):
        assert expected == actual

    assert not combat.player_1.win_state
    assert combat.player_1.score == 0
    assert combat.player_2.win_state
    assert combat.player_2.deck == (7, 5, 6, 2, 4, 1, 10, 8, 9, 3)
    assert combat.player_2.score == 291


def test_infinite_looping_deck_results_in_player_1_win():
    starting_decks = """\
Player 1:
43
19

Player 2:
2
29
14"""
    combat = process.Combat.from_text(starting_decks)
    combat.play_game()
    assert combat.player_1.win_state
