from advent_of_code.puzzles.year_2017.day_14 import process


def test_count_used_squares() -> None:
    used_squares = process.count_used_squares(key="flqrgnkx")
    assert used_squares == (8108, 1242)
