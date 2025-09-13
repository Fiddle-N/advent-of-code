from typing import Self
from enum import Enum
from dataclasses import dataclass


@dataclass(frozen=True)
class Coords:
    x: int
    y: int

    def __add__(self, other: Self):
        return type(self)(self.x + other.x, self.y + other.y)


class Directions(Enum):
    NORTH = "^"
    SOUTH = "v"
    EAST = ">"
    WEST = "<"


DIRECTION_COORDS = {
    Directions.NORTH: Coords(0, -1),
    Directions.SOUTH: Coords(0, 1),
    Directions.WEST: Coords(-1, 0),
    Directions.EAST: Coords(1, 0),
}


def read_file() -> str:
    with open("input.txt") as f:
        return f.read().strip()
