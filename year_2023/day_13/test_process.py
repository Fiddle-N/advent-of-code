from year_2023.day_13 import process


def test_pattern_input():
    pattern_input = """\
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
    pattern = process.Patterns(pattern_input)
    clean_mirrors, dirty_mirrors = pattern.find_mirrors()
    assert clean_mirrors == [
        process.Mirror(process.Orientation.VERTICAL, 5),
        process.Mirror(process.Orientation.HORIZONTAL, 4),
    ]
    assert process.summarise(clean_mirrors) == 405
    assert dirty_mirrors == [
        process.Mirror(process.Orientation.HORIZONTAL, 3),
        process.Mirror(process.Orientation.HORIZONTAL, 1),
    ]
    assert process.summarise(dirty_mirrors) == 400


def test_pattern_input_with_dirty_mirror_after_clean_mirror():
    pattern_input = """\
....#..
###....
...#.##
###....
....##.
##.#.##
..##.##
###.#..
..#.###"""

    pattern = process.Patterns(pattern_input)
    clean_mirrors, dirty_mirrors = pattern.find_mirrors()
    assert clean_mirrors == [
        process.Mirror(process.Orientation.VERTICAL, 1),
    ]
    assert process.summarise(clean_mirrors) == 1
    assert dirty_mirrors == [
        process.Mirror(process.Orientation.VERTICAL, 6),
    ]
    assert process.summarise(dirty_mirrors) == 6
