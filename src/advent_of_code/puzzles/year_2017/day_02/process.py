from itertools import combinations

from advent_of_code.common import read_file, timed_run


def parse_ss(raw_ss: str) -> list[list[int]]:
    return [[int(cell) for cell in row.split()] for row in raw_ss.splitlines()]


def calculate_checksum(ss: list[list[int]]) -> int:
    return sum((max(row) - min(row)) for row in ss)


def calculate_evenly_divisible(ss: list[list[int]]) -> int:
    total = 0
    for row in ss:
        for lower, higher in combinations(sorted(row), 2):
            div, mod = divmod(higher, lower)
            if mod == 0:
                total += div
                break
    return total


def run():
    raw_ss = read_file()
    ss = parse_ss(raw_ss)
    print(calculate_checksum(ss))
    print(calculate_evenly_divisible(ss))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
