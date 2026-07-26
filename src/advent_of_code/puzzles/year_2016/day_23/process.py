"""
2016 Day 23

https://adventofcode.com/2016/day/23

Selective optimisations of the assembunny VM code,
in particular replacing nested INC/DEC + JNZ calls
are required to ensure Part 2 runs in a good runtime.
"""

from more_itertools import consume

from advent_of_code.common import read_file, timed_run
from advent_of_code.puzzles.year_2016 import assembunny


def run():
    raw_instrs = read_file()
    instrs = assembunny.parse(raw_instrs)

    regs = {"a": 7, "b": 0, "c": 0, "d": 0}
    consume(assembunny.run(regs, instrs))
    print(regs["a"])

    regs = {"a": 12, "b": 0, "c": 0, "d": 0}
    consume(assembunny.run(regs, instrs))
    print(regs["a"])


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
