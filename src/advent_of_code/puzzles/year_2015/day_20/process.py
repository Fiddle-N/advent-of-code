"""
2015 Day 20

https://adventofcode.com/2015/day/20

Part 1
Since elves deliver 10 times their number at each
house, an optimisation is to divide the target and
the present multiplier by 10.

Part 2
Elves only deliver to 50 houses but deliver 11 times
their number at each house.
"""

from advent_of_code.common import read_file, timed_run


def find_lowest_house(
    target: int, present_multiplier: int, delivery_limit: int | None = None
):
    houses = [None] + [0] * target
    for elf in range(1, target + 1):
        for house in range(
            elf, (target if delivery_limit is None else (elf * delivery_limit)) + 1, elf
        ):
            if house <= target:
                houses[house] += elf * present_multiplier
        if houses[elf] >= target:
            return elf


def run():
    target = int(read_file())
    print(
        find_lowest_house(
            target=target // 10,
            present_multiplier=1,
        )
    )
    print(find_lowest_house(target=target, present_multiplier=11, delivery_limit=50))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
