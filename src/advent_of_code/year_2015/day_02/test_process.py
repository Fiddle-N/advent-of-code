import pytest

from advent_of_code.year_2015.day_02 import process


def test_parse_dimensions() -> None:
    assert process.parse_box_dimensions("2x3x4") == process.Box(2, 3, 4)


@pytest.mark.parametrize(
    "box,paper_area",
    [
        (process.Box(2, 3, 4), 58),
        # test all side permutations
        (process.Box(1, 1, 10), 43),
        (process.Box(10, 1, 1), 43),
        (process.Box(1, 10, 1), 43),
    ],
)
def test_wrapping_paper(box: process.Box, paper_area: int) -> None:
    assert process.calculate_wrapping_paper(box) == paper_area


@pytest.mark.parametrize(
    "box,ribbon_length",
    [
        (process.Box(2, 3, 4), 34),
        # test all side permutations
        (process.Box(1, 1, 10), 14),
        (process.Box(10, 1, 1), 14),
        (process.Box(1, 10, 1), 14),
    ],
)
def test_ribbon(box: process.Box, ribbon_length: int) -> None:
    assert process.calculate_ribbon(box) == ribbon_length
