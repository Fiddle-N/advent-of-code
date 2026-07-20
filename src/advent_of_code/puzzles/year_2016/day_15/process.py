"""
2016 Day 15

https://adventofcode.com/2016/day/15

Let's take the example:

Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1.

What this means is:
value_1(t) = (4 + t) mod 5
value_2(t) = (1 + t) mod 2

We can solve this using congruence and the Chinese Remainder Theorem.

---
Congruence

If
A ≡ B mod n
This means that if you divide A by n and B by n, you get the same remainder.

Since mod n works on a continuous cycle of 0 to n - 1,
it stands to reason that A - 1 and B - 1 will have the same remainder,
as will A - 2 and B - 2, and so on.

Hence, since addition and subtraction are possible
we can also rearrange the terms such that:
(A - B) ≡ (B - B) mod n
or
A - B ≡ 0 mod n
.

0 mod n is quite important to recognise
since 0 divided by n is 0 and leaves no remainder,
A - B ≡ 0 mod n
means that
A - B must also be a multiple of n and leave no remainder,
or in other words
(A - B) mod n = 0

---
Chinese Remainder Theorem

If you have a series of congruences in the form

x ≡ A mod m
x ≡ B mod n
x ≡ C mod o
etc

then assuming that m, n, o etc are all coprime (they only share 1 as their common divisor)
CRT can be used to find

x ≡ D mod p

that would satisfy them all.

---
Putting it all together,

value_1(t) = (4 + t) mod 5
value_2(t) = (1 + t) mod 2

If we represent the time spent waiting as T seconds
then at T + 1 we want value_1(t) to be 0
and at T + 2 we want value_2(t) to be 0.

So
value_1(T + 1) = (4 + (T + 1)) mod 5
(4 + (T + 1)) mod 5 = 0
and since we are saying that (4 + (T + 1)) is a multiple of 5, then
(4 + (T + 1)) ≡ 0 mod 5
T ≡ -(4 + 1) mod 5

value_2(T + 2) = (1 + (T + 2)) mod 2
(1 + (T + 2)) mod 2 = 0
(1 + (T + 2)) ≡ 0 mod 2
T ≡ -(2 + 1) mod 2

From here, since 2 and 5 are coprime, CRT can be used to solve this equation:
T ≡ 5 mod 10

So T must be 5, 15, 25 etc to satisfy the equation, with the lowest value being 5.

"""

import re

from advent_of_code.common import (
    ModInt,
    crt,
    timed_run,
    read_file,
)

DISC_PATTERN = (
    r"Disc #\d+ has (?P<mod>\d+) positions; at time=0, it is at position (?P<val>\d+)."
)


def parse_discs(raw_discs: str) -> list[ModInt]:
    discs = []
    for raw_disc in raw_discs.splitlines():
        match_ = re.fullmatch(DISC_PATTERN, raw_disc)
        assert match_
        discs.append(ModInt(mod=int(match_["mod"]), val=int(match_["val"])))
    return discs


def offset_discs(discs: list[ModInt]) -> list[ModInt]:
    return [
        ModInt(val=-(disc.val + disc_no), mod=disc.mod)
        for disc_no, disc in enumerate(discs, start=1)
    ]


def calculate_button_press(discs: list[ModInt]) -> int:
    disc_offsets = offset_discs(discs)
    return crt(disc_offsets).val


def run() -> None:
    raw_discs = read_file()
    discs = parse_discs(raw_discs)
    print(calculate_button_press(discs))
    discs.append(ModInt(0, 11))
    print(calculate_button_press(discs))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
