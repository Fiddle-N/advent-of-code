import pytest

from advent_of_code.puzzles.year_2018.day_01 import process


@pytest.mark.parametrize(
    "freqs,result_freq",
    [
        ([1, -2, 3, 1], 3),
        ([1, 1, 1], 3),
        ([1, 1, -2], 0),
        ([-1, -2, -3], -6),
    ],
)
def test_calculate_total_freq(freqs: list[int], result_freq) -> None:
    assert process.calculate_total_freq(freqs) == result_freq


@pytest.mark.parametrize(
    "freqs,result_freq",
    [
        ([1, -2, 3, 1], 2),
        ([1, -1], 0),
        ([3, 3, 4, -2, -4], 10),
        ([-6, 3, 8, 5, -6], 5),
        ([7, 7, -2, -7, -4], 14),
    ],
)
def test_calculate_first_freq_reached_twice(freqs: list[int], result_freq) -> None:
    assert process.calculate_first_freq_reached_twice(freqs) == result_freq
