from itertools import count, islice

from advent_of_code.common import read_file, timed_run
from advent_of_code.puzzles.year_2016 import assembunny


def run():
    raw_instrs = read_file()
    instrs = assembunny.parse(raw_instrs)

    init_regs = {"a": 0, "b": 0, "c": 0, "d": 0}
    for a_val in count(start=1):
        regs = init_regs.copy()
        regs["a"] = a_val

        # 10 chars is enough to be relatively sure of the pattern
        result = list(islice(assembunny.run(regs, instrs), 10))
        if result == [0, 1, 0, 1, 0, 1, 0, 1, 0, 1]:
            print(a_val)
            return


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
