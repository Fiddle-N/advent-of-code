import collections
import dataclasses
import enum
import itertools


@dataclasses.dataclass(frozen=True)
class Coords:
    x: int
    y: int

    def __add__(self, other):
        return Coords(self.x + other.x, self.y + other.y)


class Tile(enum.Enum):
    VERTICAL_PIPE = '|'
    HORIZONTAL_PIPE = '-'
    NORTH_EAST_90_DEGREE_BEND = 'L'
    NORTH_WEST_90_DEGREE_BEND = 'J'
    SOUTH_WEST_90_DEGREE_BEND = '7'
    SOUTH_EAST_90_DEGREE_BEND = 'F'
    GROUND = '.'
    STARTING_POSITION = 'S'


class Direction(enum.Enum):
    NORTH = enum.auto()
    EAST = enum.auto()
    SOUTH = enum.auto()
    WEST = enum.auto()


TILE_OUTBOUND_DIRS = {
    Tile.VERTICAL_PIPE: {Direction.NORTH, Direction.SOUTH},
    Tile.HORIZONTAL_PIPE: {Direction.WEST, Direction.EAST},
    Tile.NORTH_EAST_90_DEGREE_BEND: {Direction.NORTH, Direction.EAST},
    Tile.NORTH_WEST_90_DEGREE_BEND: {Direction.NORTH, Direction.WEST},
    Tile.SOUTH_WEST_90_DEGREE_BEND: {Direction.SOUTH, Direction.WEST},
    Tile.SOUTH_EAST_90_DEGREE_BEND: {Direction.SOUTH, Direction.EAST},
}

OPPOSITE_DIRS = {
    Direction.NORTH: Direction.SOUTH,
    Direction.SOUTH: Direction.NORTH,
    Direction.EAST: Direction.WEST,
    Direction.WEST: Direction.EAST,
}

DIRECTION_TO_COORDS = {
    Direction.NORTH: Coords(0, -1),
    Direction.EAST: Coords(1, 0),
    Direction.SOUTH: Coords(0, 1),
    Direction.WEST: Coords(-1, 0),
}

DIRECTION_COORDS = DIRECTION_TO_COORDS.values()

DIRECTION_COORDS_INCLUDING_DIAGONALS = list(DIRECTION_COORDS) + [
    Coords(1, -1),
    Coords(1, 1),
    Coords(-1, 1),
    Coords(-1, -1),
]


def _is_valid_coord(coord, max_x, max_y):
    return (0 <= coord.x <= max_x) and (0 <= coord.y <= max_y)


class Field:

    def __init__(self, field_input):
        self.start_coord = None
        self.grid = {}
        for y, row in enumerate(field_input.splitlines()):
            for x, tile_str in enumerate(row):
                tile_coords = Coords(x, y)
                tile = Tile(tile_str)
                self.grid[tile_coords] = tile
                if tile == Tile.STARTING_POSITION:
                    self.start_coord = tile_coords

        self.max_x = x
        self.max_y = y

        self.x_len = self.max_x + 1
        self.y_len = self.max_y + 1

        # calculate start tile
        start_tile = None
        start_surrounding_dirs = set()
        for dir_, dir_coord in DIRECTION_TO_COORDS.items():
            surrounding_coord = self.start_coord + dir_coord
            if not _is_valid_coord(surrounding_coord, self.max_x, self.max_y):
                continue
            returning_dir = OPPOSITE_DIRS[dir_]
            surrounding_tile = self.grid[surrounding_coord]
            if surrounding_tile == Tile.GROUND:
                continue
            if returning_dir in TILE_OUTBOUND_DIRS[surrounding_tile]:
                start_surrounding_dirs.add(dir_)
        for tile, dirs in TILE_OUTBOUND_DIRS.items():
            if dirs == start_surrounding_dirs:
                start_tile = tile
                break

        # place true start tile in grid
        self.grid[self.start_coord] = start_tile

        self.loop = self._calculate_loop()

    @classmethod
    def read_file(cls):
        with open("input.txt") as f:
            return cls(f.read().strip())

    def _get_next_dir(self, prev_dir, pos_coord):
        pos_tile = self.grid[pos_coord]
        next_dirs = TILE_OUTBOUND_DIRS[pos_tile].copy()
        dir_back_to_prev_tile = OPPOSITE_DIRS[prev_dir]
        next_dirs.remove(dir_back_to_prev_tile)
        assert len(next_dirs) == 1
        dir_ = next_dirs.pop()
        return dir_

    def _calculate_loop(self):
        pos_coord = self.start_coord
        path = [self.start_coord]
        start_tile = self.grid[pos_coord]
        dir_ = list(TILE_OUTBOUND_DIRS[start_tile])[0]        # arbitrarily choose any direction from start tile
        while True:
            dir_coords = DIRECTION_TO_COORDS[dir_]
            pos_coord += dir_coords
            if self.start_coord == pos_coord:
                break
            path.append(pos_coord)
            dir_ = self._get_next_dir(dir_, pos_coord)
        return path


def furthest_steps_from_start(field_path):
    """
    Simply count path length and divide by 2 to get the furthest number of steps away
    """
    quot, rem = divmod(len(field_path), 2)
    assert rem == 0
    return quot


def _is_coord_in_original_grid(coord):
    return (coord.x % 2 == 0) and (coord.y % 2 == 0)


def area_enclosed_within_the_loop(field):
    # enlarge graph by a factor of 2 in order to allow modelling space between pipes
    # fill in the extra space with ground for now
    enlarged_max_x = field.max_x * 2
    enlarged_max_y = field.max_y * 2
    enlarged_x_len = enlarged_max_x + 1
    enlarged_y_len = enlarged_max_y + 1

    enlarged_grid = {}
    for y in range(enlarged_y_len):
        for x in range(enlarged_x_len):
            enlarged_coord = Coords(x, y)
            enlarged_grid[enlarged_coord] = (
                field.grid[Coords(x // 2, y // 2)]
                if _is_coord_in_original_grid(enlarged_coord)
                else Tile.GROUND
            )

    # calculate enlarged loop
    # follow loop through and fill in gaps with their actual pipe tile
    enlarged_loop = []
    loop_pairs = itertools.pairwise(field.loop + field.loop[:1])     # add start element again to loop back to the beginning
    for coord_1, coord_2 in loop_pairs:
        coord_1_enlarged_x = coord_1.x * 2
        coord_1_enlarged_y = coord_1.y * 2
        coord_2_enlarged_x = coord_2.x * 2
        coord_2_enlarged_y = coord_2.y * 2

        is_x_equal = (coord_1_enlarged_x == coord_2_enlarged_x)
        is_y_equal = (coord_1_enlarged_y == coord_2_enlarged_y)
        assert is_x_equal != is_y_equal

        in_between_coord = (
            Coords(coord_1_enlarged_x, (coord_1_enlarged_y + coord_2_enlarged_y) // 2)
            if is_x_equal
            else Coords((coord_1_enlarged_x + coord_2_enlarged_x) // 2, coord_1_enlarged_y)
        )
        tile = Tile.VERTICAL_PIPE if is_x_equal else Tile.HORIZONTAL_PIPE

        enlarged_grid[in_between_coord] = tile
        enlarged_loop.extend([Coords(coord_1_enlarged_x, coord_1_enlarged_y), in_between_coord])

    # flood fill from inside to get all enclosed points
    # start from free points around the first part in the loop
    # at least one is guaranteed to be enclosed
    # the others are unenclosed if a flood fill hits a border

    def _is_border_point(point):
        return (
            (point.x in (0, enlarged_max_x))
            or (point.y in (0, enlarged_max_y))
        )

    enlarged_possibly_enclosed_start_points = []
    start_point = enlarged_loop[0]
    enlarged_loop_set = set(enlarged_loop)

    for dir_ in DIRECTION_COORDS_INCLUDING_DIAGONALS:
        surrounding_point = start_point + dir_
        if (
                _is_valid_coord(
                    surrounding_point, enlarged_max_x, enlarged_max_y
                )
                and not _is_border_point(surrounding_point)
                and surrounding_point not in enlarged_loop_set
        ):
            enlarged_possibly_enclosed_start_points.append(surrounding_point)

    # initiate flood fill
    # flood stops when it meets a place in the loop
    def _flood_fill(start):
        points = {start}
        points_to_check = collections.deque(points)
        while points_to_check:
            point = points_to_check.pop()
            for dir_coord in DIRECTION_COORDS:
                next_point = point + dir_coord
                if not _is_valid_coord(next_point, enlarged_max_x, enlarged_max_y):
                    continue
                if next_point in enlarged_loop_set:
                    continue
                if next_point in points:
                    continue
                if _is_border_point(next_point):
                    # the start point is ultimately part of an unenclosed area
                    return None
                points.add(next_point)
                points_to_check.appendleft(next_point)
        # no border points encountered - start point is part of an enclosed area
        return points

    enlarged_enclosed_points = None
    for flood_fill_start in enlarged_possibly_enclosed_start_points:
        flood_fill_result = _flood_fill(flood_fill_start)
        if flood_fill_result:
            enlarged_enclosed_points = flood_fill_result
            break
    assert enlarged_enclosed_points is not None

    # convert enclosed points back to original grid points
    enclosed_points = {
        Coords(point.x // 2, point.y // 2)
        for point in enlarged_enclosed_points
        if _is_coord_in_original_grid(point)
    }

    return enclosed_points


def main() -> None:
    field = Field.read_file()
    print(
        "Steps along loop to get to farthest position from starting position:",
        furthest_steps_from_start(field.loop),
    )
    print(
        "Number of tiles enclosed by the loop:",
        len(area_enclosed_within_the_loop(field)),
    )


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
