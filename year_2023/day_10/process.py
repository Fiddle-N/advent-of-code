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


VERTEX_TILES = {
    Tile.NORTH_EAST_90_DEGREE_BEND,
    Tile.NORTH_WEST_90_DEGREE_BEND,
    Tile.SOUTH_WEST_90_DEGREE_BEND,
    Tile.SOUTH_EAST_90_DEGREE_BEND,
}


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

        self.loop_verts, self.loop_length = self._process_loop()

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

    def _process_loop(self):
        pos_coord = self.start_coord
        path = [self.start_coord]
        start_tile = self.grid[pos_coord]
        dir_ = list(TILE_OUTBOUND_DIRS[start_tile])[0]        # arbitrarily choose any direction from start tile
        for length in itertools.count(start=1):
            dir_coords = DIRECTION_TO_COORDS[dir_]
            pos_coord += dir_coords
            if self.start_coord == pos_coord:
                break
            pos_tile = self.grid[pos_coord]
            if pos_tile in VERTEX_TILES:
                path.append(pos_coord)
            dir_ = self._get_next_dir(dir_, pos_coord)
        return path, length


def enclosed_num_of_tiles(field: Field):
    # Given a list of loop vertices
    # we can find the full area of the enclosing space
    # using shoelace formula
    # where (x, y) -> (x', y') denotes an edge of the loop
    # A = abs(0.5 * (sum of all (x' - x) * (y' + y)))
    #
    # However, as the field is modelled as tiles
    # what we really need is the number of interior points
    # Pick's theorem gives the area
    # given the number of interior and boundary points
    # A = i + b/2 - 1
    # we can rearrange this to give us the number of interior points
    # given the full area
    # and the number of boundary points (which is just the loop length)
    # i = A - b/2 + 1
    loop_verts = field.loop_verts.copy()
    loop_verts.append(loop_verts[0])    # repeat start point to go back to the beginning
    pairwise_loop_points = itertools.pairwise(loop_verts)

    # shoelace formula
    area = abs(
        sum(
            [(p1.x - p2.x) * (p1.y + p2.y) for p1, p2 in pairwise_loop_points]
        ) // 2
    )

    # Pick's theorem in reverse
    interior_points = area - (field.loop_length // 2) + 1

    return interior_points


def main() -> None:
    field = Field.read_file()
    print(
        "Steps along loop to get to farthest position from starting position:",
        field.loop_length // 2,
    )
    print(
        "Number of tiles enclosed by the loop:",
        enclosed_num_of_tiles(field),
    )


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
