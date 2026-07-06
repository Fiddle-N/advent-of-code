from dataclasses import dataclass
from itertools import combinations
from math import prod, ceil

from advent_of_code.common import read_file, timed_run


@dataclass(frozen=True)
class FirstPresentGroup:
    presents: tuple[int, ...]
    qe: int


def parse_input(raw_input: str) -> list[int]:
    return [int(x) for x in raw_input.splitlines()]


def _get_target(presents: list[int], no_of_groups: int) -> int:
    div, mod = divmod(sum(presents), no_of_groups)
    assert mod == 0
    return div


def _validate_subsequent_groups(
    group: tuple[int, ...], current_presents: list[int], target: int, no_of_groups: int
) -> bool:
    if no_of_groups == 1:
        return True

    remaining_presents = current_presents.copy()
    for present in group:
        remaining_presents.remove(present)

    # iterate over lengths for the next present group
    # be strict in our range end as we don't want to repeat checks
    # checks for groups larger than ceil(length / 2) is a repeat of a smaller group check
    for next_len in range(1, ceil(len(remaining_presents) / 2) + 1):
        groups = combinations(remaining_presents, next_len)
        for group in groups:
            if (sum(group) == target) and _validate_subsequent_groups(
                group, remaining_presents, target, no_of_groups=no_of_groups - 1
            ):
                return True
    return False


def group_packages(presents: list[int], no_of_groups: int) -> FirstPresentGroup:
    # ensure unique presents
    assert len(presents) == len(set(presents))

    target = _get_target(presents, no_of_groups)

    # iterate over all possible lengths for the first present group
    # be lax in our range end as we expect to return long before we reach it
    for first_len in range(1, len(presents)):
        firsts_qes = {
            group: prod(group)
            for group in combinations(presents, first_len)
            if sum(group) == target
        }
        if not firsts_qes:
            continue

        sorted_firsts = sorted(firsts_qes, key=lambda first: firsts_qes[first])

        # ensure the rest of the packages can create valid groups
        for first_group in sorted_firsts:
            if _validate_subsequent_groups(
                group=first_group,
                current_presents=presents,
                target=target,
                no_of_groups=no_of_groups - 1,
            ):
                return FirstPresentGroup(first_group, firsts_qes[first_group])

    raise ValueError("A valid result is expected from the input.")


def run():
    raw_presents = read_file()
    presents = parse_input(raw_presents)
    print(group_packages(presents, no_of_groups=3).qe)
    print(group_packages(presents, no_of_groups=4).qe)


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
