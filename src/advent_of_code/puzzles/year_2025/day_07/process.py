from dataclasses import dataclass
from functools import cache
from typing import Self

from advent_of_code.common import Coords, read_file, timed_run

START = "S"
SPLITTER = "^"


DOWN = Coords(0, 1)
LEFT = Coords(-1, 0)
RIGHT = Coords(1, 0)


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


class TachyonManifoldResolver:
    def __init__(self, tm: TachyonManifold):
        self.tm = tm

    @cache
    def split(self, splitter: Coords) -> int:
        return self.path(splitter + LEFT) + self.path(splitter + RIGHT)

    def path(self, curr: Coords) -> int:
        while True:
            immediate_below = curr + DOWN
            if immediate_below.y == self.tm.length:
                # end of manifold - beam terminates
                return 1
            elif immediate_below in self.tm.splitters:
                # beam splits
                return self.split(immediate_below)
            else:
                curr = immediate_below
            # beam continues down

    def resolve(self) -> tuple[int, int]:
        paths = self.path(self.tm.start)
        splits = self.split.cache_info().misses
        return (splits, paths)


def run():
    tm = TachyonManifold.from_input(read_file())
    tmr = TachyonManifoldResolver(tm)
    print(tmr.resolve())


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
