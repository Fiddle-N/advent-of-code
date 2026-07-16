from advent_of_code.puzzles.year_2016.day_08 import process


def test_run_instrs():
    instrs = process.parse_instrs("""\
rect 3x2
rotate column x=1 by 1
rotate row y=0 by 4
rotate column x=1 by 1""")
    grid = process.Grid(rows=3, cols=7)
    process.run_instrs(grid, instrs)
    assert (
        str(grid)
        == """\
.#..#.#
#.#....
.#....."""
    )
