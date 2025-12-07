from dataclasses import dataclass
from functools import cache
from typing import Self

from advent_of_code.common import (
    Coords,
    Directions,
    FOUR_POINT_DIRECTION_TO_COORDS,
    read_file,
    timed_run,
)

START = "S"
SPLITTER = "^"


@dataclass
class TachyonManifold:
    start: Coords
    length: int
    splitters: set[Coords]

    @classmethod
    def from_input(cls, raw_input: str) -> Self:
        lines = raw_input.splitlines()
        length = len(lines)
        splitters = set()
        for y, row in enumerate(lines):
            for x, space in enumerate(row):
                coord = Coords(x, y)
                if space == START:
                    start = coord
                elif space == SPLITTER:
                    splitters.add(coord)
        return cls(start, length, splitters)


class TachyonManifoldSimulator:
    def __init__(self, tm: TachyonManifold):
        self.tm = tm

    @cache
    def _split(self, splitter: Coords) -> int:
        return self._simulate(
            splitter + FOUR_POINT_DIRECTION_TO_COORDS[Directions.LEFT]
        ) + self._simulate(splitter + FOUR_POINT_DIRECTION_TO_COORDS[Directions.RIGHT])

    def _simulate(self, curr: Coords) -> int:
        while True:
            next_ = curr + FOUR_POINT_DIRECTION_TO_COORDS[Directions.DOWN]
            if next_.y == self.tm.length:
                # end of manifold - beam terminates
                return 1
            elif next_ in self.tm.splitters:
                # beam splits
                return self._split(next_)
            else:
                # beam continues down
                curr = next_

    def simulate(self) -> tuple[int, int]:
        timelines = self._simulate(self.tm.start)
        splits = self._split.cache_info().misses
        return (splits, timelines)


def run():
    tm = TachyonManifold.from_input(read_file())
    tmr = TachyonManifoldSimulator(tm)
    print(tmr.simulate())


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
