import collections
import dataclasses
import timeit


@dataclasses.dataclass(frozen=True)
class Coords:
    x: int
    y: int

    def __add__(self, other):
        return Coords(self.x + other.x, self.y + other.y)


class LobbyLayout:
    DIRECTIONS = {
        "e": Coords(2, 0),
        "w": Coords(-2, 0),
        "se": Coords(1, -2),
        "ne": Coords(1, 2),
        "sw": Coords(-1, -2),
        "nw": Coords(-1, 2),
    }

    REFERENCE = Coords(0, 0)

    def __init__(self, steps):
        self.steps = [self.parse_step(step) for step in steps.split("\n")]
        self.tile_map = {}

    @classmethod
    def from_file(cls):
        with open("input.txt") as f:
            return cls(f.read().strip())

    @staticmethod
    def parse_step(raw_step):
        step = []
        queue = collections.deque(raw_step)
        while queue:
            first_letter = queue.popleft()
            if first_letter in ("n", "s"):
                # diagonal direction
                second_letter = queue.popleft()
                direction = first_letter + second_letter
            else:
                # horizontal direction
                direction = first_letter
            step.append(direction)
        return step

    @property
    def black_tiles(self):
        return list(self.tile_map.values()).count("black")

    def process_steps(self):
        for step in self.steps:
            self._process_step(step)

    @classmethod
    def _calculate_position(cls, step):
        position = cls.REFERENCE
        for direction in step:
            position += cls.DIRECTIONS[direction]
        return position

    def _process_step(self, step):
        position = self._calculate_position(step)
        current_colour = self.tile_map.get(position, "white")
        if current_colour == "white":
            self.tile_map[position] = "black"
        elif current_colour == "black":
            self.tile_map[position] = "white"
        else:
            # unreachable
            raise Exception

    def flip(self, until_day):
        while True:
            min_x = min(self.tile_map, key=lambda coords: coords.x).x
            max_x = max(self.tile_map, key=lambda coords: coords.x).x
            min_y = min(self.tile_map, key=lambda coords: coords.y).y
            max_y = max(self.tile_map, key=lambda coords: coords.y).y

            # the furthest tiles to consider are one tile beyond the min and max tiles
            lower_x = min_x - 2
            upper_x = max_x + 2
            lower_y = min_y - 2
            upper_y = max_y + 2

            changes = {}

            for y in range(lower_y, upper_y + 1, 2):  # y coords have even numbers only
                for x in range(lower_x, upper_x):
                    if not ((y % 4 == 0 and x % 2 == 0) or (y % 4 == 2 and x % 2 == 1)):
                        # if y is multiple of 4, x must be even. if y is not multiple of 4, x must be odd.
                        # all other combinations are not valid hexagon coordinates in our system
                        continue
                    coords = Coords(x, y)
                    adjacent_coords = [
                        (coords + direction) for direction in self.DIRECTIONS.values()
                    ]
                    adjacent_black = [
                        self.tile_map.get(coords, "white") for coords in adjacent_coords
                    ]
                    coords_colour = self.tile_map.get(coords, "white")
                    adjacent_black_no = adjacent_black.count("black")
                    if coords_colour == "black" and (
                        adjacent_black_no == 0 or adjacent_black_no > 2
                    ):
                        changes[coords] = "white"
                    elif coords_colour == "white" and adjacent_black_no == 2:
                        changes[coords] = "black"

            self.tile_map.update(changes)
            yield self.black_tiles


def main():
    lobby_layout = LobbyLayout.from_file()
    lobby_layout.process_steps()
    print("Black tiles:", lobby_layout.black_tiles)

    iter_flip = lobby_layout.flip(until_day=100)
    black_tiles = None
    for _ in range(100):
        black_tiles = next(iter_flip)
    print("Black tiles after 100 flips:", black_tiles)


if __name__ == "__main__":
    print(f"Completed in {timeit.timeit(main, number=1)} seconds")
