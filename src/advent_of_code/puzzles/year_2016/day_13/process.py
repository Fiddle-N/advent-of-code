from dataclasses import dataclass
from functools import cache
from collections import deque

from advent_of_code.common import (
    Coords,
    FOUR_POINT_DIRECTION_COORDS,
    timed_run,
    read_file,
)


@dataclass(frozen=True)
class LocationState:
    location: Coords
    steps: int


START = Coords(1, 1)
TARGET = Coords(31, 39)

REACHABLE_FROM_STEPS = 50


class BuildingNavigator:
    def __init__(self, fave: int):
        self.fave = fave

    @cache
    def _is_open_space(self, coords: Coords) -> bool:
        sum_value = (
            coords.x * coords.x
            + 3 * coords.x
            + 2 * coords.x * coords.y
            + coords.y
            + coords.y * coords.y
            + self.fave
        )
        bitmask = f"{sum_value:0b}"
        bit_no = sum([int(bit_) for bit_ in bitmask])
        return bit_no % 2 == 0

    def simulate(
        self, start: Coords, target: Coords, reachable_from_steps: int = 0
    ) -> tuple[int, int]:
        # bfs

        q = deque([LocationState(start, 0)])
        states = {start}
        reachable = set()
        minimum_steps = None

        while q:
            ls = q.pop()

            if ls.steps <= reachable_from_steps:
                reachable.add(ls.location)

            if ls.location == target:
                minimum_steps = ls.steps

            if ls.steps > reachable_from_steps and minimum_steps is not None:
                return (minimum_steps, len(reachable))

            # calculate adjacent locations
            for offset in FOUR_POINT_DIRECTION_COORDS:
                adj_location = ls.location + offset

                # invalid coordinates - skip
                if adj_location.x < 0 or adj_location.y < 0:
                    continue

                # already visited - skip
                if adj_location in states:
                    continue

                if not self._is_open_space(adj_location):
                    continue

                q.appendleft(LocationState(adj_location, ls.steps + 1))
                states.add(adj_location)

        raise Exception


def run() -> None:
    fave_number = int(read_file())
    bn = BuildingNavigator(fave_number)
    print(
        bn.simulate(
            start=START, target=TARGET, reachable_from_steps=REACHABLE_FROM_STEPS
        )
    )


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
