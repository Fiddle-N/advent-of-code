from advent_of_code.puzzles.year_2017.day_22 import process


def test_example():
    raw_nodes = """\
..#
#..
..."""
    nodes = process.parse(raw_nodes)
    assert process.simulate(nodes, 70) == 41
    assert process.simulate(nodes, 10000) == 5587


def test_evolved_example():
    raw_nodes = """\
..#
#..
..."""
    nodes = process.parse(raw_nodes)
    assert process.evolved_simulate(nodes, 100) == 26
    assert process.evolved_simulate(nodes, 10000000) == 2511944
