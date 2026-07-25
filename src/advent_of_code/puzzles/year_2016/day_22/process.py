"""
2016 Day 22

https://adventofcode.com/2016/day/22

Only works for inputs with the following assumptions:
1. There is only one free node available.
2. Once data goes from node to node, this does not free up a node to allow data
for more than one node to flow to it.
3. The largest chunk of used data (ignoring the very large, very full 49x TB nodes)
can be moved to the smallest empty node.
4. The very large, very full nodes do not live on x = 0 or x = 1.

As a result, the solution can be simplified to:
1. Work out the shortest path to get the empty node to one left of the goal node.
   This needs to be done computationally as we need to move around the very large,
   very full nodes, however:
  1. It is only necessary to ever consider a single empty node and its neighbours.
  2. Any neighbour can be moved to any node (other than the very large, very full nodes).
  3. It is not necessary to copy the filesystem for every state.
2. Once done, the steps to move the goal node along the y-axis can be calculated using a
   closed form solution shown in the example; where it takes one step to move the goal
   and four steps to move the empty node back left of the goal node.
"""

import re
from collections import deque
from dataclasses import dataclass
from itertools import permutations
from typing import Self

from advent_of_code.common import (
    Coords,
    read_file,
    timed_run,
    FOUR_POINT_DIRECTION_COORDS,
)

DIRECT_ACCESS_NODE = Coords(0, 0)
TARGET_DATA_Y = 0
VERY_LARGE_NODE_MIN_USED = 490
FREE_NODE_RESET_CYCLE = 4

NODE_PATTERN = (
    r"/dev/grid/node-x(?P<x>\d+)-y(?P<y>\d+)"
    r"\s+(?P<size>\d+)T"
    r"\s+(?P<used>\d+)T"
    r"\s+(?P<avail>\d+)T"
    r"\s+(?P<use_perc>\d+)%"
)


@dataclass(frozen=True)
class Node:
    used: int
    size: int

    @property
    def avail(self: Self) -> int:
        return self.size - self.used


@dataclass
class FSState:
    steps: int
    free_node: Coords


def parse_filesystem(raw_filesystem: str) -> dict[Coords, Node]:
    fs = {}
    for line in raw_filesystem.splitlines()[2:]:
        match_ = re.fullmatch(NODE_PATTERN, line)
        assert match_
        fs[Coords(int(match_["x"]), int(match_["y"]))] = Node(
            int(match_["used"]), int(match_["size"])
        )
    return fs


def viable_node_pairs(fs: dict[Coords, Node]) -> set[tuple[Coords, Coords]]:
    viable = set()
    for (coords_0, node_0), (coords_1, node_1) in permutations(fs.items(), 2):
        if node_0.used == 0:
            continue
        if node_0.used <= node_1.avail:
            viable.add((coords_0, coords_1))
    return viable


def shortest_path(fs: dict[Coords, Node], start: Coords, target: Coords) -> int:
    # bfs
    q = deque([FSState(steps=0, free_node=start)])
    seen = {start}
    while True:
        state = q.pop()
        next_steps = state.steps + 1
        for offset in FOUR_POINT_DIRECTION_COORDS:
            next_location = state.free_node + offset

            if next_location == target:
                return next_steps

            if next_location not in fs:
                continue

            next_node = fs[next_location]
            if next_node.used >= VERY_LARGE_NODE_MIN_USED:
                # immovable very large node
                continue

            if next_location in seen:
                continue

            seen.add(next_location)

            q.appendleft(FSState(steps=next_steps, free_node=next_location))


def simulate(fs: dict[Coords, Node]):
    viable_pairs = viable_node_pairs(fs)
    available_free = {target for source, target in viable_pairs}
    assert len(available_free) == 1
    free_node = next(iter(available_free))

    possible_target_nodes = [coords for coords in fs if coords.y == TARGET_DATA_Y]
    target_node = max(possible_target_nodes, key=lambda coords: coords.x)
    target_node_adj = Coords(target_node.x - 1, target_node.y)

    fewest_steps = shortest_path(fs, start=free_node, target=target_node_adj) + (
        (target_node.x) + (FREE_NODE_RESET_CYCLE * (target_node.x - 1))
    )

    return (len(viable_pairs), fewest_steps)


def run():
    raw_fs = read_file()
    fs = parse_filesystem(raw_fs)
    print(simulate(fs))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
