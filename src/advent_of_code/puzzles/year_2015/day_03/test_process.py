import pytest

from advent_of_code.common import Directions
from advent_of_code.puzzles.year_2015.day_03 import process


def test_parse_directions() -> None:
    assert process.parse_directions("^>v<") == [
        Directions("^"),
        Directions(">"),
        Directions("v"),
        Directions("<"),
    ]


@pytest.mark.parametrize(
    "directions,visited",
    [
        ([Directions(">")], 2),
        ([Directions("^"), Directions(">"), Directions("v"), Directions("<")], 4),
        (
            [
                Directions("^"),
                Directions("v"),
                Directions("^"),
                Directions("v"),
                Directions("^"),
                Directions("v"),
                Directions("^"),
                Directions("v"),
                Directions("^"),
                Directions("v"),
            ],
            2,
        ),
    ],
)
def test_count_positions_visited(directions: list[Directions], visited: int) -> None:
    assert process.count_positions_visited(directions) == visited


@pytest.mark.parametrize(
    "directions,visited",
    [
        ([Directions("^"), Directions("v")], 3),
        ([Directions("^"), Directions(">"), Directions("v"), Directions("<")], 3),
        (
            [
                Directions("^"),
                Directions("v"),
                Directions("^"),
                Directions("v"),
                Directions("^"),
                Directions("v"),
                Directions("^"),
                Directions("v"),
                Directions("^"),
                Directions("v"),
            ],
            11,
        ),
    ],
)
def test_count_positions_visited_with_alternating_pair(
    directions: list[Directions], visited: int
) -> None:
    assert process.count_positions_visited_with_alternating_pair(directions) == visited
