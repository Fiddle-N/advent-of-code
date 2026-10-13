from advent_of_code.puzzles.year_2018.day_06 import process


def test_calculate_regions():
    raw_coords = """\
1, 1
1, 6
8, 3
3, 4
5, 5
8, 9"""
    coords = process.parse(raw_coords)
    assert process.calculate_regions(coords, safe_region_distance=32) == (17, 16)
