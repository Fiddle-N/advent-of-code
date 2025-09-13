"""
2015 Day 3

Part 1
Given directions of ^v<> representing movements on a 2D grid, find the number of unique positions including the starting
position.

Part 2
Find the number of unique positions if there are two people starting at the same place and each alternating on moving.
"""

from advent_of_code.common import read_file, Coords, Directions, DIRECTION_COORDS


def parse_directions(direction_str: str) -> list[Directions]:
    return [Directions(direction) for direction in direction_str]


def _visit_positions(directions: list[Directions]) -> set[Coords]:
    current = Coords(0, 0)
    visited = {current}
    for direction in directions:
        current += DIRECTION_COORDS[direction]
        visited.add(current)
    return visited


def count_positions_visited(directions: list[Directions]) -> int:
    return len(_visit_positions(directions))


def count_positions_visited_with_alternating_pair(directions: list[Directions]) -> int:
    return len(_visit_positions(directions[::2]) | _visit_positions(directions[1::2]))


def main() -> None:
    direction_text = read_file()
    directions = parse_directions(direction_text)
    print(count_positions_visited(directions))
    print(count_positions_visited_with_alternating_pair(directions))


if __name__ == "__main__":
    main()
