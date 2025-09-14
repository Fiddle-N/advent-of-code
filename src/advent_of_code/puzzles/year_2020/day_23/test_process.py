from advent_of_code.puzzles.year_2020.day_23 import process


def test_example_10_runs():
    puzzle_input = "389125467"
    crab_cups = process.crab_cups(puzzle_input, move_no=10)
    actual = None
    expected_cups = (
        (2, 8, 9, 1, 5, 4, 6, 7, 3),
        (5, 4, 6, 7, 8, 9, 1, 3, 2),
        (8, 9, 1, 3, 4, 6, 7, 2, 5),
        (4, 6, 7, 9, 1, 3, 2, 5, 8),
        (1, 3, 6, 7, 9, 2, 5, 8, 4),
        (9, 3, 6, 7, 2, 5, 8, 4, 1),
        (2, 5, 8, 3, 6, 7, 4, 1, 9),
        (6, 7, 4, 1, 5, 8, 3, 9, 2),
        (5, 7, 4, 1, 8, 3, 9, 2, 6),
        (8, 3, 7, 4, 1, 9, 2, 6, 5),
    )
    for expected in expected_cups:
        actual = next(crab_cups)
        assert expected == actual
    final_cups = actual
    assert process.calculate_final_labels(final_cups) == "92658374"


def test_example_100_runs():
    puzzle_input = "389125467"
    crab_cups = process.crab_cups(puzzle_input, move_no=100)
    cups = None
    while True:
        try:
            cups = next(crab_cups)
        except StopIteration:
            break
    assert process.calculate_final_labels(cups) == "67384529"
