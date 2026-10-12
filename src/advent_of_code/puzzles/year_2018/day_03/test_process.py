from advent_of_code.puzzles.year_2018.day_03 import process


def test_calculate_overlaps_and_non_overlapping_id() -> None:
    raw_claims = """\
#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2"""
    claims = process.parse(raw_claims)
    assert process.calculate_overlaps_and_non_overlapping_id(claims) == (4, 3)
