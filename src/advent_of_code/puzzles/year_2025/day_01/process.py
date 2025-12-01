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
        distance = abs(rotation)

        sign = -1 if rotation < 0 else 1
        if sign == -1:
            # flip dial because negatives are hard
            position = (DIAL_SIZE - position) % DIAL_SIZE

        offset = position + distance

        full_rotations, position = divmod(offset, DIAL_SIZE)
        full_rotations = abs(full_rotations)

        if sign == -1:
            # reflip dial afterwards
            position = (DIAL_SIZE - position) % DIAL_SIZE

        if mode == "original" and position == 0:
            zero_visited += 1
        elif mode == "click":
            zero_visited += full_rotations
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
