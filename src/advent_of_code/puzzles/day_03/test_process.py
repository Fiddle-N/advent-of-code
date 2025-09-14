from advent_of_code.puzzles.day_03 import process


def test_toboggan_slopes():
    input_str = """\
..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#
"""
    toboggan_trajectory = process.TobogganTrajectory(input_str)
    assert toboggan_trajectory.calculate_trees_encountered(1, 1) == 2
    assert toboggan_trajectory.calculate_trees_encountered(3, 1) == 7
    assert toboggan_trajectory.calculate_trees_encountered(5, 1) == 3
    assert toboggan_trajectory.calculate_trees_encountered(7, 1) == 4
    assert toboggan_trajectory.calculate_trees_encountered(1, 2) == 2
