from advent_of_code.puzzles.year_2018.day_05 import process


def test_react_polymer() -> None:
    polymer = "dabAcCaCBAcCcaDA"
    assert process.react_polymer(polymer) == (10, 4)
