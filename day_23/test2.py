from day_23 import process2


def test_example_10_runs():
    puzzle_input = '389125467'
    crab_cups = process2.CrabCups(puzzle_input, number_of_cups=None, moves=10)
    result = crab_cups.process()
    assert result == (9, 2)


def test_example_100_runs():
    puzzle_input = '389125467'
    crab_cups = process2.CrabCups(puzzle_input, number_of_cups=None, moves=100)
    result = crab_cups.process()
    assert result == (6, 7)


def test_example_million_cups_10_million_runs():
    puzzle_input = '389125467'
    crab_cups = process2.CrabCups(puzzle_input, number_of_cups=1_000_000, moves=10_000_000)
    result = crab_cups.process()
    assert result == (934001, 159792)
    assert result[0] * result[1] == 149245887792
