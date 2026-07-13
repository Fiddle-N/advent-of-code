from itertools import batched

from advent_of_code.common import (
    read_file,
    timed_run,
)


def parse_triangles(raw_triangles: str) -> list[tuple[int, int, int]]:
    triangles = []
    for raw_triangle in raw_triangles.splitlines():
        triangle = tuple(int(side) for side in raw_triangle.strip().split())
        assert len(triangle) == 3
        triangles.append(triangle)
    return triangles


def parse_triangles_vertically(raw_triangles: str) -> list[tuple[int, int, int]]:
    triangles = []
    for t_chunk in batched(raw_triangles.splitlines(), 3, strict=True):
        t_triangles = [[int(side) for side in line.strip().split()] for line in t_chunk]
        chunk_triangles = list(zip(*t_triangles))
        triangles.extend(chunk_triangles)
    return triangles


def is_triangle(sides: tuple[int, int, int]) -> int:
    sorted_sides = sorted(sides)
    return (sorted_sides[0] + sorted_sides[1]) > sorted_sides[2]


def calculate_triangles(triangles: list[tuple[int, int, int]]) -> int:
    return sum([is_triangle(triangle) for triangle in triangles])


def run():
    raw_triangles = read_file()
    triangles = parse_triangles(raw_triangles)
    print(calculate_triangles(triangles))
    vertical_triangles = parse_triangles_vertically(raw_triangles)
    print(calculate_triangles(vertical_triangles))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
