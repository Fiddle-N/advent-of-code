from advent_of_code.puzzles.year_2016.day_20 import process


def test_lowest_valid_ip():
    intervals = process.parse_intervals("""\
5-8
0-2
4-7""")
    merged_intervals = process.merge_intervals(intervals)
    assert process.lowest_valid_ip(merged_intervals) == 3
