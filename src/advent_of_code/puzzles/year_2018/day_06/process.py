from collections import defaultdict
from itertools import product
from operator import itemgetter

from advent_of_code.common import Coords, read_file, timed_run

SAFE_REGION_DISTANCE = 10000


def parse(raw_coords: str) -> list[Coords]:
    coords = []
    for raw_coord in raw_coords.splitlines():
        x, y = raw_coord.split(", ")
        coords.append(Coords(int(x), int(y)))
    return coords


def calculate_regions(
    coords: list[Coords], safe_region_distance: int
) -> tuple[int, int]:
    xs = [coord.x for coord in coords]
    ys = [coord.y for coord in coords]
    min_x = min(xs)
    max_x = max(xs)
    min_y = min(ys)
    max_y = max(ys)

    areas = defaultdict(int)
    infinite_area_coords = set()
    safe_region_size = 0
    for x, y in product(range(min_x, max_x + 1), range(min_y, max_y + 1)):
        distances = {coord: abs(coord.x - x) + abs(coord.y - y) for coord in coords}
        total_distance = sum(distances.values())
        if total_distance < safe_region_distance:
            safe_region_size += 1
        sorted_distances = sorted(distances.items(), key=itemgetter(1))
        if sorted_distances[0][1] == sorted_distances[1][1]:
            # equally closest to at least two coords - ignore
            continue
        nearest_coord = sorted_distances[0][0]  # retrieve closest coord
        areas[nearest_coord] += 1
        if x in (min_x, max_x) or y in (min_y, max_y):  # at edge of grid
            infinite_area_coords.add(nearest_coord)

    finite_areas = [
        area for coord, area in areas.items() if coord not in infinite_area_coords
    ]
    return max(finite_areas), safe_region_size


def run() -> None:
    raw_coords = read_file()
    coords = parse(raw_coords)
    print(calculate_regions(coords, safe_region_distance=SAFE_REGION_DISTANCE))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
