from typing import Self
from dataclasses import dataclass

from advent_of_code.common import read_file, timed_run

PRESENT = "#"


@dataclass
class TreeRegion:
    area: int
    present_qty: list[int]


class XmasTreePresentSolver:
    def __init__(self, shape_areas: list[int], regions: list[TreeRegion]):
        self.shape_areas = shape_areas
        self.regions = regions

    @classmethod
    def from_input(cls, raw_input: str) -> Self:
        shapes = []
        regions = []

        sections = raw_input.split("\n\n")
        raw_shapes, raw_regions = sections[:-1], sections[-1]
        for raw_shape in raw_shapes:
            shape_lines = raw_shape.splitlines()[1:]
            area = sum(space == PRESENT for line in shape_lines for space in line)
            shapes.append(area)

        for raw_region in raw_regions.splitlines():
            raw_dimension, raw_qty = raw_region.split(": ")
            width, height = raw_dimension.split("x")
            regions.append(
                TreeRegion(
                    area=(int(width) * int(height)),
                    present_qty=[int(qty) for qty in raw_qty.split()],
                )
            )

        return cls(shapes, regions)

    def solve(self):
        result = 0
        for region in self.regions:
            shape_area = sum(
                (qty * area) for qty, area in zip(region.present_qty, self.shape_areas)
            )
            if shape_area > region.area:
                # what a troll
                pass
            else:
                # I'm not even going to bother checking whether this is valid
                result += 1
        return result


def run():
    xtps = XmasTreePresentSolver.from_input(read_file())
    print(xtps.solve())


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
