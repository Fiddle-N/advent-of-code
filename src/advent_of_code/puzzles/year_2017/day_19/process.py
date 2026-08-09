from enum import Enum
from string import ascii_uppercase
from typing import Literal

from advent_of_code.common import (
    Coords,
    Direction,
    FOUR_POINT_DIRECTION_TO_COORDS,
    read_file,
    timed_run,
)


class Path(Enum):
    VERTICAL = "|"
    HORIZONTAL = "-"
    CROSSROADS = "+"


class Location(str):
    pass


type RouteSegment = Path | Location


def parse(raw_route: str) -> dict[Coords, RouteSegment]:
    route = {}
    for y, row in enumerate(raw_route.splitlines()):
        for x, raw_segment in enumerate(row):
            if raw_segment in ascii_uppercase:
                segment = Location(raw_segment)
            else:
                try:
                    segment = Path(raw_segment)
                except ValueError:
                    assert raw_segment == " "
                    continue
            route[Coords(x, y)] = segment
    return route


class RouteTraverser:
    def __init__(self, route: dict[Coords, RouteSegment]):
        self.route = route

    def _find_start(self) -> Coords:
        candidates = [
            coord
            for coord, segment in self.route.items()
            if coord.y == 0 and segment == Path.VERTICAL
        ]
        assert len(candidates) == 1
        return candidates[0]

    def _switch_dir(
        self, position: Coords, search: Literal["horizontal", "vertical"]
    ) -> Direction:
        dirs = (
            (Direction.UP, Direction.DOWN)
            if search == "vertical"
            else (Direction.LEFT, Direction.RIGHT)
        )
        candidates = [
            dir_
            for dir_ in dirs
            if (position + FOUR_POINT_DIRECTION_TO_COORDS[dir_]) in self.route
        ]
        assert len(candidates) == 1
        return candidates[0]

    def traverse(self) -> tuple[str, int]:
        state = Direction.DOWN
        position = self._find_start()
        seen = []
        steps = 1  # at start, packet has already taken one step
        while True:
            position += FOUR_POINT_DIRECTION_TO_COORDS[state]
            try:
                segment = self.route[position]
            except KeyError:
                return ("".join(seen), steps)

            steps += 1

            match (state, segment):
                case (_, Location() as location):
                    seen.append(location)
                case (Direction.UP | Direction.DOWN, Path.CROSSROADS):
                    state = self._switch_dir(position, search="horizontal")
                case (Direction.LEFT | Direction.RIGHT, Path.CROSSROADS):
                    state = self._switch_dir(position, search="vertical")
                case _:
                    # no change to direction
                    pass


def run():
    raw_route = read_file()
    route = parse(raw_route)
    print(RouteTraverser(route).traverse())


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
