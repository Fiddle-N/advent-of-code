from advent_of_code.puzzles.year_2025.day_09 import process


def test_resolve_polygon():
    input_ = """\
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3"""
    p = process.Polygon.from_input(input_)
    assert process.resolve(p) == (50, 24)
