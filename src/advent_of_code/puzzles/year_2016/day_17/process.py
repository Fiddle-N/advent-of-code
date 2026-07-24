import hashlib
from collections import deque
from dataclasses import dataclass

from advent_of_code.common import (
    Coords,
    Direction,
    FOUR_POINT_DIRECTION_TO_COORDS,
    DIRECTION_TO_DIRECTION_LETTER,
    read_file,
    timed_run,
)

MIN_AXIS_VAL = 0
MAX_AXIS_VAL = 3

START = Coords(MIN_AXIS_VAL, MIN_AXIS_VAL)
TARGET = Coords(MAX_AXIS_VAL, MAX_AXIS_VAL)

HASH_DIRECTIONS = [
    Direction.UP,
    Direction.DOWN,
    Direction.LEFT,
    Direction.RIGHT,
]

END_CLOSED_DOOR_RANGE = 10


@dataclass(frozen=True)
class LocationState:
    location: Coords
    path: bytes
    length: int


def find_vault(passcode: str) -> tuple[int | None, int | None]:
    passcode_bytes = passcode.encode()
    q = deque([LocationState(location=START, path=b"", length=0)])
    shortest_path = None
    longest_path_length = None
    while q:
        ls = q.pop()

        if ls.location == TARGET:
            if shortest_path is None:
                shortest_path = ls.path
            longest_path_length = ls.length
            continue

        hash_input = passcode_bytes + ls.path
        hash_output = hashlib.md5(hash_input).hexdigest()

        for dir_, dir_char in zip(HASH_DIRECTIONS, hash_output[:4]):
            next_location = ls.location + FOUR_POINT_DIRECTION_TO_COORDS[dir_]
            if (
                next_location.x < MIN_AXIS_VAL
                or next_location.x > MAX_AXIS_VAL
                or next_location.y < MIN_AXIS_VAL
                or next_location.y > MAX_AXIS_VAL
            ):
                continue
            dir_val = int(dir_char, base=16)
            if dir_val <= END_CLOSED_DOOR_RANGE:
                continue
            dir_letter = DIRECTION_TO_DIRECTION_LETTER[dir_]
            q.appendleft(
                LocationState(
                    location=next_location,
                    path=ls.path + dir_letter.encode(),
                    length=ls.length + 1,
                )
            )

    if shortest_path is not None:
        shortest_path = shortest_path.decode()

    return (shortest_path, longest_path_length)


def run():
    passcode = read_file()
    print(find_vault(passcode))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
