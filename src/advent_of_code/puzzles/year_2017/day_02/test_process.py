from advent_of_code.puzzles.year_2017.day_02 import process


def test_calculate_checksum() -> None:
    ss = process.parse_ss("""\
5 1 9 5
7 5 3
2 4 6 8""")
    assert process.calculate_checksum(ss) == 18


def test_calculate_evenly_divisible() -> None:
    ss = process.parse_ss("""\
5 9 2 8
9 4 7 3
3 8 6 5""")
    assert process.calculate_evenly_divisible(ss) == 9
