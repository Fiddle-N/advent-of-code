from more_itertools import consume

from advent_of_code.puzzles.year_2016 import assembunny


def test_assembunny() -> None:
    raw_instrs = """\
cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a"""
    instrs = assembunny.parse(raw_instrs)
    regs = {"a": 0, "b": 0, "c": 0, "d": 0}
    consume(assembunny.run(regs, instrs))
    assert regs["a"] == 3
