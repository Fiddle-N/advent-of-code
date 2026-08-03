import pytest

from advent_of_code.puzzles.year_2017.day_11 import process


@pytest.mark.parametrize(
    "dir_text,exp_steps",
    [
        ("ne,ne,ne", 3),
        ("ne,ne,sw,sw", 0),
        ("ne,ne,s,s", 2),
        ("se,sw,se,sw,sw", 3),
    ],
)
def test_calculate_knot_hash(dir_text: str, exp_steps) -> None:
    dirs = process.parse_dirs(dir_text)
    steps, _ = process.calculate_fewest_steps(dirs)
    assert steps == exp_steps
