import re
from collections import defaultdict

from advent_of_code.common import read_file, timed_run

COMPOUND_PATTERN = r"[A-Z][a-z]?"
COMPOUND_MAP_PATTERN = r"(?P<source>\w+) => (?P<target>\w+)"


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
    compound: str, compound_map: dict[str, list[str]]
) -> int:
    chunked_compound = chunk_compound(compound)
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


def run():
    compound_map_text, compound = read_file().split("\n\n")
    compound_map = parse_compound_map(compound_map_text)
    print(count_unique_transformations(compound, compound_map))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
