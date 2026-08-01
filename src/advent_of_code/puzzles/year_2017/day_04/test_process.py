import pytest

from advent_of_code.puzzles.year_2017.day_04 import process


@pytest.mark.parametrize(
    "raw_pp,is_valid",
    [
        ("aa bb cc dd ee", True),
        ("aa bb cc dd aa", False),
        ("aa bb cc dd aaa", True),
    ],
)
def test_is_valid_passphrase(raw_pp: str, is_valid: bool) -> None:
    pp = process.parse_passphrase(raw_pp)
    assert process.is_valid_passphrase(pp) == is_valid


@pytest.mark.parametrize(
    "raw_pp,is_valid",
    [
        ("abcde fghij", True),
        ("abcde xyz ecdab", False),
        ("a ab abc abd abf abj", True),
        ("iiii oiii ooii oooi oooo", True),
        ("oiii ioii iioi iiio", False),
    ],
)
def test_is_valid_passphrase_with_added_security(raw_pp: str, is_valid: bool) -> None:
    pp = process.parse_passphrase(raw_pp)
    assert process.is_valid_passphrase(pp, added_security=True) == is_valid
