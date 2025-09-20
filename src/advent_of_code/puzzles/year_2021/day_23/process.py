"""
2021 Day 23

Amphipods live in a very specific burrow of side rooms (the amphipods are denoted by A B C D, empty space by ., walls
by #):
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########

They want to be rearranged like so:
#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########

Rules:
* Amphipods don't stop on the space outside a room:
* Amphipods don't move from the hallway into a room until there's a free space and only the right type of amphipod is in
that room
* Once an amphipod is in a hallway space, it moves nowhere until it can move into a room.

Amber amphipods require 1 energy per step, Bronze amphipods require 10 energy, Copper amphipods require 100,
and Desert ones require 1000.

Find the solution with the least energy.

Part 1
Map is like so, with two rows of amphipods to be solved:

#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########

Part 2
These lines are added in the middle of the grid:
  #D#C#B#A#
  #D#B#A#C#

making a map of four rows of amphipods to be solved:

#############
#...........#
###B#C#B#D###
  #D#C#B#A#
  #D#B#A#C#
  #A#D#C#A#
  #########

"""

import collections
import dataclasses
import enum
import functools
import typing
import itertools

AMPHIPODS_PER_ROW = 4


@dataclasses.dataclass(eq=True, frozen=True, order=True)
class Coords:
    x: int
    y: int

    def __add__(self, other):
        return Coords(self.x + other.x, self.y + other.y)


OFFSETS = [
    Coords(0, 1),
    Coords(1, 0),
    Coords(0, -1),
    Coords(-1, 0),
]


@dataclasses.dataclass(frozen=True)
class Location:
    coords: Coords
    distance: int


class BurrowMapSpace(enum.Enum):
    WALL = "#"
    HALLWAY = "."
    EMPTY = " "


class BurrowHallwayType(enum.Enum):
    OUTSIDE_ROOM = enum.auto()
    AWAY_FROM_ROOM = enum.auto()


class BurrowAmphipodState(enum.Enum):
    ORIGINAL = enum.auto()
    HALLWAY = enum.auto()
    SETTLED = enum.auto()


class AmphipodType(enum.Enum):
    AMBER = "A"
    BRONZE = "B"
    COPPER = "C"
    DESERT = "D"


AMPHIPOD_ENERGY = {
    AmphipodType.AMBER: 1,
    AmphipodType.BRONZE: 10,
    AmphipodType.COPPER: 100,
    AmphipodType.DESERT: 1000,
}


@dataclasses.dataclass(frozen=True)
class Amphipod:
    type: AmphipodType
    id: int


@dataclasses.dataclass(frozen=True)
class BurrowAmphipodSpace:
    type: AmphipodType
    id: int


@dataclasses.dataclass
class Node:
    this: typing.Union[BurrowHallwayType, BurrowAmphipodSpace]
    neighbours: list[Location]


def amphipod_generator_factory():
    counter = {amphipod_type: itertools.count() for amphipod_type in AmphipodType}

    def amphipod_generator(amphipod_type: AmphipodType):
        return Amphipod(amphipod_type, next(counter[amphipod_type]))

    return amphipod_generator


def burrow_amphipod_space_generator_factory():
    counter = {amphipod_type: itertools.count() for amphipod_type in AmphipodType}

    def burrow_amphipod_space_generator(amphipod_type: AmphipodType):
        return BurrowAmphipodSpace(amphipod_type, next(counter[amphipod_type]))

    return burrow_amphipod_space_generator


@dataclasses.dataclass(frozen=True, order=True)
class AmphipodConfiguration:
    energy: int
    amphipods: dict[Coords, Amphipod] = dataclasses.field(compare=False)
    amphipods_state: dict[Amphipod, BurrowAmphipodState] = dataclasses.field(
        compare=False
    )
    history: frozenset[tuple[Amphipod, Coords]] = dataclasses.field(
        default_factory=frozenset
    )

    @property
    def diagram(self):
        burrow_top = """\
#############
#...........#
### # # # ###"""

        burrow_mid_row = "  # # # # #  "

        burrow_bottom_row = "  #########  "

        burrow_middle = "\n".join(
            [burrow_mid_row] * ((len(self.amphipods) // AMPHIPODS_PER_ROW) - 1)
        )
        burrow = "\n".join([burrow_top, burrow_middle, burrow_bottom_row])

        base_diagram_list = [list(row) for row in burrow.splitlines()]

        for amphipod_coord, amphipod in self.amphipods.items():
            base_diagram_list[amphipod_coord.y][amphipod_coord.x] = amphipod.type.value

        return "\n".join(["".join(row) for row in base_diagram_list])


class BurrowMap:
    def __init__(self, burrow_map, amphipod_rows):
        self.map = burrow_map
        self.amphipod_rows = amphipod_rows
        self._amphipod_space_coords = self._calculate_amphipod_spaces()

    def _calculate_amphipod_spaces(self):
        coords = collections.defaultdict(dict)
        for coord, space in self.map.items():
            if isinstance(space.this, BurrowAmphipodSpace):
                coords[space.this.type][space.this.id] = coord
        return coords

    def get_amphipod_coords(self, amphipod_type: AmphipodType):
        return self._amphipod_space_coords[amphipod_type]

    def get_hallway_coords(self):
        return [
            coord
            for coord, node in self.map.items()
            if node.this == BurrowHallwayType.AWAY_FROM_ROOM
        ]

    @functools.cache
    def _path_coords(self, start: Coords, end: Coords):
        def dfs(space=start, path=None):
            if path is None:
                path = []
            path.append(space)
            if space == end:
                return path
            for neighbour in self.map[space].neighbours:
                assert neighbour.distance == 1
                neighbour_space = neighbour.coords
                if neighbour_space not in path:
                    if (next_path := dfs(neighbour_space, path.copy())) is not None:
                        # only return if we have a path that ends in our destination
                        return next_path

        d = dfs()
        return d

    @functools.cache
    def path_coords(self, start: Coords, end: Coords, exclude_start=False):
        path = self._path_coords(start, end)
        return path[1:] if exclude_start else path


class BurrowMapGenerator:
    BURROW_TOP = """\
#############
#...........#
###A#B#C#D###"""

    BURROW_MID_ROW = "  #A#B#C#D#  "

    BURROW_BOTTOM_ROW = "  #########  "

    def __init__(self, burrow_amphipod_space_gen):
        self.height = None
        self.width = None
        self.burrow_amphipod_space_gen = burrow_amphipod_space_gen

    def create(self, amphipod_rows):
        burrow_middle = "\n".join([self.BURROW_MID_ROW] * (amphipod_rows - 1))
        burrow = "\n".join([self.BURROW_TOP, burrow_middle, self.BURROW_BOTTOM_ROW])
        burrow_grid = self._generate_grid(burrow)
        self.height = len(burrow_grid)
        self.width = len(burrow_grid[0])
        burrow_map = self._generate_map(burrow_grid)
        return BurrowMap(burrow_map, amphipod_rows)

    def get_neighbours(self, coord):
        neighbour_coords = []
        for offset in OFFSETS:
            neighbour_coord = coord + offset
            if (
                0 <= neighbour_coord.x < self.width
                and 0 <= neighbour_coord.y < self.height
            ):
                neighbour_coords.append(neighbour_coord)
        return neighbour_coords

    def _generate_grid(self, burrow):
        burrow_grid = []
        for row in burrow.splitlines():
            list_row = []
            for raw_space in row:
                try:
                    space = AmphipodType(raw_space)
                except ValueError:
                    space = BurrowMapSpace(raw_space)
                list_row.append(space)
            burrow_grid.append(list_row)
        return burrow_grid

    def _generate_map(self, burrow_preprocessed):
        burrow_map = {}
        for y, row in enumerate(burrow_preprocessed):
            for x, space in enumerate(row):
                coord = Coords(x, y)
                if space in (BurrowMapSpace.WALL, BurrowMapSpace.EMPTY):
                    continue

                neighbour_coords_including_walls = self.get_neighbours(coord)
                neighbour_coords = [
                    coord
                    for coord in neighbour_coords_including_walls
                    if burrow_preprocessed[coord.y][coord.x] != BurrowMapSpace.WALL
                ]
                neighbour_nodes = [
                    Location(coord, distance=1) for coord in neighbour_coords
                ]
                if space == BurrowMapSpace.HALLWAY:
                    node_val = (
                        BurrowHallwayType.OUTSIDE_ROOM
                        if len(neighbour_nodes) == 3
                        else BurrowHallwayType.AWAY_FROM_ROOM
                    )
                elif space in AmphipodType:
                    node_val = self.burrow_amphipod_space_gen(space)
                else:
                    raise Exception
                node = Node(node_val, neighbour_nodes)
                burrow_map[coord] = node
        return burrow_map


class AmphipodOrganiser:
    def __init__(self, burrow_start_input, unfolded=False):
        burrow_start = burrow_start_input.splitlines()
        if unfolded:
            burrow_start = (
                burrow_start[:3]
                + """\
  #D#C#B#A#
  #D#B#A#C#""".splitlines()
                + burrow_start[3:]
            )
        self.amphipod_gen = amphipod_generator_factory()
        burrow_amphipod_space_gen = burrow_amphipod_space_generator_factory()

        amphipods = self._find_amphipods(burrow_start)
        amphipod_rows = len(amphipods) // AMPHIPODS_PER_ROW

        self.burrow_map = BurrowMapGenerator(burrow_amphipod_space_gen).create(
            amphipod_rows
        )

        amphipods_state = self._determine_amphipod_state(amphipods)
        self.start_state = AmphipodConfiguration(0, amphipods, amphipods_state)

        self._total_energy = None
        self._cache = None

    @classmethod
    def read_file(cls, unfolded):
        with open("input.txt") as f:
            return cls(f.read().strip(), unfolded)

    def _find_amphipods(self, burrow_start):
        amphipods: dict[Coords, Amphipod] = {}
        for y, row in enumerate(burrow_start):
            for x, raw_space in enumerate(row):
                try:
                    space = AmphipodType(raw_space)
                except ValueError:
                    pass
                else:
                    amphipods[Coords(x, y)] = self.amphipod_gen(space)
        return amphipods

    def _determine_amphipod_state(self, amphipods: dict[Coords, Amphipod]):
        amphipods_state = {
            amphipod: BurrowAmphipodState.ORIGINAL for amphipod in amphipods.values()
        }

        settled_neighbours = set()

        for coord, amphipod in amphipods.items():
            room = self.burrow_map.map[coord]
            if (
                room.this.id == self.burrow_map.amphipod_rows - 1
            ):  # we need to check bottom row first - rows are ordered 0 to n-1 , where n-1 is the end
                room_amphipod_type = room.this.type
                if room_amphipod_type == amphipod.type:
                    amphipods_state[amphipod] = BurrowAmphipodState.SETTLED
                    settled_neighbours.add(
                        (room.neighbours[0].coords, coord)
                    )  # assume end only has one neighbour

        while True:
            new_settled_neighbours = set()
            for coord, prev_coord in settled_neighbours:
                amphipod = amphipods[coord]
                room = self.burrow_map.map[coord]
                room_amphipod_type = room.this.type
                if room_amphipod_type == amphipod.type:
                    amphipods_state[amphipod] = BurrowAmphipodState.SETTLED
                    next_neighbour = [
                        neighbour.coords
                        for neighbour in room.neighbours
                        if neighbour.coords != prev_coord
                    ][0]
                    if next_neighbour not in amphipods:
                        # we only care about checking amphipods - this must be a hallway space so stop
                        continue
                    new_settled_neighbours.add((next_neighbour, coord))
            if not new_settled_neighbours:
                break
            else:
                settled_neighbours = new_settled_neighbours

        return amphipods_state

    def _win_condition(self, state):
        if all(
            amphipod_state == BurrowAmphipodState.SETTLED
            for amphipod_state in state.amphipods_state.values()
        ):
            return True
        return False

    def _free_room(self, amphipods: dict[Coords, Amphipod], amphipod: Amphipod):
        amphipod_room_coords = self.burrow_map.get_amphipod_coords(amphipod.type)

        maybe_free_room = None
        for room_coord in reversed(amphipod_room_coords.values()):
            if room_coord in amphipods:
                if maybe_free_room is not None:
                    raise Exception("occupied room discovered in front of free room")
                if amphipods[room_coord].type != amphipod.type:
                    # room is blocked with another amphipod
                    return None
            else:
                if maybe_free_room is None:
                    maybe_free_room = room_coord

        return maybe_free_room

    def _is_free_path(self, state, intrapath_coords):
        amphipods = state.amphipods
        free_path = not any(
            intrapath_coord in amphipods for intrapath_coord in intrapath_coords
        )
        return free_path

    def _intrapath_coords(self, amphipod_coord, dest_coord):
        intrapath_coords = self.burrow_map.path_coords(
            amphipod_coord, dest_coord, exclude_start=True
        )
        return intrapath_coords

    def _path_details(self, state, amphipod_coord: Coords, dest_coord: Coords):
        intrapath_coords = self._intrapath_coords(amphipod_coord, dest_coord)
        free_path = self._is_free_path(state, intrapath_coords)
        distance = len(intrapath_coords)
        return free_path, distance

    def _create_next_state(
        self, state, old_coord, new_coord, distance, amphipod_state: BurrowAmphipodState
    ):
        next_amphipods = state.amphipods.copy()
        amphipod = next_amphipods.pop(old_coord)
        next_amphipods[new_coord] = amphipod

        next_history = frozenset.union(*[state.history, ((amphipod, new_coord),)])

        next_amphipods_state = state.amphipods_state.copy()
        next_amphipods_state[amphipod] = amphipod_state

        energy = AMPHIPOD_ENERGY[amphipod.type] * distance

        next_state = AmphipodConfiguration(
            energy=state.energy + energy,
            amphipods=next_amphipods,
            amphipods_state=next_amphipods_state,
            history=next_history,
        )
        return next_state

    def _move_amphipod(
        self, state, amphipod_coord, next_coord, distance, next_amphipod_state
    ):
        next_state = self._create_next_state(
            state,
            amphipod_coord,
            next_coord,
            distance,
            amphipod_state=next_amphipod_state,
        )
        if (next_history := next_state.history) in self._cache:
            return False
        self._cache.add(next_history)
        self._dfs(next_state)
        return True

    def _dfs(self, state):
        if self._total_energy is not None and state.energy >= self._total_energy:
            return
        if self._win_condition(state):
            if self._total_energy is None or state.energy < self._total_energy:
                self._total_energy = state.energy
            return
        for amphipod_coord, amphipod in state.amphipods.items():
            if (amphipod_state := state.amphipods_state[amphipod]) in (
                BurrowAmphipodState.HALLWAY,
                BurrowAmphipodState.ORIGINAL,
            ):
                if free_room_coord := self._free_room(state.amphipods, amphipod):
                    free_path, distance = self._path_details(
                        state, amphipod_coord, free_room_coord
                    )
                if free_room_coord and free_path:
                    # amphipod can move straight into settled room
                    is_new_state = self._move_amphipod(
                        state=state,
                        amphipod_coord=amphipod_coord,
                        next_coord=free_room_coord,
                        distance=distance,
                        next_amphipod_state=BurrowAmphipodState.SETTLED,
                    )
                    if not is_new_state:
                        continue

                elif amphipod_state == BurrowAmphipodState.ORIGINAL:
                    # amphipod must move into hallway
                    hallway_coords = self.burrow_map.get_hallway_coords()
                    for hallway_coord in hallway_coords:
                        free_path, distance = self._path_details(
                            state, amphipod_coord, hallway_coord
                        )
                        if not free_path:
                            # spaces from amphipod to hallway room is occupied
                            continue

                        is_new_state = self._move_amphipod(
                            state=state,
                            amphipod_coord=amphipod_coord,
                            next_coord=hallway_coord,
                            distance=distance,
                            next_amphipod_state=BurrowAmphipodState.HALLWAY,
                        )
                        if not is_new_state:
                            continue

    def organise(self):
        self._cache = set()
        self._dfs(self.start_state)
        return self._total_energy


def main():
    ao = AmphipodOrganiser.read_file(unfolded=False)
    total_energy = ao.organise()
    print(f"{total_energy=}")

    ao = AmphipodOrganiser.read_file(unfolded=True)
    total_energy = ao.organise()
    print(f"{total_energy=}")


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
