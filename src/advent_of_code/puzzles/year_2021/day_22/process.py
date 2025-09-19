"""
2021 Day 22

Consider a 3D grid of integer points. The points can either be on or off - all points are set to off at the start.
A sequence of steps define cuboids of points and an instruction to turn those points should be turned on or off.
Execute the steps in order and calculate the number of points that are on.

Part 1
Execute only the steps where the greatest point from the origin is no more than 50 units away.

Part 2
Execute all steps.
"""

import dataclasses
import enum
from typing import Self
from collections import defaultdict
from advent_of_code.common import read_file, Coords, timed_run

import parse

STEP_TEMPLATE = (
    "{state} x={x_start:d}..{x_end:d},y={y_start:d}..{y_end:d},z={z_start:d}..{z_end:d}"
)

INIT_PROCEDURE_MAX_DISTANCE_FROM_ORIGIN = 50


class Instruction(enum.Enum):
    ON = enum.auto()
    OFF = enum.auto()


@dataclasses.dataclass(frozen=True, eq=True)
class Cube:
    start: Coords
    end: Coords

    def intersect(self, other) -> Self | None:
        x_lower = max(self.start.x, other.start.x)
        x_upper = min(self.end.x, other.end.x)
        y_lower = max(self.start.y, other.start.y)
        y_upper = min(self.end.y, other.end.y)
        z_lower = max(self.start.z, other.start.z)
        z_upper = min(self.end.z, other.end.z)
        if x_lower <= x_upper and y_lower <= y_upper and z_lower <= z_upper:
            return type(self)(
                start=Coords(x_lower, y_lower, z_lower),
                end=Coords(x_upper, y_upper, z_upper),
            )
        return None

    @property
    def volume(self) -> int:
        return (
            (self.end.x - self.start.x + 1)
            * (self.end.y - self.start.y + 1)
            * (self.end.z - self.start.z + 1)
        )


def parse_steps(
    step_input: str, init_procedure_only: bool
) -> list[tuple[Cube, Instruction]]:
    steps = []
    for raw_step in step_input.splitlines():
        parsed_step = parse.parse(STEP_TEMPLATE, raw_step)
        if init_procedure_only:
            furthest_distance_from_origin = max(
                abs(parsed_step["x_start"]),
                abs(parsed_step["y_start"]),
                abs(parsed_step["z_start"]),
                abs(parsed_step["x_end"]),
                abs(parsed_step["y_end"]),
                abs(parsed_step["z_end"]),
            )
            if furthest_distance_from_origin > INIT_PROCEDURE_MAX_DISTANCE_FROM_ORIGIN:
                continue
        steps.append(
            (
                Cube(
                    start=Coords(
                        parsed_step["x_start"],
                        parsed_step["y_start"],
                        parsed_step["z_start"],
                    ),
                    end=Coords(
                        parsed_step["x_end"],
                        parsed_step["y_end"],
                        parsed_step["z_end"],
                    ),
                ),
                getattr(Instruction, parsed_step["state"].upper()),
            )
        )
    return steps


def reboot(steps: list[tuple[Cube, Instruction]]) -> int:
    signed_cubes = defaultdict(int)
    for cube, instruction in steps:
        for previous_cube, previous_cube_sign in signed_cubes.copy().items():
            intersect_cube = cube.intersect(previous_cube)
            if intersect_cube is not None:
                signed_cubes[intersect_cube] -= previous_cube_sign
        if instruction == Instruction.ON:
            signed_cubes[cube] += 1

    on_points = sum((cube.volume * sign) for cube, sign in signed_cubes.items())
    return on_points


def run() -> None:
    step_input = read_file()

    init_procedure_steps = parse_steps(step_input, init_procedure_only=True)
    print(reboot(init_procedure_steps))

    full_steps = parse_steps(step_input, init_procedure_only=False)
    print(reboot(full_steps))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
