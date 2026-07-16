import re
from dataclasses import dataclass
from typing import Literal, cast
from collections import deque

from advent_of_code.common import read_file, timed_run, Coords, Grid

RECT_PATTERN = r"rect (?P<cols>\d+)x(?P<rows>\d+)"
ROTATE_PATTERN = (
    r"rotate (row|column) (?P<axis>[xy])=(?P<axis_pos>\d+) by (?P<rotate_val>\d+)"
)


@dataclass(frozen=True)
class Rect:
    rows: int
    cols: int


@dataclass(frozen=True)
class Rotate:
    axis: Literal["x", "y"]
    axis_pos: int
    rotate_val: int


type Instrs = Rect | Rotate


def parse_instrs(raw_instrs: str) -> list[Instrs]:
    instrs = []
    for raw_instr in raw_instrs.splitlines():
        if raw_instr.startswith("rect"):
            match_ = re.fullmatch(RECT_PATTERN, raw_instr)
            assert match_
            instrs.append(Rect(rows=int(match_["rows"]), cols=int(match_["cols"])))
        else:
            match_ = re.fullmatch(ROTATE_PATTERN, raw_instr)
            assert match_
            instrs.append(
                Rotate(
                    axis=cast(Literal["x", "y"], match_["axis"]),
                    axis_pos=int(match_["axis_pos"]),
                    rotate_val=int(match_["rotate_val"]),
                )
            )
    return instrs


def draw_rect(grid: Grid, rows: int, cols: int) -> None:
    for y in range(rows):
        for x in range(cols):
            grid[Coords(x, y)] = True


def rotate(grid: Grid, axis: Literal["x", "y"], axis_pos: int, rotate_val: int) -> None:
    coords = (
        [Coords(axis_pos, y) for y in range(grid.rows)]
        if axis == "x"
        else [Coords(x, axis_pos) for x in range(grid.cols)]
    )
    vals = deque([grid[coord] for coord in coords])
    vals.rotate(rotate_val)
    for coord, val in zip(coords, vals):
        grid[coord] = val


def run_instrs(grid: Grid, instrs: list[Instrs]) -> None:
    for instr in instrs:
        match instr:
            case Rect():
                draw_rect(grid, rows=instr.rows, cols=instr.cols)
            case Rotate():
                rotate(
                    grid,
                    axis=instr.axis,
                    axis_pos=instr.axis_pos,
                    rotate_val=instr.rotate_val,
                )


def sum_lit_pixels(grid) -> int:
    return sum(grid.values())


def run() -> None:
    grid = Grid(rows=6, cols=50)
    raw_instrs = read_file()
    instrs = parse_instrs(raw_instrs)
    run_instrs(grid, instrs)
    print(sum_lit_pixels(grid))
    print(grid.render())


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
