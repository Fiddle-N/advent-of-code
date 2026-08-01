from advent_of_code.puzzles.year_2017.day_06 import process


def test_redistribute_1() -> None:
    memory = [0, 2, 7, 0]
    _, cycles = process.redistribute(memory)
    assert cycles == 5


def test_redistribute_2() -> None:
    memory = [2, 4, 1, 2]
    _, cycles = process.redistribute(memory)
    assert cycles == 4
