import pytest

from advent_of_code.puzzles.year_2015.day_01 import process


@pytest.mark.parametrize(
    "directions,floor",
    [
        ("(())", 0),
        ("()()", 0),
        ("(((", 3),
        ("(()(()(", 3),
        ("))(((((", 3),
        ("())", -1),
        ("))(", -1),
        (")))", -3),
        (")())())", -3),
    ],
)
def test_traverse_floors(directions: str, floor: int) -> None:
    assert process.traverse_floors(directions) == floor


@pytest.mark.parametrize(
    "directions,floor",
    [
        (")", 1),
        ("()())", 5),
    ],
)
def test_find_position_that_enters_basement(directions: str, floor: int) -> None:
    assert process.find_position_that_enters_basement(directions) == floor
