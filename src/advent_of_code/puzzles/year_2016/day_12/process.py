from advent_of_code.common import read_file, timed_run
from advent_of_code.puzzles.year_2016 import assembunny


def run():
    raw_instrs = read_file()
    instrs = assembunny.parse(raw_instrs)

    init_regs = {"a": 0, "b": 0, "c": 0, "d": 0}
    regs = assembunny.run(init_regs, instrs)
    print(regs["a"])

    init_regs = {"a": 0, "b": 0, "c": 1, "d": 0}
    regs = assembunny.run(init_regs, instrs)
    print(regs["a"])


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
