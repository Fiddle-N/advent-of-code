"""
Given a file of 2D binary pixel grid like so (separated by double new lines),
e.g.

#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#

---

Part 1 - find the only line of symmetry (either horizontal or vertical) in the
grid. The line of symmetry needn't be perfectly in the middle of the grid, so
some rows/columns may not be reflected over.

The first grid in the example above has its vertical line of symmetry shown by
>< :

    ><
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.
    ><

The second grid in the example above has its horizontal line of symmetry shown
by v^ :

 #...##..#
 #....#..#
 ..##..###
v#####.##.v
^#####.##.^
 ..##..###
 #....#..#

Score each grid as follows:
* If a horizontal line of symmetry, calculate the number of columns left of the
line.
* If a vertical line of symmetry, calculate the number of rows above the line
and multiply by 100.

Sum up all grid scores to get the total grid score, which is the answer to
part 1.

---

Part 2 - repeat part 1 but find the line of symmetry where a single pixel change
in the grid (* to # or vice versa) causes a different line of symmetry to
emerge. Only one pixel change exists such that a new line of symmetry emerges.

The first grid in the example has a new horizontal line of reflection when the
very first pixel in the top left corner changes from # to . :

 ..##..##.
 ..#.##.#.
v##......#v
^##......#^
 ..#.##.#.
 ..##..##.
 #.#.##.#.

The second grid has a new horizontal line of reflection when row 2 column 5
changes from . to # :

v#...##..#v
^#...##..#^
 ..##..###
 #####.##.
 #####.##.
 ..##..###
 #....#..#

Score the grids in the same way as part 1 to get the result for part 2.
"""
import copy
import dataclasses
import enum
from collections.abc import Iterator

FILENAME = 'input.txt'

OFF = '.'
ON = '#'


OPPOSITE_PIXEL = {
    OFF: ON,
    ON: OFF,
}


class Direction(enum.Enum):
    HORIZONTAL = enum.auto()
    VERTICAL = enum.auto()


@dataclasses.dataclass(frozen=True)
class SymmetryLine:
    direction: Direction
    position: int


def read_file() -> str:
    with open(FILENAME) as f:
        return f.read().strip()


def parse(grid_input: str) -> list[list[list[str]]]:
    """
    Parse grid input into a list of 2D grids.
    """
    return [
        [list(line) for line in grid.splitlines()]
        for grid in grid_input.split('\n\n')
    ]


def find_sym_lines_across_axis(
        grid: list[list[str]],
        break_on_first_sym_line: bool
) -> list[int]:
    """
    Find the positions of a line of symmetry across one axis. The axis is
    implicitly decided in whether the grid list passed in represents a list
    of rows or a list of columns.
    """

    # Scan the grid from top to bottom, trying each possible sym line in turn.
    # The terms "upper" and "lower" are used, but if columns are passed in
    # rather than rows, this should be thought of as "left" and "right" in
    # respect to the original grid.

    sym_lines = []
    upper_lines = []
    lower_lines = grid.copy()
    while True:
        upper_lines.append(lower_lines.pop(0))  # grid size is small so popping from the beginning is fine
        if not lower_lines:
            # we've reached the very end of the grid - no sym lines were found
            break

        # this value discards the lines that won't overlap when folded,
        # since the sym line is not perfectly in the middle
        num_of_lines_to_check = min(len(upper_lines), len(lower_lines))

        # check the overlapping lines for reflection
        if upper_lines[-num_of_lines_to_check:] == list(reversed(lower_lines[:num_of_lines_to_check])):
            # sym line found
            sym_line_position = len(upper_lines)
            sym_lines.append(sym_line_position)
            if break_on_first_sym_line or len(sym_lines) == 2:
                # the max numbers of sym lines in a single grid can only be two
                break
    return sym_lines


def find_grid_sym_lines(grid: list[list[str]], break_on_first_sym_line: bool) -> list[SymmetryLine]:
    """
    Find the lines of symmetry in a single grid across both axes.

    For part 1, we are guaranteed only one symmetry line per grid, so if
    we find it, we can break immediately - set break_on_first_sym_line to
    True to stop searching.

    For part 2, we might search and initially find the same line we found
    in part 1, so we need to keep searching until we find a second one - set
    break_on_first_sym_line to False to keep searching.
    """
    sym_lines = []

    # find sym lines across rows
    rows = grid
    sym_line_positions = find_sym_lines_across_axis(rows, break_on_first_sym_line)
    for sym_line_pos in sym_line_positions:
        sym_lines.append(SymmetryLine(direction=Direction.HORIZONTAL, position=sym_line_pos))
        if break_on_first_sym_line:
            return sym_lines

    # find sym lines across columns
    cols = [list(col) for col in zip(*rows)]
    sym_line_positions = find_sym_lines_across_axis(cols, break_on_first_sym_line)
    for sym_line_pos in sym_line_positions:
        sym_lines.append(SymmetryLine(direction=Direction.VERTICAL, position=sym_line_pos))
        if break_on_first_sym_line:
            return sym_lines

    return sym_lines


def find_grid_permutations(grid: list[list[str]]) -> Iterator[list[list[str]]]:
    """
    Yield permutations of the grid where one pixel of the grid is changed at
    a time.
    """
    for y, row in enumerate(grid):
        for x, px in enumerate(row):
            new_grid = copy.deepcopy(grid)      # fine as grid sizes are small
            new_grid[y][x] = OPPOSITE_PIXEL[px]
            yield new_grid


def find_sym_lines(grids: list[list[list[str]]]) -> tuple[list[SymmetryLine], list[SymmetryLine]]:
    """
    Find the single line of symmetry in each original grid, as per part 1.
    Then find the new line of symmetry in each grid when exactly one pixel is
    changed, as per part 2.
    """

    # part 1
    orig_sym_lines = []
    for grid in grids:
        sym_lines = find_grid_sym_lines(grid, break_on_first_sym_line=True)
        sym_line, = sym_lines       # exactly one orig line of symmetry is present
        orig_sym_lines.append(sym_line)

    # part 2
    # We need to know the original line of symmetry for each grid in part 1
    # so that we can find the different line of symmetry when going through
    # each permutation of changed grids
    new_sym_lines = []
    for orig_sym_line, grid in zip(orig_sym_lines, grids):
        for grid_perm in find_grid_permutations(grid):
            sym_lines = find_grid_sym_lines(grid_perm, break_on_first_sym_line=False)
            if orig_sym_line in sym_lines:
                sym_lines.remove(orig_sym_line)
            if not sym_lines:
                continue

            # new sym line found
            sym_line, = sym_lines  # exactly one orig line of symmetry is present
            new_sym_lines.append(sym_line)
            break

    return orig_sym_lines, new_sym_lines


def score(sym_lines: list[SymmetryLine]) -> int:
    factor = {
        Direction.HORIZONTAL: 100,
        Direction.VERTICAL: 1,
    }
    return sum(
        factor[sym_line.direction] * sym_line.position
        for sym_line in sym_lines
    )


def main() -> None:
    grids_input = read_file()
    grids = parse(grids_input)
    orig_sym_lines, new_sym_lines = find_sym_lines(grids)
    print(
        "Part 1 - summed score for original line of symmetry in grids:",
        score(orig_sym_lines)
    )
    print(
        "Part 2 - summed score for new line of symmetry in grids where exactly one px has changed:",
        score(new_sym_lines)
    )


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
