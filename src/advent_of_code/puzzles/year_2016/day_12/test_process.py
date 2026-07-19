from advent_of_code.puzzles.year_2016.day_12 import process


def test_run_program() -> None:
    raw_instrs = """\
cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a"""
    instrs = process.parse_instrs(raw_instrs)
    init_regs = {"a": 0, "b": 0, "c": 0, "d": 0}
    regs = process.run_program(init_regs, instrs)
    assert regs["a"] == 42
