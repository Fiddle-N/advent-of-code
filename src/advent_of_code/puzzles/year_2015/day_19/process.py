"""
2015 Day 19

Part 1
Parse the given compound and count all element replacements that
result in unique transformations.

Part 2
Calculate the number of transformations to go from a starting point
(e) to the given compound.

There are only certain types of transformations possible:

Case 1: a => b c
Case 2: a => b Rn c Ar
Case 3: a => b Rn c Y d Ar
Case 4: a => b Rn c Y d Y e Ar

Furthermore - Rn, Ar and Y have no transformations of their own.
As a result, they mimic ( ) and , in a grammar describing a language,
like so:

Case 1: a => bc
Case 2: a => b(c)
Case 3: a => b(c,d)
Case 4: a => b(c,d,e)

The number of transformations can therefore be calculated entirely
mathematically.

First, consider Case 1.
The number of steps to create this is simply the number of elements
minus 1
e.g. e -> ad and then d -> bc.
len(elements) - 1
3 - 1 = 2.

Now consider Case 2.
Think of it as "Rn c Ar" in Case 2 replacing "c" in Case 1.
Hence, by simply subtracting the number of Rn and Ar, for as many
instances of it exists, we get to the answer.
len(elements) - len(Rn) - len(Ar) - 1
4 - 1 - 1 - 1 = 1

Now consider Case 3 and 4.
Again, think of "Rn c Y d Ar" replacing "c" in Case 1.
We have already taken care of Rn and Ar in Case 2.
But the presence of Y also adds an extra element - d.
In the case of "Rn c Y d Y e Ar", the presence of two Ys
has added two extra elements - d and e.
So, we also need to subtract the number of Ys x 2, to account
for the extra elements added, to get to the answer.
len(elements) - len(Rn) - len(Ar) - (2 * len(Y)) - 1

b Rn c Y d Ar
6 - 1 - 1 - (2 * 1) - 1 = 1

b Rn c Y d Y e Ar
8 - 1 - 1 - (2 * 2) - 1 = 1
"""

import re
from collections import defaultdict, Counter

from advent_of_code.common import read_file, timed_run

COMPOUND_PATTERN = r"[A-Z][a-z]?"
COMPOUND_MAP_PATTERN = r"(?P<source>\w+) => (?P<target>\w+)"

LEFT_BRACKET = "Rn"
COMMA = "Y"
RIGHT_BRACKET = "Ar"


def chunk_compound(compound: str) -> list[str]:
    return re.findall(COMPOUND_PATTERN, compound)


def parse_compound_map(compound_map_text: str) -> dict[str, list[str]]:
    compound_map = defaultdict(list)
    for match_ in re.finditer(COMPOUND_MAP_PATTERN, compound_map_text):
        compound_map[match_.group("source")].append(match_.group("target"))
    return compound_map


def flip_compound_map(compound_map: dict[str, list[str]]) -> dict[str, list[str]]:
    reversed_map = defaultdict(list)
    for element, compound_transforms in compound_map.items():
        for compound in compound_transforms:
            reversed_map[compound].append(element)
    return reversed_map


def groupby_idx(chunked_compound: list[str]) -> dict[str, list[int]]:
    grouped_compound = defaultdict(list)
    for idx, element in enumerate(chunked_compound):
        grouped_compound[element].append(idx)
    return grouped_compound


def count_unique_transformations(
    chunked_compound: list[str], compound_map: dict[str, list[str]]
) -> int:
    grouped_compound = groupby_idx(chunked_compound)
    filtered_compound_map = {
        element: compound_transforms
        for element, compound_transforms in compound_map.items()
        if element in grouped_compound
    }

    transforms = set()
    for element, compound_transforms in filtered_compound_map.items():
        element_positions = grouped_compound[element]
        for transformed in compound_transforms:
            for position in element_positions:
                new_compound = chunked_compound.copy()
                new_compound[position] = transformed
                transforms.add("".join(new_compound))

    return len(transforms)


def count_steps_from_e(chunked_compound: list[str]) -> int:
    element_count = Counter(chunked_compound)
    return (
        len(chunked_compound)
        - element_count[LEFT_BRACKET]
        - element_count[RIGHT_BRACKET]
        - (2 * element_count[COMMA])
        - 1
    )


def run():
    compound_map_text, compound = read_file().split("\n\n")
    compound_map = parse_compound_map(compound_map_text)

    chunked_compound = chunk_compound(compound)
    print(count_unique_transformations(chunked_compound, compound_map))

    print(count_steps_from_e(chunked_compound))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
