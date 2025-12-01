from typing import Literal

from advent_of_code.common import read_file, timed_run

STARTING_POSITION = 50
DIAL_SIZE = 100


def parse(raw_rotations: str) -> list[int]:
    rotations = []
    for rotation in raw_rotations.splitlines():
        direction, distance = rotation[0], int(rotation[1:])
        assert direction in ["L", "R"]
        if direction == "L":
            distance = -distance
        rotations.append(distance)
    return rotations


def execute_instructions(
    rotations: list[int], mode: Literal["original", "click"]
) -> int:
    position = STARTING_POSITION
    zero_visited = 0
    for rotation in rotations:
        sign = -1 if rotation < 0 else 1
        distance = abs(rotation)
        for i in range(distance):
            offset = position + sign
            position = offset % DIAL_SIZE
            if position == 0 and (mode == "click" or (i == distance - 1)):
                zero_visited += 1

    return zero_visited


def run():
    raw_rotations = read_file()
    rotations = parse(raw_rotations)
    print(execute_instructions(rotations, mode="original"))
    print(execute_instructions(rotations, mode="click"))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
