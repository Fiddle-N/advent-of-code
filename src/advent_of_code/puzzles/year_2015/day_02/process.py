"""
2015 Day 2

Part 1
Given dimensions of boxes in l*w*h format, calculate much wrapping paper is required to cover all boxes. Each box
requires wrapping paper to cover its surface area plus the area of the smallest side.

Part 2
Calculate how much ribbon is required to cover all boxes. Each box requires ribbon to cover its smallest perimeter face
plus ribbon equal to the value of the volume of the box.
"""

from dataclasses import dataclass
from advent_of_code.common import read_file


@dataclass
class Box:
    length: int
    width: int
    height: int


def parse_box_dimensions(dimension_str: str) -> Box:
    dimensions = dimension_str.split("x")
    return Box(*[int(dimension) for dimension in dimensions])


def calculate_wrapping_paper(box: Box) -> int:
    # wrapping paper required is the surface area plus the area of the smallest side
    sorted_sides = sorted([box.length, box.width, box.height])
    smallest_area = sorted_sides[0] * sorted_sides[1]
    surface_area = (
        2 * box.length * box.width
        + 2 * box.width * box.height
        + 2 * box.height * box.length
    )
    return surface_area + smallest_area


def calculate_ribbon(box: Box) -> int:
    # ribbon required is the smallest perimeter of any one face plus cubic volume
    sorted_sides = sorted([box.length, box.width, box.height])
    smallest_perimeter = 2 * (sorted_sides[0] + sorted_sides[1])
    volume = box.length * box.width * box.height
    return volume + smallest_perimeter


def main():
    dimension_text = read_file()
    boxes = [
        parse_box_dimensions(dimension) for dimension in dimension_text.splitlines()
    ]
    print(sum(calculate_wrapping_paper(box) for box in boxes))
    print(sum(calculate_ribbon(box) for box in boxes))


if __name__ == "__main__":
    main()
