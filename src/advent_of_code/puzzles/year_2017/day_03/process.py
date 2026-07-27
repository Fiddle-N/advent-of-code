from collections.abc import Iterator
from itertools import count, cycle, dropwhile, repeat

from advent_of_code.common import (
    Coords,
    Direction,
    FOUR_POINT_DIRECTION_TO_COORDS,
    EIGHT_POINT_DIRECTION_COORDS,
    read_file,
    timed_run,
)

START_SQUARE = 1
START_LOCATION = Coords(0, 0)

SPIRAL_ORDER = [Direction.RIGHT, Direction.UP, Direction.LEFT, Direction.DOWN]


def get_spiral_dist() -> Iterator[int]:
    for dist in count(start=1):
        yield from repeat(dist, 2)


def get_spiral_dir() -> Iterator[Direction]:
    yield from cycle(SPIRAL_ORDER)


def get_spiral_move() -> Iterator[tuple[int, Direction]]:
    yield from zip(get_spiral_dist(), get_spiral_dir())


def calculate_dist_to_square(target: int) -> int:
    square = START_SQUARE
    location = START_LOCATION
    for dist, dir_ in get_spiral_move():
        next_square = square + dist
        coord_offset = FOUR_POINT_DIRECTION_TO_COORDS[dir_]
        next_location = location + (coord_offset * dist)

        if square <= target <= next_square:
            square_offset = target - square
            target_location = location + (coord_offset * square_offset)
            break

        square = next_square
        location = next_location

    return START_LOCATION.manhattan_distance_to(target_location)


def execute_stress_test() -> Iterator[int]:
    location = START_LOCATION
    visited = {START_LOCATION: START_SQUARE}
    yield START_SQUARE
    for dist, dir_ in get_spiral_move():
        for _ in range(dist):
            coord_offset = FOUR_POINT_DIRECTION_TO_COORDS[dir_]
            location += coord_offset
            value = sum(
                visited.get(location + adj_offset, 0)
                for adj_offset in EIGHT_POINT_DIRECTION_COORDS
            )
            yield value
            visited[location] = value


def run():
    target = int(read_file())
    print(calculate_dist_to_square(target))
    print(next(dropwhile(lambda square: square <= target, execute_stress_test())))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
