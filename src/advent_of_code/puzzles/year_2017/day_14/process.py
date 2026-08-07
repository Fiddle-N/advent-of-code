from advent_of_code.common import (
    read_file,
    timed_run,
    Coords,
    FOUR_POINT_DIRECTION_COORDS,
)
from advent_of_code.puzzles.year_2017 import knot_hash

GRID_SIZE = 128


def _count_used(key: str) -> set[Coords]:
    used = set()
    for y in range(GRID_SIZE):
        for x, char in enumerate(
            knot_hash.calculate_knot_hash(f"{key}-{y}").bindigest()
        ):
            if int(char):
                used.add(Coords(x, y))
    return used


class CountGroups:
    def __init__(self, used_squares: set[Coords]):
        self._used_squares = used_squares
        self._unseen_squares = used_squares.copy()

    def _count_group(self):
        used_square = self._unseen_squares.pop()
        group_squares = [used_square]
        while group_squares:
            square = group_squares.pop()
            for offset in FOUR_POINT_DIRECTION_COORDS:
                next_square = square + offset
                if not (
                    0 <= next_square.x < GRID_SIZE and 0 <= next_square.y < GRID_SIZE
                ):
                    # not a valid grid square
                    continue
                if next_square not in self._used_squares:
                    # not a used square
                    continue
                if next_square not in self._unseen_squares:
                    # used square seen before
                    continue
                group_squares.append(next_square)
                self._unseen_squares.remove(next_square)

    def count(self) -> int:
        groups = 0
        while self._unseen_squares:
            self._count_group()
            groups += 1
        return groups


def count_used_squares(key: str) -> tuple[int, int]:
    used_squares = _count_used(key)
    used_groups = CountGroups(used_squares).count()
    return len(used_squares), used_groups


def run():
    key = read_file()
    print(count_used_squares(key))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
