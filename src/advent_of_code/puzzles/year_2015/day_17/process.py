"""
2015 Day 17

Part 1
Fill 150 litres of eggnog in a given number of containers and find the number of arrangements.

Part 2
Find the number of arrangements for the lowest number of containers needed.
"""

from collections import Counter
from advent_of_code.common import read_file, timed_run


EGGNOG_VOL = 150


class EggnogResolver:
    def __init__(self):
        self._containers = []
        self._arrangements = Counter()

    def resolve(self, containers: list[int], target: int) -> tuple[int, int]:
        self._containers = sorted(containers)
        self._arrangements = Counter()
        for pos, _ in enumerate(self._containers):
            self._resolve(pos=pos, container_no=1, target=target)

        lowest_count = self._arrangements[sorted(self._arrangements)[0]]
        return self._arrangements.total(), lowest_count

    def _resolve(self, pos: int, container_no: int, target: int) -> None:
        if pos >= len(self._containers):
            # exhausted all containers - dead path
            return None
        container = self._containers[pos]
        if container == target:
            # completely fills container and no liquid left
            self._arrangements[container_no] += 1
        elif container < target:
            # completely fills container and some liquid spare
            liquid_left = target - container
            for next_pos in range(pos + 1, len(self._containers)):
                self._resolve(
                    pos=next_pos, container_no=container_no + 1, target=liquid_left
                )
        return None


def parse_containers(container_text: str) -> list[int]:
    return [int(container) for container in container_text.splitlines()]


def run():
    container_text = read_file()
    containers = parse_containers(container_text)
    for result in EggnogResolver().resolve(containers, target=EGGNOG_VOL):
        print(result)


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
