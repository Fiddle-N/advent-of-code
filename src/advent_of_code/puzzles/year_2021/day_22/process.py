"""
2021 Day 22

Consider a 3D grid of integer points. The points can either be on or off - all points are set to off at the start.
A sequence of steps define cuboids of points and an instruction to turn those points should be turned on or off.
Execute the steps in order and calculate the number of points that are on.

Part 1
Execute only the steps where the greatest point from the origin is no more than 50 units away.

Part 2
Execute all steps.

Solution
This solution uses the inclusion/exclusion principle.

Considering two cuboids A and B where the instructions are to turn both on,
then the number of on points are calculated as:
A + B - A∩B
.
The subtraction of the intersection is needed to avoid double-counting those points.

Extending to three cuboids A, B and C,
then the number of on points are calculated as:
A + B + C - A∩B - A∩C - B∩C + A∩B∩C
Subtraction of the double intersections are needed to avoid double-counting those points, as before.
But in doing so, any point in A∩B∩C ends up completely negated, as we have added three regions and subtracted three.
So we need to add back in A∩B∩C to avoid missing this region.

This alternating plus/minus pattern continues with each cuboid intersection.
Hence, each new intersection can be added in by recording the intersection with the opposite sign of the previous cuboid
recorded.

Considering two cuboids A and B where the instructions are to turn A on and B off,
then the number of on points are calculated as:
A - A∩B
.

Hence, an off instruction is identical to an on instruction, except that the volume of the off cuboid is not added in.


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
class Cuboid:
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
) -> list[tuple[Cuboid, Instruction]]:
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
                Cuboid(
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


def reboot(steps: list[tuple[Cuboid, Instruction]]) -> int:
    signed_cuboids = defaultdict(int)
    for cuboid, instruction in steps:
        for previous_cuboid, previous_cuboid_sign in signed_cuboids.copy().items():
            intersect_cuboid = cuboid.intersect(previous_cuboid)
            if intersect_cuboid is not None:
                signed_cuboids[intersect_cuboid] -= previous_cuboid_sign
        if instruction == Instruction.ON:
            signed_cuboids[cuboid] += 1

    on_points = sum((cuboid.volume * sign) for cuboid, sign in signed_cuboids.items())
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
