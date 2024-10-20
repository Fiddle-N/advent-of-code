import operator
import re
from dataclasses import dataclass
from typing import Self


@dataclass(frozen=True)
class Coords:
    x: int
    y: int

    def __add__(self, other: Self) -> Self:
        return Coords(self.x + other.x, self.y + other.y)


OFFSET_COORDS = [
    Coords(-1, -1),
    Coords(-1, 0),
    Coords(-1, 1),
    Coords(0, 1),
    Coords(0, -1),
    Coords(1, -1),
    Coords(1, 0),
    Coords(1, 1),
]

GEAR = '*'


class EngineSchematic:

    def __init__(self, schematic_text):
        # parse text into number and symbol locations
        self.numbers = {}
        self.symbols = {}
        for line_no, line in enumerate(schematic_text.splitlines()):
            numbers_match = re.finditer(r'\d+', line)
            for number_match in numbers_match:
                number_coords_range = (
                    Coords(line_no, number_match.start()),
                    Coords(line_no, number_match.end()),
                )
                self.numbers[number_coords_range] = int(number_match.group())
            symbols_match = re.finditer(r'[^\d.]', line)
            for symbol_match in symbols_match:
                self.symbols[Coords(line_no, symbol_match.start())] = symbol_match.group()

        # for convenience, expand coord ranges into individual coords with a map to their range
        # to allow for easier lookup of numbers
        self._expanded_coord_range = {}
        for coord_range in self.numbers:
            start_coord, end_coord = coord_range
            y_range = range(start_coord.y, end_coord.y)
            for y in y_range:
                self._expanded_coord_range[Coords(start_coord.x, y)] = coord_range

        # generate parts and gear parts collection
        self.parts = []
        self.gear_parts = []
        for symbol_coord, symbol in self.symbols.items():
            surrounding_num_ranges = set()  # use a set to ensure we don't count a number more than once
            for offset_coord in OFFSET_COORDS:
                adjacent_coord = symbol_coord + offset_coord
                if adjacent_coord in self._expanded_coord_range:
                    coord_range = self._expanded_coord_range[adjacent_coord]
                    surrounding_num_ranges.add(coord_range)
            for num_range in surrounding_num_ranges:
                part = self.numbers[num_range]
                self.parts.append(part)
            if symbol == GEAR and len(surrounding_num_ranges) == 2:
                self.gear_parts.append(
                    tuple(self.numbers[num_range] for num_range in surrounding_num_ranges)
                )

    @classmethod
    def read_file(cls) -> Self:
        with open("input.txt") as f:
            return cls(f.read())


def calculate_gear_ratios(gear_parts):
    return [operator.mul(*gear_part) for gear_part in gear_parts]


def main() -> None:
    schematic = EngineSchematic.read_file()
    print(
        "Sum of all part numbers in engine schematic:",
        sum(schematic.parts),
    )
    print(
        "Sum of all gear ratios in engine schematic:",
        sum(calculate_gear_ratios(schematic.gear_parts)),
    )


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
