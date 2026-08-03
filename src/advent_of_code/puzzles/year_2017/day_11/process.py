from enum import Enum

from advent_of_code.common import Coords, START_COORDS, read_file, timed_run


class HexDirection(Enum):
    NORTH = "n"
    NORTH_EAST = "ne"
    SOUTH_EAST = "se"
    SOUTH = "s"
    SOUTH_WEST = "sw"
    NORTH_WEST = "nw"


HEX_DIRECTION_TO_COORDS = {
    HexDirection.NORTH: Coords(0, -2),
    HexDirection.NORTH_EAST: Coords(1, -1),
    HexDirection.SOUTH_EAST: Coords(1, 1),
    HexDirection.SOUTH: Coords(0, 2),
    HexDirection.SOUTH_WEST: Coords(-1, 1),
    HexDirection.NORTH_WEST: Coords(-1, -1),
}


def parse_dirs(raw_dirs: str) -> list[HexDirection]:
    return [HexDirection(raw_dir) for raw_dir in raw_dirs.split(",")]


def hex_dist_to(location: Coords) -> int:
    # on a hexagonal grid, you must go at least as many steps
    # as the x offset of the location
    # that many steps can also represent up to that many steps
    # towards the y offset of the location
    # If there is still a y offset to cover, that is covered by
    # direct steps in the y-axis, of which each of those
    # steps is 2 units in the y direction
    x_travel = abs(location.x - START_COORDS.x)
    remaining_y_travel = (abs(location.y) - x_travel) // 2
    if remaining_y_travel < 0:
        remaining_y_travel = 0
    return x_travel + remaining_y_travel


def calculate_fewest_steps(dirs: list[HexDirection]) -> tuple[int, int]:
    curr = START_COORDS
    max_steps = 0
    for dir_ in dirs:
        dir_coords = HEX_DIRECTION_TO_COORDS[dir_]
        curr += dir_coords
        steps = hex_dist_to(curr)
        if steps > max_steps:
            max_steps = steps
    return steps, max_steps


def run():
    raw_dirs = read_file()
    dirs = parse_dirs(raw_dirs)
    print(calculate_fewest_steps(dirs))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
