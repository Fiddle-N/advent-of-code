from typing import Self
from collections.abc import Callable
from enum import Enum
from dataclasses import dataclass
import timeit


@dataclass(frozen=True)
class Coords:
    x: int
    y: int
    z: int = 0

    def __add__(self, other: Self) -> Self:
        return type(self)(self.x + other.x, self.y + other.y, self.z + other.z)

    def manhatten_distance(self, other: Self) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)


class Directions(Enum):
    UP = "^"
    DOWN = "v"
    RIGHT = ">"
    LEFT = "<"


FOUR_POINT_DIRECTION_TO_COORDS = {
    Directions.UP: Coords(0, -1),
    Directions.DOWN: Coords(0, 1),
    Directions.LEFT: Coords(-1, 0),
    Directions.RIGHT: Coords(1, 0),
}


class CardinalDirections(Enum):
    NORTH = "^"
    SOUTH = "v"
    EAST = ">"
    WEST = "<"


FOUR_POINT_CARDINAL_DIRECTION_TO_COORDS = {
    CardinalDirections.NORTH: Coords(0, -1),
    CardinalDirections.SOUTH: Coords(0, 1),
    CardinalDirections.WEST: Coords(-1, 0),
    CardinalDirections.EAST: Coords(1, 0),
}

EIGHT_POINT_DIRECTION_COORDS = [
    Coords(0, -1),
    Coords(1, -1),
    Coords(1, 0),
    Coords(1, 1),
    Coords(0, 1),
    Coords(-1, 1),
    Coords(-1, 0),
    Coords(-1, -1),
]


def read_file() -> str:
    with open("input.txt") as f:
        return f.read().rstrip("\n")


def timed_run(fn: Callable) -> None:
    print(f"Ran in {timeit.timeit(fn, number=1)} seconds.")


def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    intervals = sorted(intervals)
    left, right = intervals[:1], intervals[1:]
    for next_i in right:
        last_i = left.pop()
        if last_i[0] <= next_i[0] <= last_i[1]:
            i = (last_i[0], max(last_i[1], next_i[1]))
            left.append(i)
        else:
            left.extend((last_i, next_i))
    return left
