from advent_of_code.puzzles.year_2017.day_08 import process


def test_run_instrs() -> None:
    instrs = process.parse_instrs("""\
b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10""")
    assert process.run_instrs(instrs) == (1, 10)
