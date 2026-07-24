from enum import Enum

import more_itertools

from advent_of_code.common import read_file, timed_run

N_ROWS_P1 = 40
N_ROWS_P2 = 400000


class Tile(Enum):
    SAFE = "."
    TRAP = "^"


TRAPS = {
    (Tile.TRAP, Tile.TRAP, Tile.SAFE),
    (Tile.SAFE, Tile.TRAP, Tile.TRAP),
    (Tile.TRAP, Tile.SAFE, Tile.SAFE),
    (Tile.SAFE, Tile.SAFE, Tile.TRAP),
}


def parse_row(raw_row: str) -> list[Tile]:
    return [Tile(raw_tile) for raw_tile in raw_row]


def simulate(row: list[Tile], n_rows: int) -> int:
    n = 0
    safe_tiles = 0
    while True:
        safe_tiles += sum(tile == tile.SAFE for tile in row)
        n += 1
        if n == n_rows:
            return safe_tiles

        # add safe tiles on either end
        # to simulate safe wall tiles
        extended_row = [Tile.SAFE]
        extended_row.extend(row)
        extended_row.append(Tile.SAFE)

        row = [
            (Tile.TRAP if window in TRAPS else Tile.SAFE)
            for window in more_itertools.windowed(extended_row, 3)
        ]


def run():
    raw_row = read_file()
    row = parse_row(raw_row)
    print(simulate(row, N_ROWS_P1))
    print(simulate(row, N_ROWS_P2))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
