from advent_of_code.puzzles.year_2016.day_18 import process


def test_simulate_1():
    row = process.parse_row("..^^.")
    assert process.simulate(row, 3) == 6


def test_simulate_2():
    row = process.parse_row(".^^.^.^^^^")
    assert process.simulate(row, 10) == 38
