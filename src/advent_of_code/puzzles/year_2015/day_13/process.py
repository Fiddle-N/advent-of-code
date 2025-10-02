"""
2015 Day 13

Part 1
Seat people at a circular table where one person has a certain happiness score towards the person they sit next to, and
work out the total happiness possible.

Part 2
Part 1, but add yourself into the table, where you add 0 to any happiness relationships including you.
"""

import itertools
import re
from typing import cast, Self

from advent_of_code.common import read_file, timed_run


RELATIONSHIP_PATTERN = r"(?P<subject>\w+) would (?P<happiness_sign>gain|lose) (?P<happiness_units>\d+) happiness units by sitting next to (?P<object>\w+)."

YOURSELF = "__YOURSELF"


class DinnerTableResolver:
    def __init__(self, attendees: list[str], relationships: dict[tuple[str, str], int]):
        self.attendees = attendees
        self.relationships = relationships

    @classmethod
    def from_text(cls, text: str) -> Self:
        attendees: list[str] = []
        relationships: dict[tuple[str, str], int] = {}
        for line in text.splitlines():
            if (match := re.fullmatch(RELATIONSHIP_PATTERN, line)) is not None:
                subject = match.group("subject")
                object_ = match.group("object")
                happiness_sign = 1 if match.group("happiness_sign") == "gain" else -1
                happiness_units = int(match.group("happiness_units"))
                happiness = happiness_units * happiness_sign

                if subject not in attendees:
                    attendees.append(subject)

                relationships[(subject, object_)] = happiness

        return cls(attendees, relationships)

    def _resolve(self, arrangement: tuple[str, ...]) -> int:
        happiness = 0
        arrangement_pairs = arrangement + (
            arrangement[0],
        )  # re-add first person to simulate circular table
        for pair in itertools.pairwise(arrangement_pairs):
            if YOURSELF in pair:
                # zero change in happiness
                continue
            reversed_pair = tuple(reversed(pair))
            reversed_pair = cast(tuple[str, str], reversed_pair)
            happiness += self.relationships[pair]
            happiness += self.relationships[reversed_pair]
        return happiness

    def resolve(self, include_yourself: bool = False) -> int:
        attendees = self.attendees.copy()
        if include_yourself:
            attendees.append(YOURSELF)
        best_happiness = None
        for arrangement in itertools.permutations(attendees, len(attendees)):
            happiness = self._resolve(arrangement)
            if best_happiness is None or best_happiness < happiness:
                best_happiness = happiness
        best_happiness = cast(int, best_happiness)
        return best_happiness


def run():
    relationship_text = read_file()
    dtr = DinnerTableResolver.from_text(relationship_text)
    print(dtr.resolve())
    print(dtr.resolve(include_yourself=True))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
