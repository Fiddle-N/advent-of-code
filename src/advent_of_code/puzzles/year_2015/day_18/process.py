"""
2015 Day 18

Part 1
Conway's Game of Life - calculate number of live cells (modelled as on lights below) after 100 simulations.

Part 2
Part 1 but the corner pixels are stuck on/live.
"""

import enum
from collections.abc import Iterator
from typing import Self

from advent_of_code.common import Coords, read_file, timed_run


NEIGHBOUR_COORDS = [
    Coords(1, 0),
    Coords(1, 1),
    Coords(0, 1),
    Coords(-1, 1),
    Coords(-1, 0),
    Coords(-1, -1),
    Coords(0, -1),
    Coords(1, -1),
]


class LightState(enum.Enum):
    ON = "#"
    OFF = "."


class ConwaysGameOfLife:
    def __init__(
        self, lights: dict[Coords, LightState], grid_length: int, grid_width: int
    ):
        self.lights = lights
        self.grid_length = grid_length
        self.grid_width = grid_width

    @classmethod
    def parse_grid(cls, grid_text: str) -> Self:
        grid_list = grid_text.splitlines()
        grid_length = len(grid_list)
        grid_width = len(grid_list[0])
        lights: dict[Coords, LightState] = {}
        for y, row in enumerate(grid_text.splitlines()):
            for x, light in enumerate(row):
                lights[Coords(x, y)] = LightState(light)
        return cls(lights, grid_length, grid_width)

    def simulate_animation(
        self, stuck_corners: bool = False
    ) -> Iterator[dict[Coords, LightState]]:
        lights = self.lights.copy()
        if stuck_corners:
            corners = [
                Coords(0, 0),
                Coords(self.grid_width - 1, 0),
                Coords(0, self.grid_length - 1),
                Coords(self.grid_width - 1, self.grid_length - 1),
            ]
            for corner in corners:
                lights[corner] = LightState.ON
        while True:
            new_lights: dict[Coords, LightState] = {}
            for light_coord, light_state in lights.items():
                if stuck_corners and light_coord in corners:
                    new_lights[light_coord] = LightState.ON
                    continue
                neighbour_coords = [
                    (light_coord + neighbour_coord)
                    for neighbour_coord in NEIGHBOUR_COORDS
                ]
                neighbour_light_states = [
                    lights.get(neighbour_coord, LightState.OFF)
                    for neighbour_coord in neighbour_coords
                ]
                on_neighbours = len(
                    [
                        neighbour_light_state
                        for neighbour_light_state in neighbour_light_states
                        if neighbour_light_state == LightState.ON
                    ]
                )
                new_light_state = (
                    LightState.ON
                    if (on_neighbours == 2 and light_state == LightState.ON)
                    or on_neighbours == 3
                    else LightState.OFF
                )
                new_lights[light_coord] = new_light_state
            yield new_lights
            lights = new_lights


def calculate_on_lights(lights: dict[Coords, LightState]) -> int:
    return len(
        [light_state for light_state in lights.values() if light_state == LightState.ON]
    )


def run():
    grid_text = read_file()
    cgl = ConwaysGameOfLife.parse_grid(grid_text)

    animation_simulator = cgl.simulate_animation()
    for _ in range(100):
        next_lights = next(animation_simulator)
    print(calculate_on_lights(next_lights))

    animation_simulator = cgl.simulate_animation(stuck_corners=True)
    for _ in range(100):
        next_lights = next(animation_simulator)
    print(calculate_on_lights(next_lights))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
