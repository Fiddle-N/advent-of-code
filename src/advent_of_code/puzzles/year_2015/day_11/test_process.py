import pytest

from advent_of_code.puzzles.year_2015.day_11 import process


@pytest.mark.parametrize(
    "input_password, output",
    [
        ("aaaaaaaa", "aaaaaaab"),
        ("aaaaaaaz", "aaaaaaba"),
        ("aaaaaaba", "aaaaaabb"),
        ("aaaaaczz", "aaaaadaa"),
        ("azzzzzzz", "baaaaaaa"),
        ("zzzzzzzy", "zzzzzzzz"),
    ],
)
def test_cycle_password(input_password: str, output: str) -> None:
    password_gen = process.cycle_password(input_password)
    assert next(password_gen) == output


def test_cycle_password_doesnt_cycle_past_8_chars() -> None:
    password_gen = process.cycle_password("zzzzzzzz")
    with pytest.raises(StopIteration):
        next(password_gen)


@pytest.mark.parametrize(
    "input_password, exp_output",
    [
        ("abcdefgh", "abcdffaa"),
        ("ghijklmn", "ghjaabcc"),
    ],
)
def test_next_valid_password(input_password: str, exp_output: str) -> None:
    output = process.next_valid_password(input_password)
    assert output == exp_output
