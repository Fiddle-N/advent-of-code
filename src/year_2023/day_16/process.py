import collections
import dataclasses
import enum
import functools
from typing import Self


@dataclasses.dataclass(frozen=True)
class Coords:
    x: int
    y: int

    def __add__(self, other: Self) -> Self:
        return Coords(self.x + other.x, self.y + other.y)


class Direction(enum.Enum):
    UPWARDS = enum.auto()
    RIGHTWARDS = enum.auto()
    DOWNWARDS = enum.auto()
    LEFTWARDS = enum.auto()


OFFSET_COORDS = {
    Direction.UPWARDS: Coords(0, -1),
    Direction.RIGHTWARDS: Coords(1, 0),
    Direction.DOWNWARDS: Coords(0, 1),
    Direction.LEFTWARDS: Coords(-1, 0),
}


@dataclasses.dataclass(frozen=True)
class BeamState:
    location: Coords
    direction: Direction


class ContraptionSpace(enum.Enum):
    EMPTY_SPACE = "."
    FORWARDS_DIAGONAL_MIRROR = "/"
    BACKWARDS_DIAGONAL_MIRROR = "\\"
    VERTICAL_SPLITTER = "|"
    HORIZONTAL_SPLITTER = "-"


FORWARDS_DIAGONAL_DIRECTIONS = {
    Direction.RIGHTWARDS: Direction.UPWARDS,
    Direction.UPWARDS: Direction.RIGHTWARDS,
    Direction.LEFTWARDS: Direction.DOWNWARDS,
    Direction.DOWNWARDS: Direction.LEFTWARDS,
}

BACKWARDS_DIAGONAL_DIRECTIONS = {
    Direction.RIGHTWARDS: Direction.DOWNWARDS,
    Direction.DOWNWARDS: Direction.RIGHTWARDS,
    Direction.LEFTWARDS: Direction.UPWARDS,
    Direction.UPWARDS: Direction.LEFTWARDS,
}


class Contraption:
    def __init__(self, contraption_input):
        self.contraption = {}
        contraption_rows = contraption_input.splitlines()
        self.width = len(contraption_rows[0])
        self.height = len(contraption_rows)
        for y, row in enumerate(contraption_rows):
            for x, space in enumerate(row):
                self.contraption[Coords(x, y)] = ContraptionSpace(space)

    @classmethod
    def read_file(cls):
        with open("input.txt") as f:
            return cls(f.read().strip())

    def _is_valid_coord(self, coord):
        return (0 <= coord.x < self.width) and (0 <= coord.y < self.height)

    @functools.cache
    def _get_next_beam_states(self, beam_state):
        direction = beam_state.direction
        location = beam_state.location + OFFSET_COORDS[direction]
        if not self._is_valid_coord(location):
            return []
        space = self.contraption[location]

        match (space, direction):
            case (
                (ContraptionSpace.EMPTY_SPACE, _)
                | (
                    ContraptionSpace.HORIZONTAL_SPLITTER,
                    (Direction.LEFTWARDS | Direction.RIGHTWARDS),
                )
                | (
                    ContraptionSpace.VERTICAL_SPLITTER,
                    (Direction.UPWARDS | Direction.DOWNWARDS),
                )
            ):
                # beam passes through as normal
                return [BeamState(location=location, direction=direction)]
            case ContraptionSpace.HORIZONTAL_SPLITTER, (
                Direction.UPWARDS
                | Direction.DOWNWARDS
            ):
                return [
                    BeamState(location=location, direction=next_direction)
                    for next_direction in (Direction.LEFTWARDS, Direction.RIGHTWARDS)
                ]
            case ContraptionSpace.VERTICAL_SPLITTER, (
                Direction.LEFTWARDS
                | Direction.RIGHTWARDS
            ):
                return [
                    BeamState(location=location, direction=next_direction)
                    for next_direction in (Direction.UPWARDS, Direction.DOWNWARDS)
                ]
            case ContraptionSpace.FORWARDS_DIAGONAL_MIRROR, _:
                return [
                    BeamState(
                        location=location,
                        direction=FORWARDS_DIAGONAL_DIRECTIONS[direction],
                    )
                ]
            case ContraptionSpace.BACKWARDS_DIAGONAL_MIRROR, _:
                return [
                    BeamState(
                        location=location,
                        direction=BACKWARDS_DIAGONAL_DIRECTIONS[direction],
                    )
                ]
            case _:
                raise ValueError("Unhandled space/direction case")

    def simulate_beam(
        self, init_location=Coords(-1, 0), init_direction=Direction.RIGHTWARDS
    ):
        # init locations do not exist on the grid
        # but is used to model where the beam is originating from
        init_beam_state = BeamState(location=init_location, direction=init_direction)
        energised_spaces: dict[Coords, set[Direction]] = collections.defaultdict(set)
        beam_states = collections.deque([init_beam_state])
        while beam_states:
            beam_state = beam_states.pop()
            next_beam_states = self._get_next_beam_states(beam_state)

            for next_beam_state in next_beam_states:
                if (
                    next_beam_state.direction
                    in energised_spaces[next_beam_state.location]
                ):
                    # we've been here before
                    continue
                energised_spaces[next_beam_state.location].add(
                    next_beam_state.direction
                )
                beam_states.appendleft(next_beam_state)
        return energised_spaces

    def best_configuration(self):
        left_starting_positions = [
            {"init_location": Coords(-1, y), "init_direction": Direction.RIGHTWARDS}
            for y in range(self.height)
        ]
        right_starting_positions = [
            {
                "init_location": Coords(self.width, y),
                "init_direction": Direction.LEFTWARDS,
            }
            for y in range(self.height)
        ]
        top_starting_positions = [
            {"init_location": Coords(x, -1), "init_direction": Direction.DOWNWARDS}
            for x in range(self.width)
        ]
        bottom_starting_positions = [
            {
                "init_location": Coords(x, self.height),
                "init_direction": Direction.UPWARDS,
            }
            for x in range(self.width)
        ]
        starting_positions = (
            left_starting_positions
            + right_starting_positions
            + top_starting_positions
            + bottom_starting_positions
        )
        results = []
        for start_params in starting_positions:
            result = self.simulate_beam(**start_params)
            tile_num = len(result)
            results.append((result, tile_num))

        best_result = max(results, key=lambda result_detail: result_detail[1])
        return best_result


def main() -> None:
    contraption = Contraption.read_file()
    top_left_energised_spaces = contraption.simulate_beam()
    top_left_tile_num = len(top_left_energised_spaces)
    print(
        "Number of tiles ending up being energised with beam entering from top-left:",
        top_left_tile_num,
    )
    best_config = contraption.best_configuration()
    _, best_tile_num = best_config
    print(
        "Number of tiles ending up being energised with beam entering from any edge:",
        best_tile_num,
    )


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
