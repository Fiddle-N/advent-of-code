from advent_of_code.puzzles.year_2016.day_03 import process


def test_invalid_triangle():
    assert not process.is_triangle((5, 10, 25))


def test_parse_triangles_vertically():
    triangles = process.parse_triangles_vertically("""\
101 301 501
102 302 502
103 303 503
201 401 601
202 402 602
203 403 603""")
    assert triangles == [
        (101, 102, 103),
        (301, 302, 303),
        (501, 502, 503),
        (201, 202, 203),
        (401, 402, 403),
        (601, 602, 603),
    ]
