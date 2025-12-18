import dataclasses
import collections
import functools
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
    position: Coords | None = None
    distance_from_start: int | None = None
    keys: tuple[bool, ...] = ()
    key_letters: tuple[str, ...] = ()
    key_set: set | None = None
    blocked_nodes: set | None = None
    seen_nodes: set | None = None
    key_path: list | None = None

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
#             key_pairs[frozenset([start_position, end_position])] = key_pair_details
#
#     if remove_intermediate_keys_slow:
#         key_pairs = {
#             key_pair: key_pair_details
#             for key_pair, key_pair_details in key_pairs.items()
#             if not key_pair_details.keys
#         }
#     return key_pairs


@dataclasses.dataclass
class KeyPair:
    distance: int
    keys: typing.Sequence[str] = ()
    doors: typing.Sequence[str] = ()


def cached(func):
    func.cache = {}

    @functools.wraps(func)
    def wrapper(*args):
        try:
            result = func.cache[args]
        except KeyError:
            func.cache[args] = result = func(*args)
            return result
        else:
            return result

    return wrapper


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

    DUMMY_NODE = "!"

    def __init__(self, maze=None, filename="input.txt"):
        self.maze: list[list[str]]
        self.filename = filename
        if maze is not None:
            self.preprocess_maze(maze)
        else:
            self.read_file()
        self.flooded_maze: list[list[str]]
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
        for col_idx, row in enumerate(self.maze):
            for row_idx, space in enumerate(row):
                if (
                    space in string.ascii_lowercase
                    or space in string.ascii_uppercase
                    or space == self.START_SPACE
                ):
                    self.item_map[space] = Coords(row_idx, col_idx)
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

    def key_pair(self, start, end):
        start_coords = self.item_map[start]
        end_coords = self.item_map[end]
        open_list = []
        details = {}
        open_list.append(start_coords)
        details[start_coords] = Node(distance_from_start=0)
        while end_coords not in details:
            position = open_list.pop(0)
            position_details = details[position]
            for direction in self.DIRECTION_COORDINATES.values():
                next_position = position + direction
                next_distance = position_details.distance_from_start + 1
                if not self.does_position_exist(next_position):
                    continue
                next_space = self.maze[next_position.y][next_position.x]
                if next_space not in self.SPACES:
                    continue
                if (
                    next_position not in details
                    or next_distance < details[next_position].distance_from_start
                ):
                    details[next_position] = Node(
                        distance_from_start=next_distance,
                        previous_node=position,
                        key=next_space if next_space in self.KEYS else None,
                        door=next_space if next_space in self.DOORS else None,
                    )
                    open_list.append(next_position)

        end_details = details[end_coords]

        previous_coords = end_details.previous_node
        keys = []
        doors = []
        while previous_coords != start_coords:
            previous_details = details[previous_coords]
            if (key := previous_details.key) is not None:
                keys.append(key)
            if (door := previous_details.door) is not None:
                doors.append(door)
            previous_coords = previous_details.previous_node

        return KeyPair(
            distance=end_details.distance_from_start,
            keys=tuple(reversed(keys)),
            doors=tuple(sorted(doors)),
        )

    def generate_all_key_pairs(self, add_dummy=False):
        positions = ["@"] + list(self.KEYS)
        initial_positions = positions.copy()
        key_pairs = {}
        while positions:
            start_position = positions.pop(0)
            for end_position in positions:
                key_pair_details = self.key_pair(start_position, end_position)
                key_pairs[frozenset([start_position, end_position])] = key_pair_details
        if add_dummy:
            for position in initial_positions:
                key_pairs[frozenset([self.DUMMY_NODE, position])] = KeyPair(0)
        return key_pairs

    def distance_2(self):
        self.key_pairs = self.generate_all_key_pairs()
        positions = self.KEYS
        distances = []
        for end_key in self.KEYS:
            _, distance = self._distance_2(frozenset(positions), end_key)
            if distance is None:
                continue
            distances.append(distance)
            # print('finished distance for @ to', end_key)
        # print(self._distance_2.cache_info())
        return min(distances)

    @functools.cache
    def _distance_2(self, positions, end_key):
        print(positions, end_key)
        if len(positions) == 1:
            assert positions == frozenset(end_key)
            key_pair_info = self.key_pairs[frozenset(list(positions) + ["@"])]
            if len(key_pair_info.doors) != 0:
                # there is a door between @ and the key
                return None, None
            if len(key_pair_info.keys) != 0:
                # there is a key between @ and the key
                return None, None
            return positions, key_pair_info.distance
        else:
            new_positions = frozenset(
                position for position in positions if position != end_key
            )
            distances = []
            for second_from_end_key in new_positions:
                retrieved_keys, distance_part_1 = self._distance_2(
                    new_positions, second_from_end_key
                )
                if distance_part_1 is None:
                    continue
                key_info = self.key_pairs[frozenset([second_from_end_key, end_key])]
                unlocked_doors = [key.upper() for key in retrieved_keys]
                if not set(key_info.doors).issubset(set(unlocked_doors)):
                    # all doors are not yet unlocked
                    continue
                if not set(key_info.keys).issubset(set(retrieved_keys)):
                    # there is still a key in between these keys
                    continue
                distance_part_2 = key_info.distance
                distance = distance_part_1 + distance_part_2
                new_retrieved_keys = list(retrieved_keys)
                new_retrieved_keys.append(end_key)
                distances.append((new_retrieved_keys, distance))
            if len(distances) == 0:
                return None, None
            return min(distances, key=lambda x: x[1])

    def distance_3(self):
        self.key_pairs = self.generate_all_key_pairs()
        distances = {}
        while True:
            distances = self._distance_3(distances)
            example_distance = list(distances.keys())[0]
            if len(example_distance) == (len(self.KEYS) + 1):
                break
        return distances[min(distances, key=lambda key_pair: distances[key_pair])]

    def _distance_3(self, old_distances):
        if not old_distances:
            distances = {}
            for key in self.KEYS:
                key_pair = ("@", key)
                key_pair_info = self.key_pairs[frozenset(key_pair)]
                if len(key_pair_info.doors) == 0 and len(key_pair_info.keys) == 0:
                    distances[key_pair] = key_pair_info.distance
        else:
            distances = {}
            for path, distance in old_distances.items():
                remaining_keys = set(self.KEYS) - set(path)
                last_key = path[-1]
                unlocked_doors = [key.upper() for key in path]
                for key in remaining_keys:
                    key_pair = (last_key, key)
                    key_pair_info = self.key_pairs[frozenset(key_pair)]
                    if not set(key_pair_info.doors).issubset(set(unlocked_doors)):
                        # all doors are not yet unlocked
                        continue
                    if not set(key_pair_info.keys).issubset(set(path)):
                        # there is still a key in between these keys
                        continue
                    new_path = tuple(list(path) + [key])
                    distances[new_path] = distance + key_pair_info.distance
        return distances

    def distance(self, start="@", mode="bfs", maxdistance=None):
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
            seen_nodes=set(),
            key_path=list(),
        )
        open_list.append(initial_path)
        details[start_coords].append(initial_path)

        while True:
            dead_end = False
            if mode == "bfs":
                current_position = open_list.pop(0)
            else:
                try:
                    current_position = open_list.pop()
                except IndexError:
                    return False
                if current_position.distance_from_start >= maxdistance:
                    continue

            current_keys = current_position.keys
            dead_ends = current_position.blocked_nodes.copy()
            # dead_ends = self.dirt_fill(start_position=current_position.position, doors_are_walls=True, found_keys=current_position.key_set)

            if all(current_keys):  # found all the keys
                break

            next_positions = []
            for direction in self.DIRECTION_COORDINATES.values():
                next_position = current_position.position + direction
                if not self.does_position_exist(next_position):
                    continue
                next_space = (
                    self.WALL
                    if (next_position in blocked_nodes or next_position in dead_ends)
                    else self.maze[next_position.y][next_position.x]
                )
                if next_space not in self.SPACES:
                    continue
                next_positions.append(next_position)
            if (
                len(next_positions) == 1
            ):  # we are in a dead end that we never want to return to
                dead_end = True

            for next_position in next_positions:
                current_key_path = current_position.key_path.copy()
                current_keys = current_position.keys
                current_key_set = set(
                    k
                    for k, v in zip(current_position.key_letters, current_position.keys)
                    if v
                )
                next_position = next_position
                next_distance = current_position.distance_from_start + 1
                next_space = self.maze[next_position.y][next_position.x]

                seen_nodes_copy = current_position.seen_nodes.copy()
                seen_nodes_copy.add(current_position.position)
                if next_position in seen_nodes_copy:
                    continue

                if next_space in self.KEYS:
                    current_key_path.append(next_space)
                    current_keys_list = list(current_position.keys)
                    current_keys_list[self.KEYS.index(next_space)] = True
                    current_keys = tuple(current_keys_list)
                    current_key_set = set(
                        k for k, v in zip(self.KEYS, current_keys) if v
                    )
                    seen_nodes_copy = (
                        set()
                    )  # if we get a key we can go over different nodes
                    seen_nodes_copy.add(next_position)

                    # dead_ends = self.dirt_fill(start_position=next_position, doors_are_walls=True, found_keys=current_key_set)
                dead_ends = current_position.blocked_nodes.copy()
                if dead_end:
                    dead_ends.add(current_position.position)

                if (
                    next_space in self.DOORS
                    and not current_keys[self.KEYS.index(next_space.lower())]
                ):
                    continue
                # if dead_end:
                #     dead_ends.add(current_position.position)
                next_path = Path(
                    position=next_position,
                    distance_from_start=next_distance,
                    keys=current_keys,
                    key_letters=self.KEYS,
                    key_set=current_key_set,
                    blocked_nodes=dead_ends,
                    seen_nodes=seen_nodes_copy,
                    key_path=current_key_path,
                )

                existing_paths = details[next_path.position]
                for existing_path in existing_paths:
                    existing_keys = existing_path.key_set
                    new_keys = next_path.key_set
                    if (
                        existing_path.distance_from_start
                        <= next_path.distance_from_start
                        and new_keys <= existing_keys
                    ):
                        break
                else:
                    open_list.append(next_path)
                    details[next_path.position].append(next_path)
                    self.times_passed += 1
        print(self.times_passed)
        return current_position.distance_from_start

    times_passed = 0

    def idfs(self):
        for x in range(1000):
            distance = self.distance(mode="dfs", maxdistance=x)
            if distance:
                return distance

    def dirt_fill(
        self,
        filled_nodes=None,
        start_position=None,
        doors_are_walls=False,
        found_keys=None,
    ):
        if found_keys is None:
            found_keys = set()
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
                    if (
                        doors_are_walls
                        and current_space in self.DOORS
                        and current_space.lower() not in found_keys
                    ):
                        current_space = self.WALL
                    if current_space not in self.SPACES:
                        continue
                    if current_space in self.KEYS and current_space not in found_keys:
                        continue
                    if current_position == start_position or (
                        start_position is None and current_space == "@"
                    ):
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
                        if (
                            doors_are_walls
                            and next_space in self.DOORS
                            and next_space.lower() not in found_keys
                        ):
                            next_space = self.WALL
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
    maze = Maze()
    # blocked_nodes = maze.dirt_fill()
    # pprint.pprint(blocked_nodes)
    # maze.display(blocked_nodes=blocked_nodes)
    # pprint.pprint(maze.generate_all_key_pairs())
    print(maze.distance())
    # print(maze.distance_2())

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


def main3():
    input_maze = """\
    #################
    #i.G..c...e..H.p#
    ########.########
    #j.A..b...f..D.o#
    ########@########
    #k.E..a...g..B.n#
    ########.########
    #l.F..d...h..C.m#
    #################"""
    maze_solver = Maze(input_maze)
    pprint.pprint(maze_solver.generate_all_key_pairs(add_dummy=True))


def main2():
    maze = Maze(filename="input2.txt")
    blocked_nodes = maze.dirt_fill()
    pprint.pprint(blocked_nodes)
    maze.display(blocked_nodes=blocked_nodes)


if __name__ == "__main__":
    print("Time taken:", timeit.timeit(main, number=1))
    # main()
