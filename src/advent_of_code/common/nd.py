from typing import Self
from enum import Enum, auto
from dataclasses import dataclass
from math import sqrt

__all__ = [
    "Coords",
    "Grid",
    "Direction",
    "Turn",
    "CardinalDirection",
    "FOUR_POINT_DIRECTION_COORDS",
    "DIRECTION_LETTERS_TO_DIRECTION",
    "FOUR_POINT_CARDINAL_DIRECTIONS",
    "FOUR_POINT_DIRECTION_TO_COORDS",
    "FOUR_POINT_CARDINAL_DIRECTION_TO_COORDS",
    "EIGHT_POINT_DIRECTION_COORDS",
    "turn_cardinal_direction",
]


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


class Grid(dict):
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        super().__init__(
            (Coords(x, y), False) for y in range(rows) for x in range(cols)
        )

    def __repr__(self) -> str:
        return f"{type(self).__name__}(rows={self.rows}, cols={self.cols})"

    def __str__(self) -> str:
        return "\n".join(
            "".join(["#" if self[Coords(x, y)] else "." for x in range(self.cols)])
            for y in range(self.rows)
        )

    def render(self) -> str:
        return "\n".join(
            "".join(["██" if self[Coords(x, y)] else "  " for x in range(self.cols)])
            for y in range(self.rows)
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


def turn_cardinal_direction(
    dir_: CardinalDirection, turn: Turn, no_of_turns: int
) -> CardinalDirection:
    offset = -1 if turn == turn.LEFT else 1
    dir_pos = FOUR_POINT_CARDINAL_DIRECTIONS.index(dir_)
    new_dir_pos = dir_pos + (offset * no_of_turns)
    return FOUR_POINT_CARDINAL_DIRECTIONS[new_dir_pos % 4]
