from typing import Literal

from advent_of_code.common import read_file, timed_run, parse_ints


def execute_instrs(
    offsets: list[int], mode: Literal["part_1", "part_2"]
) -> tuple[list[int], int]:
    offsets = offsets.copy()
    idx = 0
    steps = 0
    while True:
        offset = offsets[idx]
        meta_offset = -1 if mode == "part_2" and offset >= 3 else 1
        offsets[idx] += meta_offset
        idx += offset
        steps += 1

        if idx < 0 or idx >= len(offsets):
            return (offsets, steps)


def run():
    raw_instrs = read_file()
    instrs = parse_ints(raw_instrs)

    _, steps_p1 = execute_instrs(instrs, mode="part_1")
    print(steps_p1)

    _, steps_p2 = execute_instrs(instrs, mode="part_2")
    print(steps_p2)


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
