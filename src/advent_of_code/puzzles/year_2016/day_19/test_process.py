from advent_of_code.puzzles.year_2016.day_19 import process


def test_simulate_p1():
    assert process.simulate_p1(elves=5) == 3


def test_simulate_p2():
    assert process.simulate_p2(elves=5) == 2
