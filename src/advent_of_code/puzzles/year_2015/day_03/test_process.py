import pytest

from advent_of_code.common import CardinalDirections
from advent_of_code.puzzles.year_2015.day_03 import process


def test_parse_directions() -> None:
    assert process.parse_directions("^>v<") == [
        CardinalDirections("^"),
        CardinalDirections(">"),
        CardinalDirections("v"),
        CardinalDirections("<"),
    ]


@pytest.mark.parametrize(
    "directions,visited",
    [
        ([CardinalDirections(">")], 2),
        (
            [
                CardinalDirections("^"),
                CardinalDirections(">"),
                CardinalDirections("v"),
                CardinalDirections("<"),
            ],
            4,
        ),
        (
            [
                CardinalDirections("^"),
                CardinalDirections("v"),
                CardinalDirections("^"),
                CardinalDirections("v"),
                CardinalDirections("^"),
                CardinalDirections("v"),
                CardinalDirections("^"),
                CardinalDirections("v"),
                CardinalDirections("^"),
                CardinalDirections("v"),
            ],
            2,
        ),
    ],
)
def test_count_positions_visited(
    directions: list[CardinalDirections], visited: int
) -> None:
    assert process.count_positions_visited(directions) == visited


@pytest.mark.parametrize(
    "directions,visited",
    [
        ([CardinalDirections("^"), CardinalDirections("v")], 3),
        (
            [
                CardinalDirections("^"),
                CardinalDirections(">"),
                CardinalDirections("v"),
                CardinalDirections("<"),
            ],
            3,
        ),
        (
            [
                CardinalDirections("^"),
                CardinalDirections("v"),
                CardinalDirections("^"),
                CardinalDirections("v"),
                CardinalDirections("^"),
                CardinalDirections("v"),
                CardinalDirections("^"),
                CardinalDirections("v"),
                CardinalDirections("^"),
                CardinalDirections("v"),
            ],
            11,
        ),
    ],
)
def test_count_positions_visited_with_alternating_pair(
    directions: list[CardinalDirections], visited: int
) -> None:
    assert process.count_positions_visited_with_alternating_pair(directions) == visited
