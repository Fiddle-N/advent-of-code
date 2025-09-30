"""
2015 Day 9

Part 1
Calculate the shortest path between a number of locations where you need to start at one location and end at another,
visiting every location exactly once.

Part 2
Part 1 but calculate the longest path.

Solution
Part 1 is the Travelling Salesman Problem but if we model the problem as a state space, where the states are
(set(locations_visited, current_locations)) then we can run Dijkstra's algorithm on the state space, ending when we get
to all locations visited. As is in regular Dijkstra's algorithm, we need to use a heap queue, but we don't need a
visited set to ensure we don't visit the same state multiple times, as we store the locations_visited on the state
itself.

Part 2 is similar to Dijkstra, but we need to consider states in topological order (we can substitute the heap
queue for a regular queue for this, as the state's locations visited is always monotonically increasing), we need to
process all states, and we need to discard states where we have a longer distance for that state already saved, as
opposed to a shorter distance in classic Dijkstra.
"""

import dataclasses
import heapq
from typing import Self

from advent_of_code.common import read_file, timed_run


@dataclasses.dataclass(frozen=True, order=True)
class State:
    distance: int
    visited: frozenset[str] = dataclasses.field(compare=False)
    location: str = dataclasses.field(compare=False)


class DistanceResolver:
    def __init__(self, locations: frozenset[str], distances: dict[frozenset[str], int]):
        self.locations = locations
        self.distances = distances

    @classmethod
    def from_distances(cls, distance_text) -> Self:
        locations = set()
        distances = {}
        for distance_pair in distance_text.splitlines():
            raw_locations, distance = distance_pair.split(" = ")
            location_0, location_1 = raw_locations.split(" to ")
            locations.add(location_0)
            locations.add(location_1)
            distances[frozenset([location_0, location_1])] = int(distance)
        return cls(frozenset(locations), distances)

    def shortest_path_length(self) -> int:
        costs: dict[tuple[frozenset[str], str], int] = {}
        q: list[State] = []

        for location in self.locations:
            visited = frozenset([location])
            costs[(visited, location)] = 0
            heapq.heappush(q, State(0, visited, location))

        while q:
            state = heapq.heappop(q)
            if state.visited == self.locations:
                return state.distance
            remaining = self.locations - state.visited
            for location in remaining:
                visited = state.visited | frozenset([location])
                new_node = (visited, location)
                prev_distance = costs.get(new_node)
                new_distance = (
                    state.distance
                    + self.distances[frozenset([state.location, location])]
                )
                if prev_distance is None or new_distance < prev_distance:
                    heapq.heappush(q, State(new_distance, visited, location))
                    costs[(visited, location)] = new_distance

        raise Exception("unreachable")

    def longest_path_length(self) -> int:
        costs: dict[tuple[frozenset[str], str], int] = {}
        q: list[State] = []

        for location in self.locations:
            visited = frozenset([location])
            costs[(visited, location)] = 0
            q.insert(0, State(0, visited, location))

        while q:
            state = q.pop()
            remaining = self.locations - state.visited
            for location in remaining:
                visited = state.visited | frozenset([location])
                new_node = (visited, location)
                prev_distance = costs.get(new_node)
                new_distance = (
                    state.distance
                    + self.distances[frozenset([state.location, location])]
                )
                if prev_distance is None or new_distance > prev_distance:
                    q.insert(0, State(new_distance, visited, location))
                    costs[(visited, location)] = new_distance

        return max(
            [cost for state, cost in costs.items() if state[0] == self.locations]
        )


def run() -> None:
    distance_text = read_file()
    dr = DistanceResolver.from_distances(distance_text)
    print(dr.shortest_path_length())
    print(dr.longest_path_length())


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
