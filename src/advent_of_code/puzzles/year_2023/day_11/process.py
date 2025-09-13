import dataclasses
import itertools

GALAXY = "#"


@dataclasses.dataclass(frozen=True)
class Coords:
    x: int
    y: int


class Universe:
    def __init__(self, universe_input):
        universe = universe_input.splitlines()

        empty_ys = self._calc_empty_rows(universe)
        universe_transposed = [list(col) for col in zip(*universe)]
        empty_xs = self._calc_empty_rows(universe_transposed)
        self.empty_axes = {"x": empty_xs, "y": empty_ys}

        self.galaxies = {}
        galaxy_no = 0
        for y, row in enumerate(universe):
            for x, px in enumerate(row):
                if px != GALAXY:
                    continue
                galaxy_no += 1
                self.galaxies[galaxy_no] = Coords(x, y)

    def _calc_empty_rows(self, universe):
        empty_rows = set()
        for row_num, row in enumerate(universe):
            if GALAXY not in row:
                empty_rows.add(row_num)
        return empty_rows

    @classmethod
    def read_file(cls):
        with open("input.txt") as f:
            return cls(f.read().strip())

    def _manhatten_distance_single_axis(
        self, coords_1, coords_2, expansion_factor, axis
    ):
        pos_0, pos_1 = sorted([getattr(coords_1, axis), getattr(coords_2, axis)])
        inbetween_lines = len(
            [line for line in self.empty_axes[axis] if (pos_0 <= line <= pos_1)]
        )
        # to work out added distance, scale up lines by the expansion factor
        # but remove the original lines as these get replaced
        added_lines = (inbetween_lines * expansion_factor) - inbetween_lines
        dist = pos_1 - pos_0 + added_lines
        return dist

    def _manhatten_distance(self, coords_1, coords_2, expansion_factor):
        x_dist = self._manhatten_distance_single_axis(
            coords_1, coords_2, expansion_factor, axis="x"
        )
        y_dist = self._manhatten_distance_single_axis(
            coords_1, coords_2, expansion_factor, axis="y"
        )
        return x_dist + y_dist

    def galaxy_paths(self, expansion_factor=2):
        galaxy_paths = {}
        for galaxy_1, galaxy_2 in itertools.combinations(self.galaxies.items(), 2):
            galaxy_1_id, galaxy_1_coords = galaxy_1
            galaxy_2_id, galaxy_2_coords = galaxy_2
            distance = self._manhatten_distance(
                galaxy_1_coords, galaxy_2_coords, expansion_factor
            )
            galaxy_paths[frozenset([galaxy_1_id, galaxy_2_id])] = distance
        return galaxy_paths


def main() -> None:
    universe = Universe.read_file()
    print(
        "Sum of all galaxy shortest path lengths with universe expansion factor 2:",
        sum(universe.galaxy_paths().values()),
    )
    print(
        "Sum of all galaxy shortest path lengths with universe expansion factor 1,000,000:",
        sum(universe.galaxy_paths(expansion_factor=1_000_000).values()),
    )


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
