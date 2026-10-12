import re
from collections import Counter
from itertools import product
from dataclasses import dataclass

from advent_of_code.common import (
    read_file,
    timed_run,
    Coords,
)

CLAIM_PATTERN = r"#(?P<id>\d+) @ (?P<top_left_x>\d+),(?P<top_left_y>\d+): (?P<width>\d+)x(?P<height>\d+)"


@dataclass(frozen=True)
class FabricClaim:
    id: int
    top_left: Coords
    width: int
    height: int


def parse(raw_claims: str) -> list[FabricClaim]:
    claims = []
    for raw_claim in raw_claims.splitlines():
        match = re.fullmatch(CLAIM_PATTERN, raw_claim)
        assert match is not None
        claims.append(
            FabricClaim(
                id=int(match["id"]),
                top_left=Coords(int(match["top_left_x"]), int(match["top_left_y"])),
                width=int(match["width"]),
                height=int(match["height"]),
            )
        )
    return claims


def _find_non_overlapping_id(
    claims: list[FabricClaim],
    claim_coords: list[list[tuple[int, int]]],
    coord_counts: Counter[tuple[int, int]],
):
    for claim, coord_range in zip(claims, claim_coords):
        if all(coord_counts[coord] == 1 for coord in coord_range):
            return claim.id
    raise ValueError("non-overlapping claim must be present")


def calculate_overlaps_and_non_overlapping_id(
    claims: list[FabricClaim],
) -> tuple[int, int]:
    claim_coords = []
    for claim in claims:
        width_range = range(claim.top_left.x, claim.top_left.x + claim.width)
        height_range = range(claim.top_left.y, claim.top_left.y + claim.height)
        claim_coords.append(list(product(width_range, height_range)))
    coord_counts = Counter(
        [coord for coord_range in claim_coords for coord in coord_range]
    )

    overlaps = sum((count >= 2) for count in coord_counts.values())
    non_overlapping_id = _find_non_overlapping_id(claims, claim_coords, coord_counts)

    return overlaps, non_overlapping_id


def run():
    raw_claims = read_file()
    claims = parse(raw_claims)
    print(calculate_overlaps_and_non_overlapping_id(claims))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
