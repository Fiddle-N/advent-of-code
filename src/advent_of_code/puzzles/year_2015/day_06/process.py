"""
2015 Day 6

Consider a 2D grid of points representing individual lights. Each light has a brightness - all lights are set to off
at the start. A sequence of steps define rectangles of points and an instruction to turn those points on or off, or to
toggle them. Execute the steps in order and calculate the total brightness.

Part 1
Each light has a fixed brightness. They can be turned on, off, or toggled (on if off, off if on).

Part 2
Each light has a variable brightness. An on instruction turns them up by 1, a toggle instruction turns them up by 2,
and an off instructions turns them down by 1, unless they are completely off.

Solution
This solution uses brute force. A clever way to do Part 1 is to use the inclusion/exclusion principle, explained further
in 2021 Day 22. In this case, inclusion/exclusion is no faster than brute force because there are a large number of
intersections.
"""

import dataclasses
import enum
from collections.abc import Callable
from typing import Self
from collections import defaultdict
from advent_of_code.common import read_file, Coords, timed_run

import parse

STEP_TEMPLATE = "{instruction} {x_start:d},{y_start:d} through {x_end:d},{y_end:d}"


class Instruction(enum.Enum):
    ON = enum.auto()
    OFF = enum.auto()
    TOGGLE = enum.auto()


INSTRUCTION_MAP = {
    "turn on": Instruction.ON,
    "turn off": Instruction.OFF,
    "toggle": Instruction.TOGGLE,
}


@dataclasses.dataclass(frozen=True, eq=True)
class Rectangle:
    start: Coords
    end: Coords

    def intersect(self, other) -> Self | None:
        x_lower = max(self.start.x, other.start.x)
        x_upper = min(self.end.x, other.end.x)
        y_lower = max(self.start.y, other.start.y)
        y_upper = min(self.end.y, other.end.y)
        if x_lower <= x_upper and y_lower <= y_upper:
            return type(self)(
                start=Coords(x_lower, y_lower),
                end=Coords(x_upper, y_upper),
            )
        return None

    @property
    def volume(self) -> int:
        return (self.end.x - self.start.x + 1) * (self.end.y - self.start.y + 1)


def parse_steps(step_input: str) -> list[tuple[Rectangle, Instruction]]:
    steps = []
    for raw_step in step_input.splitlines():
        parsed_step = parse.parse(STEP_TEMPLATE, raw_step)

        steps.append(
            (
                Rectangle(
                    start=Coords(
                        parsed_step["x_start"],
                        parsed_step["y_start"],
                    ),
                    end=Coords(
                        parsed_step["x_end"],
                        parsed_step["y_end"],
                    ),
                ),
                INSTRUCTION_MAP[parsed_step["instruction"]],
            )
        )
    return steps


def execute_fixed_brightness(
    points: dict[Coords, int], point: Coords, instruction: Instruction, brightness: int
) -> None:
    match (instruction, brightness):
        case Instruction.ON, 0:
            points[point] = 1
        case Instruction.OFF, 1:
            points[point] = 0
        case Instruction.TOGGLE, 0:
            points[point] = 1
        case Instruction.TOGGLE, 1:
            points[point] = 0


def execute_variable_brightness(
    points: dict[Coords, int], point: Coords, instruction: Instruction, brightness: int
) -> None:
    match instruction:
        case Instruction.ON:
            points[point] += 1
        case Instruction.TOGGLE:
            points[point] += 2
        case Instruction.OFF if brightness > 0:
            points[point] -= 1


def execute_brightness_steps(
    steps: list[tuple[Rectangle, Instruction]],
    brightness_callback: Callable[[dict[Coords, int], Coords, Instruction, int], None],
) -> int:
    points = defaultdict(int)
    for rectangle, instruction in steps:
        for x in range(rectangle.start.x, rectangle.end.x + 1):
            for y in range(rectangle.start.y, rectangle.end.y + 1):
                point = Coords(x, y)
                brightness = points[point]
                brightness_callback(points, point, instruction, brightness)
    return sum(points.values())


def run() -> None:
    step_input = read_file()

    steps = parse_steps(step_input)
    print(execute_brightness_steps(steps, execute_fixed_brightness))
    print(execute_brightness_steps(steps, execute_variable_brightness))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
