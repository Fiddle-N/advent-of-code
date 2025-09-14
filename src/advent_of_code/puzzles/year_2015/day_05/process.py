"""
2015 Day 5

Part 1
Find the number of strings with at least 3 vowels, one letter twice in a row and doesn't contain the strings
ab, cd, pq, or xy. These strings are considered "nice".

Part 2
Find the number of strings with a pair of two letters that appear at least twice with no overlaps, and one letter that
repeats with exactly one letter between them. These strings will be nice "v2".
"""

import itertools

import more_itertools

from advent_of_code.common import read_file, timed_run

FORBIDDEN_STRS = ["ab", "cd", "pq", "xy"]


def _contains_three_vowels(str_: str) -> bool:
    return sum(char in "aeiou" for char in str_) >= 3


def _contains_one_letter_twice_in_a_row(str_: str) -> bool:
    for left_char, right_char in itertools.pairwise(str_):
        if left_char == right_char:
            return True
    return False


def _contains_forbidden_strings(str_: str) -> bool:
    for forbidden in FORBIDDEN_STRS:
        if forbidden in str_:
            return True
    return False


def _contains_char_pair_twice_nonoverlapping(str_: str) -> bool:
    if len(str_) < 4:
        # cannot contain char pair twice, immediately exclude
        return False
    for idx in range(2, len(str_)):
        left_str, right_str = str_[:idx], str_[idx:]
        if len(left_str) < 2 or len(right_str) < 2:
            # one side cannot contain char pair - immediately skip
            return False
        pair = left_str[-2:]
        if pair in right_str:
            return True
    return False


def _contains_one_letter_repeating_with_exactly_one_letter_between(str_: str) -> bool:
    for window in more_itertools.windowed(str_, 3):
        if window[0] == window[2]:
            return True
    return False


def is_nice(str_) -> bool:
    return (
        _contains_three_vowels(str_)
        and _contains_one_letter_twice_in_a_row(str_)
        and not _contains_forbidden_strings(str_)
    )


def is_nice_v2(str_) -> bool:
    return _contains_char_pair_twice_nonoverlapping(
        str_
    ) and _contains_one_letter_repeating_with_exactly_one_letter_between(str_)


def run():
    text = read_file()
    lines = text.splitlines()
    print(sum(is_nice(line) for line in lines))
    print(sum(is_nice_v2(line) for line in lines))


def main():
    timed_run(run)


if __name__ == "__main__":
    main()
