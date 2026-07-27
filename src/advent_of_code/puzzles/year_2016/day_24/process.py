from enum import Enum
from collections import defaultdict, deque
from dataclasses import dataclass, field
from itertools import combinations
from heapq import heappush, heappop

from advent_of_code.common import (
    read_file,
    timed_run,
    Coords,
    FOUR_POINT_DIRECTION_COORDS,
    ones_mask,
    iter_bits,
)

START = 0


class Space(Enum):
    EMPTY = "."
    WALL = "#"


@dataclass
class Maze:
    grid: dict[Coords, Space]
    start: Coords
    locations: dict[int, Coords]


@dataclass(frozen=True)
class ShortestPairState:
    steps: int
    location: Coords


@dataclass(frozen=True, order=True)
class ShortestLocationState:
    steps: int
    location: int = field(compare=False)
    state: int = field(compare=False)


def parse_maze(raw_maze: str) -> Maze:
    grid = {}
    locations = {}
    for y, row in enumerate(raw_maze.splitlines()):
        for x, raw_space in enumerate(row):
            location = Coords(x, y)
            try:
                label = int(raw_space)
            except ValueError:
                # not a location to visit
                space = Space(raw_space)
            else:
                # location to visit
                locations[label] = location
                if label == START:
                    start = location
                space = Space.EMPTY
            finally:
                grid[location] = space
    return Maze(grid, start, locations)


def _calculate_shortest_pair(maze: Maze, start: Coords, target: Coords) -> int:
    q = deque([ShortestPairState(0, start)])
    visited = {start}
    while q:
        sps = q.pop()
        next_steps = sps.steps + 1
        for offset in FOUR_POINT_DIRECTION_COORDS:
            next_location = sps.location + offset
            if next_location == target:
                return next_steps
            if next_location not in maze.grid:
                continue
            next_space = maze.grid[next_location]
            if next_space == Space.WALL:
                continue
            if next_location in visited:
                continue
            visited.add(next_location)
            q.appendleft(ShortestPairState(next_steps, next_location))
    raise ValueError("Result must be present")


def calculate_shortest_pairs(maze: Maze) -> dict[int, dict[int, int]]:
    shortest_pairs = defaultdict(dict)
    for (label_0, location_0), (label_1, location_1) in combinations(
        maze.locations.items(), 2
    ):
        shortest_pair = _calculate_shortest_pair(
            maze, start=location_0, target=location_1
        )
        shortest_pairs[label_0][label_1] = shortest_pair
        shortest_pairs[label_1][label_0] = shortest_pair
    return shortest_pairs


def calculate_shortest_route(
    maze: Maze, shortest_pairs: dict[int, dict[int, int]], return_to_start: bool = False
) -> int:
    n_locations = len(maze.locations)

    # use mask of 1s as state
    # flip 1 to 0 each time a location is visited
    # if not returning to start, flip start bit already
    starting_state = (
        ones_mask(n_locations) - 1 if not return_to_start else ones_mask(n_locations)
    )

    pq: list[ShortestLocationState] = []
    seen = {(starting_state, 0): 0}
    heappush(pq, ShortestLocationState(0, 0, starting_state))
    while pq:
        sls = heappop(pq)
        if not sls.state:
            return sls.steps
        for next_location_bits in iter_bits(sls.state):
            next_location = next_location_bits.bit_length() - 1
            if next_location == START and sls.state != 2**START:
                # only consider going to start
                # when it is the last place to visit
                continue
            dist = shortest_pairs[sls.location][next_location]
            total_dist = sls.steps + dist
            next_state = sls.state & ~next_location_bits

            if (next_state, next_location) in seen and total_dist > seen[
                (next_state, next_location)
            ]:
                continue
            else:
                seen[(next_state, next_location)] = total_dist
                heappush(
                    pq,
                    ShortestLocationState(total_dist, next_location, next_state),
                )

    raise ValueError("Result must be present")


def run() -> None:
    raw_maze = read_file()
    maze = parse_maze(raw_maze)
    shortest_pairs = calculate_shortest_pairs(maze)
    shortest_route = calculate_shortest_route(
        maze, shortest_pairs, return_to_start=False
    )
    print(shortest_route)
    shortest_route_back_to_start = calculate_shortest_route(
        maze, shortest_pairs, return_to_start=True
    )
    print(shortest_route_back_to_start)


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
