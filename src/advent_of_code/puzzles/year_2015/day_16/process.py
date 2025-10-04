"""
2015 Day 16

Part 1
Find the Aunt Sue that matches the following:
children: 3
cats: 7
samoyeds: 2
pomeranians: 3
akitas: 0
vizslas: 0
goldfish: 5
trees: 3
cars: 2
perfumes: 1

Part 2
Part 1, but cats is greater than 7, trees is greater than 3, pomeranians is less than 3 and goldfish is less than 5.
"""

import re
import itertools
from collections.abc import Callable

from advent_of_code.common import read_file, timed_run


SUE_PATTERN = r"Sue \w+: (?P<compound_1_name>\w+): (?P<compound_1_val>\d+), (?P<compound_2_name>\w+): (?P<compound_2_val>\d+), (?P<compound_3_name>\w+): (?P<compound_3_val>\d+)"

MFCSAM_RESULT_PART_1 = {
    "children": lambda val: val == 3,
    "cats": lambda val: val == 7,
    "samoyeds": lambda val: val == 2,
    "pomeranians": lambda val: val == 3,
    "akitas": lambda val: val == 0,
    "vizslas": lambda val: val == 0,
    "goldfish": lambda val: val == 5,
    "trees": lambda val: val == 3,
    "cars": lambda val: val == 2,
    "perfumes": lambda val: val == 1,
}

MFCSAM_RESULT_PART_2 = {
    "children": lambda val: val == 3,
    "cats": lambda val: val > 7,
    "samoyeds": lambda val: val == 2,
    "pomeranians": lambda val: val < 3,
    "akitas": lambda val: val == 0,
    "vizslas": lambda val: val == 0,
    "goldfish": lambda val: val < 5,
    "trees": lambda val: val > 3,
    "cars": lambda val: val == 2,
    "perfumes": lambda val: val == 1,
}


def parse_sue_details(sue_details_text: str) -> list[dict[str, int]]:
    sue_details: list[dict[str, int]] = []
    for line in sue_details_text.splitlines():
        if (match := re.fullmatch(SUE_PATTERN, line)) is not None:
            sue_detail = {
                match.group("compound_1_name"): int(match.group("compound_1_val")),
                match.group("compound_2_name"): int(match.group("compound_2_val")),
                match.group("compound_3_name"): int(match.group("compound_3_val")),
            }
            sue_details.append(sue_detail)
        else:
            raise ValueError("did not match re pattern")
    return sue_details


def find_sue(
    sue_details: list[dict[str, int]], mfcsam_result: dict[str, Callable[[int], bool]]
) -> int:
    for sue_no, sue_detail in zip(itertools.count(start=1), sue_details):
        if all(mfcsam_result[name](val) for name, val in sue_detail.items()):
            return sue_no
    raise ValueError("Error - could not find correct Sue")


def run():
    sue_details_text = read_file()
    sue_details = parse_sue_details(sue_details_text)
    print(find_sue(sue_details, mfcsam_result=MFCSAM_RESULT_PART_1))
    print(find_sue(sue_details, mfcsam_result=MFCSAM_RESULT_PART_2))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
