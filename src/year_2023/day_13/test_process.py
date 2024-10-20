from year_2023.day_13 import process


def test_finding_lines_of_symmetry() -> None:
    grids_input = """\
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
#....#..#"""
    grids = process.parse(grids_input)
    orig_sym_lines, new_sym_lines = process.find_sym_lines(grids)
    assert orig_sym_lines == [
        process.SymmetryLine(process.Direction.VERTICAL, 5),
        process.SymmetryLine(process.Direction.HORIZONTAL, 4),
    ]
    assert process.score(orig_sym_lines) == 405
    assert new_sym_lines == [
        process.SymmetryLine(process.Direction.HORIZONTAL, 3),
        process.SymmetryLine(process.Direction.HORIZONTAL, 1),
    ]
    assert process.score(new_sym_lines) == 400
