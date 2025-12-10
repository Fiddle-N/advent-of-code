from collections import defaultdict
from itertools import pairwise, combinations
from operator import itemgetter
from typing import Self

from advent_of_code.common import Coords, read_file, timed_run, merge_intervals


def area(a: Coords, b: Coords):
    return (abs(a.x - b.x) + 1) * (abs(a.y - b.y) + 1)


class Polygon:
    def __init__(
        self,
        coords: list[Coords],
        min_x: int,
        max_x: int,
        min_y: int,
        max_y: int,
    ) -> None:
        self.coords = coords
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y

    @classmethod
    def from_input(cls, raw_input: str) -> Self:
        min_x = None
        max_x = None
        min_y = None
        max_y = None
        coords = []
        for line in raw_input.splitlines():
            x, y = line.split(",")
            x = int(x)
            y = int(y)
            if min_x is None or x < min_x:
                min_x = x
            if max_x is None or x > max_x:
                max_x = x
            if min_y is None or y < min_y:
                min_y = y
            if max_y is None or y > max_y:
                max_y = y
            coords.append(Coords(x, y))
        return cls(coords, min_x, max_x, min_y, max_y)


def resolve(polygon: Polygon) -> tuple[int, int]:
    distances = [
        (tuple(sorted([a, b])), area(a, b)) for a, b in combinations(polygon.coords, 2)
    ]
    sorted_distances = sorted(distances, key=itemgetter(1), reverse=True)

    max_rectangle = sorted_distances[0][1]

    # largest rectangle within polygon
    vertical_walls = defaultdict(list)
    horizontal_walls = defaultdict(list)
    full_coords = polygon.coords.copy()
    full_coords.append(polygon.coords[0])
    for a, b in pairwise(full_coords):
        if a.y == b.y:
            horizontal_walls[a.y].append(tuple(sorted([a.x, b.x])))
        elif a.x == b.x:
            vertical_walls[a.x].append(tuple(sorted([a.y, b.y])))
    vertical_wall_xs = sorted(vertical_walls)

    y_ranges = defaultdict(list)
    for y in range(polygon.min_y, polygon.max_y + 1):
        walls_crossed = 0
        last_x = polygon.min_x
        for x in vertical_wall_xs:
            possible_wall = None
            wall_cross = False

            for vertical_wall in vertical_walls[x]:
                if vertical_wall[0] <= y <= vertical_wall[1]:
                    possible_wall = vertical_wall
                    break

            if possible_wall is None:
                continue

            if y in possible_wall:
                # only count this case if other y is below y
                other_y = (
                    possible_wall[1] if possible_wall[0] == y else possible_wall[0]
                )
                if other_y > y:
                    wall_cross = True
            else:
                # y between wall range
                wall_cross = True

            if wall_cross:
                walls_crossed += 1
                if walls_crossed != 0 and walls_crossed % 2 == 0:
                    # gone from inside to outside
                    y_ranges[y].append((last_x, x))
                last_x = x

    full_y_ranges = {
        y: merge_intervals(y_ranges[y] + horizontal_walls[y])
        for y in range(polygon.min_y, polygon.max_y + 1)
    }

    for (a, b), distance in sorted_distances:
        fully_inside = True
        y_start, y_end = sorted([a.y, b.y])
        for y in range(y_start, y_end + 1):
            if y not in full_y_ranges:
                fully_inside = False
                break
            y_intervals = full_y_ranges[y]
            if not any((a.x >= y_int[0] and b.x <= y_int[1]) for y_int in y_intervals):
                fully_inside = False
                break
        if fully_inside:
            max_rectangle_inside_polygon = distance
            break

    return (max_rectangle, max_rectangle_inside_polygon)


def run():
    p = Polygon.from_input(read_file())
    print(resolve(p))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
