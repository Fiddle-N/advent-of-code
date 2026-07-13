import pytest

from advent_of_code.common import CardinalDirection
from advent_of_code.puzzles.year_2015.day_03 import process


def test_parse_directions() -> None:
    assert process.parse_directions("^>v<") == [
        CardinalDirection("^"),
        CardinalDirection(">"),
        CardinalDirection("v"),
        CardinalDirection("<"),
    ]


@pytest.mark.parametrize(
    "directions,visited",
    [
        ([CardinalDirection(">")], 2),
        (
            [
                CardinalDirection("^"),
                CardinalDirection(">"),
                CardinalDirection("v"),
                CardinalDirection("<"),
            ],
            4,
        ),
        (
            [
                CardinalDirection("^"),
                CardinalDirection("v"),
                CardinalDirection("^"),
                CardinalDirection("v"),
                CardinalDirection("^"),
                CardinalDirection("v"),
                CardinalDirection("^"),
                CardinalDirection("v"),
                CardinalDirection("^"),
                CardinalDirection("v"),
            ],
            2,
        ),
    ],
)
def test_count_positions_visited(
    directions: list[CardinalDirection], visited: int
) -> None:
    assert process.count_positions_visited(directions) == visited


@pytest.mark.parametrize(
    "directions,visited",
    [
        ([CardinalDirection("^"), CardinalDirection("v")], 3),
        (
            [
                CardinalDirection("^"),
                CardinalDirection(">"),
                CardinalDirection("v"),
                CardinalDirection("<"),
            ],
            3,
        ),
        (
            [
                CardinalDirection("^"),
                CardinalDirection("v"),
                CardinalDirection("^"),
                CardinalDirection("v"),
                CardinalDirection("^"),
                CardinalDirection("v"),
                CardinalDirection("^"),
                CardinalDirection("v"),
                CardinalDirection("^"),
                CardinalDirection("v"),
            ],
            11,
        ),
    ],
)
def test_count_positions_visited_with_alternating_pair(
    directions: list[CardinalDirection], visited: int
) -> None:
    assert process.count_positions_visited_with_alternating_pair(directions) == visited
