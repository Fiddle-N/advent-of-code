import dataclasses
import itertools

import timeit

ACTIVE = "#"
INACTIVE = "."


@dataclasses.dataclass(frozen=True)
class Coord:
    x: int
    y: int
    z: int
    w: int = 0

    def __add__(self, other):
        return Coord(
            self.x + other.x, self.y + other.y, self.z + other.z, self.w + other.w
        )


class PocketDimension:
    def __init__(self, coords):
        self.cubes = coords

    @classmethod
    def from_input(cls, state_input):
        coords = {}
        for (z, w), xy_grid in state_input.items():
            for y, row in enumerate(xy_grid.split("\n")):
                for x, cube in enumerate(row):
                    coords[Coord(x, y, z, w)] = cube
        return cls(coords)

    @classmethod
    def from_file(cls):
        with open("input.txt") as f:
            state_input = {(0, 0): f.read().strip()}
            return cls.from_input(state_input)

    def __eq__(self, other):
        active_cubes = {coord for coord, cube in self.cubes.items() if cube == ACTIVE}
        other_active_cubes = {
            coord for coord, cube in other.cubes.items() if cube == ACTIVE
        }
        return active_cubes == other_active_cubes


class PocketDimensionModel:
    def __init__(self, pocket_dimension, dimension_no=3):
        self.dimension = self.initial_dimension = pocket_dimension
        self.dimension_no = dimension_no

    def __iter__(self):
        return self

    def __next__(self):
        cubes = self.dimension.cubes
        active_cubes = {coord: cube for coord, cube in cubes.items() if cube == ACTIVE}
        next_coords = set()
        for coord, cube in active_cubes.items():
            for direction in self._directions:
                neighbour = coord + direction
                next_coords.add(neighbour)

        next_cubes = {}
        for coord in next_coords:
            cube = cubes.get(coord, INACTIVE)
            neighbour_cubes = []
            for direction in self._directions:
                neighbour = coord + direction
                neighbour_cube = cubes.get(neighbour, INACTIVE)
                neighbour_cubes.append(neighbour_cube)
            active_neighbour_cubes = [
                cube for cube in neighbour_cubes if cube == ACTIVE
            ]
            if (cube == ACTIVE and len(active_neighbour_cubes) in (2, 3)) or (
                cube == INACTIVE and len(active_neighbour_cubes) == 3
            ):
                next_cube = ACTIVE
            else:
                next_cube = INACTIVE
            next_cubes[coord] = next_cube
        self.dimension = PocketDimension(next_cubes)
        return self.dimension

    @property
    def _directions(self):
        dimension_params = [-1, 0, 1]
        no_change = (0,) * self.dimension_no
        return [
            Coord(*coords)
            for coords in itertools.product(dimension_params, repeat=self.dimension_no)
            if coords != no_change
        ]


def run_model(pocket_dimension, dimension_no, cycles):
    model = PocketDimensionModel(pocket_dimension, dimension_no)
    for _ in range(cycles):
        next_pocket_dimension = next(model)
    active_cubes = len(
        [coord for coord, cube in next_pocket_dimension.cubes.items() if cube == ACTIVE]
    )
    return active_cubes


def main():
    pocket_dimension = PocketDimension.from_file()
    print(
        f"Number of active cubes after 6th cycle in 3D model: {run_model(pocket_dimension, dimension_no=3, cycles=6)}"
    )
    print(
        f"Number of active cubes after 6th cycle in 4D model: {run_model(pocket_dimension, dimension_no=4, cycles=6)}"
    )


if __name__ == "__main__":
    print(f"Completed in {timeit.timeit(main, number=1)} seconds")
