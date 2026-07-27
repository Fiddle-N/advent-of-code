from typing import Literal

from advent_of_code.common import read_file, timed_run


def solve_capcha(seq: str, mode: Literal["part_1", "part_2"]):
    offset = (len(seq) // 2) if mode == "part_2" else 1
    total = 0
    for idx, char in enumerate(seq):
        comp_idx = (idx + offset) % len(seq)
        comp_char = seq[comp_idx]
        if char == comp_char:
            total += int(char)
    return total


def run():
    seq = read_file()
    print(solve_capcha(seq, mode="part_1"))
    print(solve_capcha(seq, mode="part_2"))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
