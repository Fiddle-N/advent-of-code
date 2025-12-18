from itertools import combinations
from math import prod
from operator import itemgetter
from typing import Self, cast

from advent_of_code.common import (
    Coords,
    read_file,
    timed_run,
)


def resolve_distances(
    coords: set[Coords],
) -> list[tuple[tuple[Coords, Coords], float]]:
    distances: list[tuple[tuple[Coords, Coords], float]] = []
    for a, b in combinations(coords, 2):
        distances.append(((a, b), a.distance(b)))
    return distances


class CircuitConnector:
    def __init__(self, points: set[Coords]):
        self.points = points
        self._id = 0

    @classmethod
    def from_input(cls, raw_input: str) -> Self:
        coords = set()
        for raw_coord in raw_input.splitlines():
            x, y, z = raw_coord.split(",")
            coords.add(Coords(int(x), int(y), int(z)))
        return cls(coords)

    def resolve(self, connection_no: int) -> tuple[int, int]:
        distance_pairs = resolve_distances(self.points)
        distance_pairs = sorted(distance_pairs, key=itemgetter(1))

        circuits: dict[int, set[Coords]] = {}
        for n, ((a, b), distance) in enumerate(distance_pairs):
            # part 1 check
            if n == connection_no:
                circuit_lengths = [len(circuit) for circuit in circuits.values()]
                most_common = sorted(circuit_lengths, reverse=True)[:3]
                part_1_result = prod(most_common)

            # resolve circuit pair
            circuit_id_a: int | None = None
            circuit_id_b: int | None = None
            for circuit_id, circuit in circuits.items():
                if a in circuit:
                    circuit_id_a = circuit_id
                if b in circuit:
                    circuit_id_b = circuit_id
            if circuit_id_a is None and circuit_id_b is None:
                next_circuit = {a, b}
                circuits[self._id] = next_circuit
                self._id += 1
            elif circuit_id_a is None:
                circuit_id_b = cast(
                    int, circuit_id_b
                )  # type checker not yet able to deduce this from previous if clause
                circuits[circuit_id_b].add(a)
            elif circuit_id_b is None:
                circuits[circuit_id_a].add(b)
            elif circuit_id_a != circuit_id_b:
                next_circuit = circuits[circuit_id_a] | circuits[circuit_id_b]

                del circuits[circuit_id_a]
                del circuits[circuit_id_b]

                circuits[self._id] = next_circuit
                self._id += 1
            else:
                assert circuit_id_a == circuit_id_b

            # part 2 check
            if len(circuits) == 1 and list(circuits.values())[0] == self.points:
                part_2_result = a.x * b.x
                break

        return (part_1_result, part_2_result)


def run():
    cc = CircuitConnector.from_input(read_file())
    print(cc.resolve(1000))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
