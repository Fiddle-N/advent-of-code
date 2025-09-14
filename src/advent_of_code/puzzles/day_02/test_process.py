from advent_of_code.puzzles.day_02 import process


def test():
    input_str = """\
1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc
"""
    assert process.process(input_str) == (2, 1)