from enum import StrEnum
from typing import Self
from advent_of_code.common import read_file, timed_run, Coords


EMPTY = "."


class SeaCucumber(StrEnum):
    SOUTH_FACING = "v"
    EAST_FACING = ">"


OFFSETS = {
    SeaCucumber.SOUTH_FACING: Coords(0, 1),
    SeaCucumber.EAST_FACING: Coords(1, 0),
}


class Map:
    def __init__(self, tiles: dict[Coords, SeaCucumber], length: int, width: int):
        self.tiles = tiles
        self.length = length
        self.width = width

    def __str__(self) -> str:
        grid = []
        for y in range(self.length):
            row = []
            for x in range(self.width):
                space = self.tiles.get(Coords(x, y))
                row.append(space if space is not None else EMPTY)
            grid.append("".join(row))
        return "\n".join(grid)

    @classmethod
    def from_text(cls, grid: str) -> Self:
        grid_list = grid.splitlines()
        map_ = {}
        for y, row in enumerate(grid_list):
            for x, point in enumerate(row):
                if point == EMPTY:
                    continue
                map_[Coords(x, y)] = SeaCucumber(point)
        return cls(map_, length=len(grid_list), width=len(grid_list[0]))


def move(map_instance: Map, location: Coords, offset: Coords) -> Coords:
    new_location = location + offset
    return Coords(
        x=new_location.x % map_instance.width, y=new_location.y % map_instance.length
    )


def _simulate_herd_movement(current_map: Map, cucumber_type: SeaCucumber) -> Map:
    moved_map = {}

    for coord, cucumber in current_map.tiles.items():
        if cucumber == cucumber_type:
            next_location = move(current_map, coord, OFFSETS[cucumber])

            if next_location not in current_map.tiles:
                moved_map[next_location] = cucumber
            else:
                moved_map[coord] = cucumber
        else:
            moved_map[coord] = cucumber

    return Map(moved_map, current_map.length, current_map.width)


def simulate_movement(map_instance: Map) -> int:
    initial_map = map_instance
    current_map = initial_map
    count = 0
    while True:
        count += 1
        east_facing_move_map = _simulate_herd_movement(
            current_map, SeaCucumber.EAST_FACING
        )
        all_moved_map = _simulate_herd_movement(
            east_facing_move_map, SeaCucumber.SOUTH_FACING
        )

        if initial_map.tiles == all_moved_map.tiles:
            return count

        current_map = all_moved_map
        initial_map = all_moved_map


def run() -> None:
    grid = read_file()
    map_ = Map.from_text(grid)
    print(simulate_movement(map_))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
