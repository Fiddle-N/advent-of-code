from advent_of_code.puzzles.year_2025.day_04 import process


def test_remove_paper():
    paper_grid = process.parse("""\
..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.""")
    assert process.remove_paper(paper_grid) == (13, 43)
