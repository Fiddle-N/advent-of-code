from advent_of_code.puzzles.year_2017.day_12 import process


def test_calculate_group_info():
    raw_rels = """\
0 <-> 2
1 <-> 1
2 <-> 0, 3, 4
3 <-> 2, 4
4 <-> 2, 3, 6
5 <-> 6
6 <-> 4, 5"""
    rels = process.parse_rels(raw_rels)
    assert process.calculate_group_info(rels) == (6, 2)
