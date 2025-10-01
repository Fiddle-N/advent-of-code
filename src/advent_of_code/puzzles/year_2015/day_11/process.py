"""
2015 Day 11

Part 1
Iterate an 8 character password made of lower-case letters and find the next password where
- no i, o or l is present
- there is a window of 3 chars where the chars are next to each other in the alphabet (e.g. abc, stu...)
- there are two different, overlapping pairs of letters (e.g. aa, bb, zz..)

Part 2
Find the next password.
"""

import itertools
import typing

import more_itertools

from advent_of_code.common import read_file, timed_run

FORBIDDEN_LETTERS = ["i", "o", "l"]


def cycle_password(password):
    password_list = list(password)
    while True:
        cycle_next_char = True
        for rev_idx, char in enumerate(reversed(password_list)):
            idx = len(password_list) - rev_idx - 1
            if char == "z":
                password_list[idx] = "a"
            else:
                password_list[idx] = chr(ord(char) + 1)
                cycle_next_char = False
            if not cycle_next_char:
                yield "".join(password_list)
                break
        if cycle_next_char:
            # exhausted 8 char passes
            return None


def _validate_forbidden_letters(password: str) -> bool:
    return all(char not in FORBIDDEN_LETTERS for char in password)


def _validate_straight_increasing_three_chars(password: str) -> bool:
    for window in more_itertools.windowed(password, 3):
        window = typing.cast(
            tuple[str, str, str], window
        )  # since password is 8 chars, this will always be true
        if (ord(window[1]) - ord(window[0])) == (ord(window[2]) - ord(window[1])) == 1:
            return True
    return False


def _validate_two_different_non_overlapping_pairs(password: str) -> bool:
    return sum(len(list(g)) >= 2 for _, g in itertools.groupby(password)) >= 2


def validate_password(password: str) -> bool:
    return (
        _validate_forbidden_letters(password)
        and _validate_straight_increasing_three_chars(password)
        and _validate_two_different_non_overlapping_pairs(password)
    )


def next_valid_password(password: str) -> str:
    password_gen = cycle_password(password)
    for next_password in password_gen:
        if validate_password(next_password):
            return next_password
    raise ValueError("exhausted all passwords")


def run():
    input_password = read_file()
    next_password = next_valid_password(input_password)
    print(next_password)
    print(next_valid_password(next_password))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
