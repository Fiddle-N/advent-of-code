from typing import Self
from collections.abc import Callable
from enum import Enum, auto
from dataclasses import dataclass
from math import sqrt
import timeit


@dataclass(frozen=True, order=True)
class Coords:
    x: int
    y: int
    z: int = 0

    def __add__(self, other: Self) -> Self:
        return type(self)(self.x + other.x, self.y + other.y, self.z + other.z)

    def manhattan_distance_to(self, other: Self) -> int:
        return abs(self.x - other.x) + abs(self.y - other.y) + abs(self.z - other.z)

    def distance_to(self, other: Self) -> float:
        return sqrt(
            (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2
        )


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    RIGHT = auto()
    LEFT = auto()


class Turn(Enum):
    LEFT = "L"
    RIGHT = "R"


class CardinalDirection(Enum):
    NORTH = "^"
    EAST = ">"
    SOUTH = "v"
    WEST = "<"


FOUR_POINT_DIRECTION_COORDS = [
    Coords(0, -1),
    Coords(1, 0),
    Coords(0, 1),
    Coords(-1, 0),
]


DIRECTION_LETTERS_TO_DIRECTION = {
    "U": Direction.UP,
    "D": Direction.DOWN,
    "R": Direction.RIGHT,
    "L": Direction.LEFT,
}


FOUR_POINT_CARDINAL_DIRECTIONS = list(CardinalDirection)


FOUR_POINT_DIRECTION_TO_COORDS = {
    Direction.UP: FOUR_POINT_DIRECTION_COORDS[0],
    Direction.RIGHT: FOUR_POINT_DIRECTION_COORDS[1],
    Direction.DOWN: FOUR_POINT_DIRECTION_COORDS[2],
    Direction.LEFT: FOUR_POINT_DIRECTION_COORDS[3],
}


FOUR_POINT_CARDINAL_DIRECTION_TO_COORDS = {
    CardinalDirection.NORTH: FOUR_POINT_DIRECTION_COORDS[0],
    CardinalDirection.EAST: FOUR_POINT_DIRECTION_COORDS[1],
    CardinalDirection.SOUTH: FOUR_POINT_DIRECTION_COORDS[2],
    CardinalDirection.WEST: FOUR_POINT_DIRECTION_COORDS[3],
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


def turn_cardinal_direction(
    dir_: CardinalDirection, turn: Turn, no_of_turns: int
) -> CardinalDirection:
    offset = -1 if turn == turn.LEFT else 1
    dir_pos = FOUR_POINT_CARDINAL_DIRECTIONS.index(dir_)
    new_dir_pos = dir_pos + (offset * no_of_turns)
    return FOUR_POINT_CARDINAL_DIRECTIONS[new_dir_pos % 4]
