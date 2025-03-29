from advent_of_code.year_2023.day_11 import process


def test_universe_original_expansion():
    universe_input = """\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""
    universe = process.Universe(universe_input)
    assert universe.galaxies == {
        1: process.Coords(3, 0),
        2: process.Coords(7, 1),
        3: process.Coords(0, 2),
        4: process.Coords(6, 4),
        5: process.Coords(1, 5),
        6: process.Coords(9, 6),
        7: process.Coords(7, 8),
        8: process.Coords(0, 9),
        9: process.Coords(4, 9),
    }
    galaxy_paths = universe.galaxy_paths()
    assert galaxy_paths == {
        frozenset({1, 2}): 6,
        frozenset({1, 3}): 6,
        frozenset({1, 4}): 9,
        frozenset({1, 5}): 9,
        frozenset({1, 6}): 15,
        frozenset({1, 7}): 15,
        frozenset({1, 8}): 15,
        frozenset({1, 9}): 12,
        frozenset({2, 3}): 10,
        frozenset({2, 4}): 5,
        frozenset({2, 5}): 13,
        frozenset({2, 6}): 9,
        frozenset({2, 7}): 9,
        frozenset({2, 8}): 19,
        frozenset({2, 9}): 14,
        frozenset({3, 4}): 11,
        frozenset({3, 5}): 5,
        frozenset({3, 6}): 17,
        frozenset({3, 7}): 17,
        frozenset({3, 8}): 9,
        frozenset({3, 9}): 14,
        frozenset({4, 5}): 8,
        frozenset({4, 6}): 6,
        frozenset({4, 7}): 6,
        frozenset({4, 8}): 14,
        frozenset({4, 9}): 9,
        frozenset({5, 6}): 12,
        frozenset({5, 7}): 12,
        frozenset({5, 8}): 6,
        frozenset({5, 9}): 9,
        frozenset({6, 7}): 6,
        frozenset({6, 8}): 16,
        frozenset({6, 9}): 11,
        frozenset({7, 8}): 10,
        frozenset({7, 9}): 5,
        frozenset({8, 9}): 5,
    }
    assert sum(galaxy_paths.values()) == 374


def test_universe_expansion_factor_10():
    universe_input = """\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""
    universe = process.Universe(universe_input)
    galaxy_paths = universe.galaxy_paths(expansion_factor=10)
    assert sum(galaxy_paths.values()) == 1030


def test_universe_expansion_factor_100():
    universe_input = """\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#....."""
    universe = process.Universe(universe_input)
    galaxy_paths = universe.galaxy_paths(expansion_factor=100)
    assert sum(galaxy_paths.values()) == 8410
