import dataclasses
import enum
import itertools

import parse
from typing import Self


@dataclasses.dataclass(frozen=True)
class Coords:
    x: int
    y: int

    def __add__(self, other: Self) -> Self:
        return Coords(self.x + other.x, self.y + other.y)

    def __mul__(self, other: int) -> Self:
        return Coords(self.x * other, self.y * other)


class Direction(enum.Enum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


DIR_STR_MAPPING = {
    'U': Direction.UP,
    'D': Direction.DOWN,
    'L': Direction.LEFT,
    'R': Direction.RIGHT,
}


OFFSET_COORDS = {
    Direction.UP: Coords(0, -1),
    Direction.DOWN: Coords(0, 1),
    Direction.LEFT: Coords(-1, 0),
    Direction.RIGHT: Coords(1, 0),
}


@dataclasses.dataclass(frozen=True)
class DigInstruct:
    dir_: Direction
    num: int


def parse_plan(plan_input: str, extract_data_from_hex: bool = False) -> list[DigInstruct]:
    plan = []
    for instruct_input in plan_input.splitlines():
        parsed_instruct = parse.parse(
            '{dir} {num:d} ({hex})',
            instruct_input
        )
        if extract_data_from_hex:
            hex = parsed_instruct['hex']
            hex_num = hex[1:-1]
            hex_dir = hex[-1]
            num = int(hex_num, 16)
            dir_ = Direction(int(hex_dir))
        else:
            dir_ = DIR_STR_MAPPING[parsed_instruct['dir']]
            num = parsed_instruct['num']

        plan.append(
            DigInstruct(
                dir_=dir_,
                num=num,
            )
        )
    return plan


def capacity(plan: list[DigInstruct]) -> int:
    # calculate path vertices and path length
    start = Coords(0, 0)
    pos = start
    path_verts = [start]
    path_length = 0
    for instr in plan:
        pos += (OFFSET_COORDS[instr.dir_] * instr.num)
        path_verts.append(pos)
        path_length += instr.num
    assert pos == start

    # Use shoelace formula and Pick's theorem to get internal points
    # (see 2023 day 10 for more info)

    area = abs(
        sum(
            [(p1.x - p2.x) * (p1.y + p2.y) for p1, p2 in itertools.pairwise(path_verts)]
        ) // 2
    )
    interior_points = area - (path_length // 2) + 1

    lagoon_capacity = path_length + interior_points
    return lagoon_capacity


def read_file() -> str:
    with open("input.txt") as f:
        return f.read()


def main():
    input_ = read_file()
    plan = parse_plan(input_)
    print(
        "Lagoon capacity:",
        capacity(plan),
    )
    plan_from_hex = parse_plan(input_, extract_data_from_hex=True)
    print(
        "Lagoon capacity using hex data:",
        capacity(plan_from_hex),
    )


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
