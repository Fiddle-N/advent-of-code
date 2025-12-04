from advent_of_code.common import (
    Coords,
    EIGHT_POINT_DIRECTION_COORDS,
    read_file,
    timed_run,
)

PAPER = "@"
SURROUNDING_LIMIT = 4


def parse(raw_input: str) -> set[Coords]:
    return {
        Coords(x, y)
        for y, row in enumerate(raw_input.splitlines())
        for x, space in enumerate(row)
        if space == PAPER
    }


def remove_paper(paper_coords: set[Coords]) -> tuple[int, int]:
    orig_paper_coords = paper_coords
    paper_coords = paper_coords.copy()
    first_round = True
    while True:
        remaining_paper_coords = set()
        for paper in paper_coords:
            surrounding = 0
            for dir_ in EIGHT_POINT_DIRECTION_COORDS:
                neighbour = paper + dir_
                if neighbour in paper_coords:
                    surrounding += 1
            if surrounding >= SURROUNDING_LIMIT:
                remaining_paper_coords.add(paper)
        if first_round:
            first_removed = len(paper_coords) - len(remaining_paper_coords)
        first_round = False
        if len(paper_coords) == len(remaining_paper_coords):
            total_removed = len(orig_paper_coords) - len(remaining_paper_coords)
            return (first_removed, total_removed)
        paper_coords = remaining_paper_coords


def run():
    paper_coords = parse(read_file())
    print(remove_paper(paper_coords))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
