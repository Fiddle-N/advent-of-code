from itertools import takewhile

import pytest

from advent_of_code.puzzles.year_2017.day_03 import process


@pytest.mark.parametrize(
    "square,dist",
    [
        (1, 0),
        (12, 3),
        (23, 2),
        (1024, 31),
    ],
)
def test_calculate_dist_to_square(square: int, dist: int) -> None:
    assert process.calculate_dist_to_square(square) == dist


def test_execute_stress_test() -> None:
    assert list(
        takewhile(lambda square: square <= 806, process.execute_stress_test())
    ) == [
        1,
        1,
        2,
        4,
        5,
        10,
        11,
        23,
        25,
        26,
        54,
        57,
        59,
        122,
        133,
        142,
        147,
        304,
        330,
        351,
        362,
        747,
        806,
    ]
