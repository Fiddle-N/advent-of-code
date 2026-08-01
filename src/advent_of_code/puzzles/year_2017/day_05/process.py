from typing import Literal

from advent_of_code.common import read_file, timed_run, parse_ints


def execute_instrs(offsets: list[int], mode: Literal["part_1", "part_2"]) -> int:
    idx = 0
    steps = 0
    while True:
        offset = offsets[idx]
        meta_offset = -1 if mode == "part_2" and offset >= 3 else 1
        offsets[idx] += meta_offset
        idx += offset
        steps += 1

        if idx < 0 or idx >= len(offsets):
            return steps


def run():
    raw_instrs = read_file()
    instrs = parse_ints(raw_instrs)

    print(execute_instrs(instrs.copy(), mode="part_1"))
    print(execute_instrs(instrs.copy(), mode="part_2"))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
