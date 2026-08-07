import pytest

from advent_of_code.puzzles.year_2017 import knot_hash


def test_run_knot_hash_round() -> None:
    result = knot_hash.run_knot_hash_round(lengths=[3, 4, 1, 5], marks=5)
    assert result[:2] == [3, 4]


@pytest.mark.parametrize(
    "hash_input,hash_",
    [
        ("", "a2582a3a0e66e6e86e3812dcb672a272"),
        ("AoC 2017", "33efeb34ea91902bb2f59c9920caa6cd"),
        ("1,2,3", "3efbe78a8d82f29979031a4aa0b16a9d"),
        ("1,2,4", "63960835bcdc130f0b66d7ff4f6a5a8e"),
    ],
)
def test_calculate_knot_hash(hash_input: str, hash_: str) -> None:
    hash_result = knot_hash.calculate_knot_hash(hash_input)
    assert hash_result.hexdigest() == hash_
