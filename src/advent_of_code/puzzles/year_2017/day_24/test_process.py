from advent_of_code.puzzles.year_2017.day_24 import process


def test_example():
    raw_components = """\
0/2
2/2
2/3
3/4
3/5
0/1
10/1
9/10"""
    components = process.parse(raw_components)
    builder = process.BridgeBuild()
    assert builder.build(components) == (31, 19)
