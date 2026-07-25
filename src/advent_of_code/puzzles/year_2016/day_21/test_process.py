from advent_of_code.puzzles.year_2016.day_21 import process


def test_scramble():
    instrs = process.parse_instrs("""\
swap position 4 with position 0
swap letter d with letter b
reverse positions 0 through 4
rotate left 1 step
move position 1 to position 4
move position 3 to position 0
rotate based on position of letter b
rotate based on position of letter d""")
    assert process.scramble(password="abcde", instrs=instrs) == "decab"
