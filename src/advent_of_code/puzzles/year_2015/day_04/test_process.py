import pytest

from advent_of_code.puzzles.year_2015.day_04 import process


@pytest.mark.parametrize(
    "secret_key,number",
    [
        ("abcdef", 609043),
        ("pqrstuv", 1048970),
    ],
)
def test_md5_search(secret_key: str, number: int) -> None:
    assert process.md5_search(secret_key, prefix="00000") == number
