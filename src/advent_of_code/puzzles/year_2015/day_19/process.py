import re
from collections import defaultdict


COMPOUND_PATTERN = r"[A-Z][a-z]?"
COMPOUND_MAP_PATTERN = r"(?P<source>\w+) => (?P<target>\w+)"


def chunk_compound(compound: str) -> list[str]:
    return re.findall(COMPOUND_PATTERN, compound)


def parse_compound_map(compound_map_text: str) -> dict[str, list[str]]:
    compound_map = defaultdict(list)
    for match_ in re.finditer(COMPOUND_MAP_PATTERN, compound_map_text):
        compound_map[match_.group("source")].append(match_.group("target"))
    return compound_map


def flip_com(compound_map: dict[str, list[str]]) -> dict[str, list[str]]:
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


# def old_count_synthesis_steps(compound: str, compound_map: dict[str, list[str]]) -> int:
#     flipped_map = flip_compound_map(compound_map)
#     re_compound_pattern = (
#         rf"(?=(?P<compound>{'|'.join(compound for compound in flipped_map)}))"
#     )
#
#     q = deque()
#     q.append((compound, 0))
#
#     while q:
#         current_compound, steps = q.popleft()
#         next_steps = steps + 1
#         for match_ in re.finditer(re_compound_pattern, current_compound):
#             matched_compound = match_.group("compound")
#             for transform in flipped_map[matched_compound]:
#                 new_compound = (
#                     current_compound[: match_.start("compound")]
#                     + transform
#                     + current_compound[match_.end("compound") :]
#                 )
#                 # print(new_compound)
#                 # print(next_steps)
#                 if set(new_compound) == {"e"}:
#                     return next_steps
#                 q.append((new_compound, next_steps))
#
#     raise RuntimeError("invalid synthesis")


# def count_synthesis_steps(compound: str, compound_map: dict[str, list[str]]) -> int:
#     chunked_compound = chunk_compound(compound)
#     flipped_map = flip_compound_map(compound_map)
#
#     chunked_compound_map = [chunk_compound(c) for c in flipped_map]
#
#     # smallest_target = min(len(c) for c in chunked_compound_map)
#     # largest_target = max(len(c) for c in chunked_compound_map)
#     #
#     # right = deque(chunked_compound)
#
#     subs = 0
#     current_compound = compound
#     while True:
#         re_compound_pattern = (
#             rf"(?=(?P<compound>{'|'.join(compound for compound in flipped_map)}))"
#         )
#         match_ = re.search(re_compound_pattern, current_compound)
#         matched_compound = match_.group("compound")
#         transform = flipped_map[matched_compound][0]
#         current_compound = (
#             current_compound[: match_.start("compound")]
#             + transform
#             + current_compound[match_.end("compound") :]
#         )
#         subs += 1
#         print()
#
#     print()
#     raise RuntimeError("invalid synthesis")
#

# def run():
#     compound_map_text, compound = read_file().split("\n\n")
#     compound_map = parse_compound_map(compound_map_text)
#     print(count_unique_transformations(compound, compound_map))
#
#     # flipped_map = flip_compound_map(compound_map)
#     # for compound in flipped_map:
#     #     other_compounds = set(flipped_map) - {compound}
#     #     for other in other_compounds:
#     #         if other.endswith(compound):
#     #             print('uhuh')
#     # print('yay')
#
#     print(count_synthesis_steps(compound, compound_map))
#
#
# def main() -> None:
#     timed_run(run)
#
#
# if __name__ == "__main__":
#     main()
