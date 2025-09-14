import dataclasses
import collections
import itertools
import pprint
import timeit
import typing
import string


from advent_of_code.common import Coords


def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


@dataclasses.dataclass
class Node:
    distance_from_start: int
    previous_node: Coords | None = None
    key: str | None = None
    door: str | None = None


@dataclasses.dataclass(frozen=True)
class Path:
    position: tuple | None = None
    distance_from_start: int | None = None
    keys: tuple | None = None
    key_letters: tuple | None = None
    key_set: set | None = None
    blocked_nodes: set | None = None

    def __repr__(self):
        return f"Path object: coords {self.position}; distance {self.distance_from_start}; retrieved keys {''.join(k for k, v in zip(self.key_letters, self.keys) if v)}"

    def __lt__(self, other):
        return (self.distance_from_start, sum(self.keys) * -1) < (
            other.distance_from_start,
            sum(other.keys) * -1,
        )


# class Path:
#
#     def __init__(self, position=None, distance_from_start=None, keys=None):
#         self.position = position
#         self.distance_from_start = distance_from_start
#         self.keys = keys
#
#     def __repr__(self):
#         return f"Path object: coords {self.position}; distance {self.distance_from_start}; retrieved keys {''.join(k for k, v in self.keys.items() if v)}"


@dataclasses.dataclass
class KeyPair:
    distance: int
    keys: typing.Sequence[str]
    doors: typing.Sequence[str]


class Maze:
    DIRECTION_COORDINATES = {
        "N": Coords(0, -1),
        "S": Coords(0, 1),
        "E": Coords(1, 0),
        "W": Coords(-1, 0),
    }

    DRY = "#"
    WET = "~"
    EMPTY_SPACE = "."
    START_SPACE = "@"
    WALL = "#"

    def __init__(self, maze=None, filename="input.txt"):
        self.maze = None
        self.filename = filename
        if maze is not None:
            self.preprocess_maze(maze)
        else:
            self.read_file()
        self.flooded_maze = None
        self.KEYS = ()
        self.DOORS = ()
        self.item_map = {}
        self.get_items()
        self.SPACES = (
            list(self.KEYS) + list(self.DOORS) + [self.EMPTY_SPACE] + [self.START_SPACE]
        )

    def read_file(self):
        with open(self.filename) as f:
            maze_str = f.read().rstrip()
        self.preprocess_maze(maze_str)

    def preprocess_maze(self, maze_str):
        maze = []
        for line in maze_str.split("\n"):
            maze.append(list(line.rstrip()))
        self.maze = maze

    def get_items(self):
        keys = []
        doors = []
        self.item_map[self.START_SPACE] = list()  # prep for multiple start spaces
        for col_idx, row in enumerate(self.maze):
            for row_idx, space in enumerate(row):
                if space in string.ascii_lowercase or space in string.ascii_uppercase:
                    self.item_map[space] = Coords(row_idx, col_idx)
                if space == self.START_SPACE:
                    self.item_map[space].append(Coords(row_idx, col_idx))
                if space in string.ascii_lowercase:
                    keys.append(space)
                if space in string.ascii_uppercase:
                    doors.append(space)
        self.KEYS = tuple(sorted(keys))
        self.DOORS = tuple(sorted(doors))

    def display(self, maze=None, blocked_nodes=None):
        blocked_nodes = set() if blocked_nodes is None else blocked_nodes
        if maze is None:
            maze = self.maze
        for col_idx, row in enumerate(maze):
            for row_idx, space in enumerate(row):
                position = Coords(row_idx, col_idx)
                space = self.WALL if position in blocked_nodes else space
                print(space, end="")
            print("\n", end="")

    @property
    def length(self):
        return len(self.maze)

    @property
    def width(self):
        return len(self.maze[0])

    def does_position_exist(self, coords):
        if (0 <= coords.x < self.width) and (0 <= coords.y < self.length):
            return True
        return False

    def is_perfect(self):
        self.flood_fill()
        for row in self.flooded_maze:
            if self.DRY in row:
                return False
        return True

    def flood_fill(self):
        self.flooded_maze = [row.copy() for row in self.maze]
        self._flood_fill(Coords(0, 0), self.DRY, self.WET)

    def _flood_fill(self, node, target_colour, replacement_colour):
        if not self.does_position_exist(node):
            return
        tile = self.flooded_maze[node.y][node.x]
        if target_colour == replacement_colour:
            pass
        elif tile != target_colour:
            pass
        else:
            self.flooded_maze[node.y][node.x] = replacement_colour
            for direction in self.DIRECTION_COORDINATES.values():
                new_node = node + direction
                self._flood_fill(new_node, target_colour, replacement_colour)

    def find_item(self, item):
        for col_idx, row in enumerate(self.maze):
            for row_idx, space in enumerate(row):
                if space == item:
                    return Coords(row_idx, col_idx)

    # def key_pair(self, start, end):
    #     start_coords = self.item_map[start]
    #     end_coords = self.item_map[end]
    #     open_list = []
    #     details = {}
    #     open_list.append(start_coords)
    #     details[start_coords] = Node(distance_from_start=0)
    #     while end_coords not in details:
    #         position = open_list.pop(0)
    #         position_details = details[position]
    #         for direction in self.DIRECTION_COORDINATES.values():
    #             next_position = position + direction
    #             next_distance = position_details.distance_from_start + 1
    #             if not self.does_position_exist(next_position):
    #                 continue
    #             next_space = self.maze[next_position.y][next_position.x]
    #             if next_space not in self.SPACES:
    #                 continue
    #             if (
    #                     next_position not in details
    #                     or next_distance < details[next_position].distance_from_start
    #             ):
    #                 details[next_position] = Node(
    #                     distance_from_start=next_distance,
    #                     previous_node=position,
    #                     key=next_space if next_space in self.KEYS else None,
    #                     door=next_space if next_space in self.DOORS else None,
    #                 )
    #                 open_list.append(next_position)
    #
    #     end_details = details[end_coords]
    #
    #     previous_coords = end_details.previous_node
    #     keys = []
    #     doors = []
    #     while previous_coords != start_coords:
    #         previous_details = details[previous_coords]
    #         if (key := previous_details.key) is not None:
    #             keys.append(key)
    #         if (door := previous_details.door) is not None:
    #             doors.append(door)
    #         previous_coords = previous_details.previous_node
    #
    #     return KeyPair(
    #         distance=end_details.distance_from_start,
    #         keys=tuple(reversed(keys)),
    #         doors=tuple(sorted(doors)),
    #     )
    #
    # def generate_all_key_pairs(self, remove_intermediate_keys_fast=False, remove_intermediate_keys_slow=False):
    #     positions = ['@'] + list(self.KEYS)
    #     naughty_list = []
    #
    #     key_pairs = {}
    #     while positions:
    #         start_position = positions.pop(0)
    #         for end_position in positions:
    #             if remove_intermediate_keys_fast:
    #                 if (start_position, end_position) in naughty_list:
    #                     continue
    #             key_pair_details = self.key_pair(start_position, end_position)
    #             if remove_intermediate_keys_fast:
    #                 keys = key_pair_details.keys
    #                 if len(keys) >= 2:
    #                     all_keys = [start_position] + list(keys) + [end_position]
    #                     perfect_keypairs = set(pairwise(all_keys))
    #                     all_keypairs = set(itertools.combinations(all_keys, 2))
    #                     blacklist_keypairs = all_keypairs - perfect_keypairs
    #                     for blacklist_keypair in blacklist_keypairs:
    #                         sorted_blacklist_keypair = tuple(sorted(blacklist_keypair))
    #                         naughty_list.append(sorted_blacklist_keypair)
    #                 if keys:
    #                     continue
    #             key_pairs[(start_position, end_position)] = key_pair_details
    #
    #     if remove_intermediate_keys_slow:
    #         key_pairs = {
    #             key_pair: key_pair_details
    #             for key_pair, key_pair_details in key_pairs.items()
    #             if not key_pair_details.keys
    #         }
    #     return key_pairs

    def _add_path_to_list(self, open_list, details, next_path):
        existing_paths = details[next_path.position]
        for existing_path in existing_paths:
            existing_keys = existing_path.key_set
            new_keys = next_path.key_set
            if (
                existing_path.distance_from_start
                <= next_path.distance_from_start  # i think this optimisation logic is correct but tricky to say for sure
                and new_keys <= existing_keys
            ):
                break
        else:
            open_list.append(next_path)
            details[next_path.position].append(next_path)

    @property
    def direction_combos(self):
        template = [Coords(0, 0)] * 4
        direction_combos = []
        for idx, _ in enumerate(template):
            meta_combo = []
            for direction_coord in self.DIRECTION_COORDINATES.values():
                base = template.copy()
                base[idx] = direction_coord
                meta_combo.append(base)
            direction_combos.append(meta_combo)
        return direction_combos

    def distance(self, start="@"):
        start_coords = self.item_map[start]
        open_list = []
        details = collections.defaultdict(list)
        blocked_nodes = self.dirt_fill()

        initial_path = Path(
            position=start_coords,
            distance_from_start=0,
            keys=tuple(False for letter in self.KEYS),
            key_letters=self.KEYS,
            key_set=set(),
            blocked_nodes=set(),
        )
        open_list.append(initial_path)
        details[tuple(start_coords)].append(initial_path)

        while True:
            dead_end = None
            current_position = open_list.pop(0)
            current_keys = current_position.keys
            dead_ends = current_position.blocked_nodes.copy()
            if all(current_keys):  # found all the keys
                break

            next_positions = []
            direction_combos = self.direction_combos

            for idx, meta_combo in enumerate(direction_combos):
                dead_end = None
                possible_next_positions = []
                for direction_combo in meta_combo:
                    next_position = tuple(
                        self_coords + other_coords
                        for self_coords, other_coords in zip(
                            current_position.position, direction_combo
                        )
                    )
                    if not all(
                        self.does_position_exist(position) for position in next_position
                    ):
                        continue
                    next_space = [
                        self.WALL
                        if (position in blocked_nodes or position in dead_ends)
                        else self.maze[position.y][position.x]
                        for position in next_position
                    ]
                    if any(space not in self.SPACES for space in next_space):
                        continue
                    possible_next_positions.append(next_position)
                if len(possible_next_positions) == 1:
                    dead_end = idx
                for position in possible_next_positions:
                    next_positions.append((position, dead_end))

            for next_position, dead_end in next_positions:  # too many comparisons
                current_keys = current_position.keys
                current_key_set = set(
                    k
                    for k, v in zip(current_position.key_letters, current_position.keys)
                    if v
                )
                next_distance = current_position.distance_from_start + 1

                next_space = [
                    self.maze[position.y][position.x] for position in next_position
                ]
                next_space_keys = [space for space in next_space if space in self.KEYS]
                if next_space_keys:
                    current_keys_list = list(current_position.keys)
                    for space in next_space_keys:
                        current_keys_list[self.KEYS.index(space)] = True
                    current_keys = tuple(current_keys_list)
                    current_key_set = set(
                        k for k, v in zip(self.KEYS, current_keys) if v
                    )
                if any(
                    space in self.DOORS
                    and not current_keys[self.KEYS.index(space.lower())]
                    for space in next_space
                ):
                    continue
                dead_ends_copy = dead_ends.copy()
                if dead_end is not None:
                    dead_ends_copy.add(current_position.position[dead_end])
                next_path = Path(
                    position=next_position,
                    distance_from_start=next_distance,
                    keys=current_keys,
                    key_letters=self.KEYS,
                    key_set=current_key_set,
                    blocked_nodes=dead_ends_copy,
                )
                self._add_path_to_list(open_list, details, next_path)
        return current_position.distance_from_start

    def dirt_fill(self, filled_nodes=None, initial_position="@"):
        filled_nodes = set() if filled_nodes is None else filled_nodes
        next_filled_nodes = filled_nodes.copy()
        while True:
            for col_idx, row in enumerate(self.maze):
                for row_idx, space in enumerate(row):
                    current_position = Coords(row_idx, col_idx)
                    current_space = (
                        self.WALL
                        if current_position in filled_nodes
                        else self.maze[current_position.y][current_position.x]
                    )
                    if current_space not in self.SPACES:
                        continue
                    if current_space in self.KEYS or current_space == initial_position:
                        continue
                    next_positions = []
                    for direction in self.DIRECTION_COORDINATES.values():
                        next_position = current_position + direction
                        if not self.does_position_exist(next_position):
                            continue
                        next_space = (
                            self.WALL
                            if next_position in filled_nodes
                            else self.maze[next_position.y][next_position.x]
                        )
                        if next_space not in self.SPACES:
                            continue
                        next_positions.append(next_position)
                    if len(next_positions) == 1:
                        next_filled_nodes.add(current_position)
            if next_filled_nodes == filled_nodes:
                return filled_nodes
            else:
                filled_nodes = next_filled_nodes.copy()

    def dirt_fill_top_down(self):
        pass


def get_key_pairs(maze):
    key_pairs = maze.generate_all_key_pairs()
    print("Number of key pairs", len(key_pairs))
    pprint.pprint(key_pairs)


def main():
    maze = Maze(filename="input2.txt")
    # blocked_nodes = maze.dirt_fill()
    # pprint.pprint(blocked_nodes)
    # maze.display(blocked_nodes=blocked_nodes)
    print(maze.distance())
    # maze.display()
    # print()
    # # maze.flood_fill()
    # # maze.display(maze.flooded_maze)
    # print('Is maze perfect?', maze.is_perfect())
    # print()
    # # assert maze.generate_all_key_pairs(remove_intermediate_keys_fast=True) == maze.generate_all_key_pairs(remove_intermediate_keys_slow=True)
    # frozen_get_key_pairs = functools.partial(get_key_pairs, maze)
    # print(timeit.timeit(frozen_get_key_pairs, number=1))
    # cProfile.run('maze=Maze();maze.distance()')


# def main2():
#     input_maze = """\
#     #################
#     #i.G..c...e..H.p#
#     ########.########
#     #j.A..b...f..D.o#
#     ########@########
#     #k.E..a...g..B.n#
#     ########.########
#     #l.F..d...h..C.m#
#     #################"""
#     maze_solver = Maze(input_maze)
#     pprint.pprint(maze_solver.generate_all_key_pairs())


def main2():
    maze = Maze(filename="input2.txt")
    blocked_nodes = maze.dirt_fill()
    pprint.pprint(blocked_nodes)
    maze.display(blocked_nodes=blocked_nodes)


if __name__ == "__main__":
    print("Time taken:", timeit.timeit(main, number=1))
    # main()
    # main()
