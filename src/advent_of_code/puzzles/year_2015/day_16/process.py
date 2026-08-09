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
from functools import partial
from typing import Literal
from operator import eq

from advent_of_code.common import read_file, timed_run


SUE_PATTERN = (
    r"Sue \w+: (?P<compound_1_name>\w+): (?P<compound_1_val>\d+), "
    r"(?P<compound_2_name>\w+): (?P<compound_2_val>\d+), "
    r"(?P<compound_3_name>\w+): (?P<compound_3_val>\d+)"
)


def eq_factory(condition: int) -> Callable[[int], bool]:
    return partial(eq, condition)


def lt_factory(condition: int) -> Callable[[int], bool]:
    def lt(val: int) -> bool:
        return val < condition

    return lt


def gt_factory(condition: int) -> Callable[[int], bool]:
    def gt(val: int) -> bool:
        return val > condition

    return gt


MFCSAM_PRINTOUT = {
    "children": 3,
    "cats": 7,
    "samoyeds": 2,
    "pomeranians": 3,
    "akitas": 0,
    "vizslas": 0,
    "goldfish": 5,
    "trees": 3,
    "cars": 2,
    "perfumes": 1,
}

GREATER_THAN_RANGES = ["cats", "trees"]
LESS_THAN_RANGES = ["pomeranians", "goldfish"]


def generate_mfcsam_comp_fns(mode: Literal["part_1", "part_2"]):
    comp_fns = {}
    for compound, value in MFCSAM_PRINTOUT.items():
        comp_fn_factory = (
            gt_factory
            if mode == "part_2" and compound in GREATER_THAN_RANGES
            else lt_factory
            if mode == "part_2" and compound in LESS_THAN_RANGES
            else eq_factory
        )
        comp_fns[compound] = comp_fn_factory(value)
    return comp_fns


def parse_sue_details(sue_details_text: str) -> list[dict[str, int]]:
    sue_details: list[dict[str, int]] = []
    for line in sue_details_text.splitlines():
        match = re.fullmatch(SUE_PATTERN, line)
        assert match is not None
        sue_detail = {
            match["compound_1_name"]: int(match["compound_1_val"]),
            match["compound_2_name"]: int(match["compound_2_val"]),
            match["compound_3_name"]: int(match["compound_3_val"]),
        }
        sue_details.append(sue_detail)
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
    print(find_sue(sue_details, mfcsam_result=generate_mfcsam_comp_fns("part_1")))
    print(find_sue(sue_details, mfcsam_result=generate_mfcsam_comp_fns("part_2")))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
