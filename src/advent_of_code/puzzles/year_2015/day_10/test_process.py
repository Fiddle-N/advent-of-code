import pytest

from advent_of_code.puzzles.year_2015.day_10 import process


@pytest.mark.parametrize(
    "input_num, output",
    [
        ("1", "11"),
        ("11", "21"),
        ("21", "1211"),
        ("1211", "111221"),
        ("111221", "312211"),
    ],
)
def test_execute_look_and_say(input_num, output) -> None:
    assert process.execute_look_and_say(input_num) == output
