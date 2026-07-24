import pytest

from advent_of_code.puzzles.year_2016.day_17 import process


@pytest.mark.parametrize(
    "passcode, shortest_path, longest_path_length",
    [
        ("hijkl", None, None),
        ("ihgpwlah", "DDRRRD", 370),
        ("kglvqrro", "DDUDRLRRUDRD", 492),
        ("ulqzkmiv", "DRURDRUDDLLDLUURRDULRLDUUDDDRR", 830),
    ],
)
def test_find_vault(
    passcode: str, shortest_path: str | None, longest_path_length: int | None
) -> None:
    assert process.find_vault(passcode) == (shortest_path, longest_path_length)
