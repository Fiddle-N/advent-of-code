import pytest

from advent_of_code.puzzles.year_2017.day_01 import process


@pytest.mark.parametrize(
    "seq,result",
    [
        ("1122", 3),
        ("1111", 4),
        ("1234", 0),
        ("91212129", 9),
    ],
)
def test_captcha_part_1(seq: str, result: int) -> None:
    assert process.solve_capcha(seq, mode="part_1") == result


@pytest.mark.parametrize(
    "seq,result",
    [
        ("1212", 6),
        ("1221", 0),
        ("123425", 4),
        ("123123", 12),
        ("12131415", 4),
    ],
)
def test_captcha_part_2(seq: str, result: int) -> None:
    assert process.solve_capcha(seq, mode="part_2") == result
