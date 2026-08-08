from advent_of_code.puzzles.year_2017.day_16 import process


def test_watch_dance() -> None:
    moves = process.parse("s1,x3/4,pe/b")
    initial_dance, _ = process.dance("abcde", moves)
    assert initial_dance == "baedc"
