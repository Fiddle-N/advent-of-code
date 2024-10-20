from year_2023.day_14 import process


def test_tilt():
    platform_input = """\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""
    tilted_platform = process.tilt(platform_input)
    assert (
        tilted_platform
        == """\
OOOO.#.O..
OO..#....#
OO..O##..O
O..#.OO...
........#.
..#....#.#
..O..#.O.O
..O.......
#....###..
#....#...."""
    )
    assert process.calculate_load(tilted_platform) == 136


def test_cycle():
    platform_input = """\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#...."""
    cycle_iter = process.cycle(platform_input, total_cycles=1_000_000_000)
    assert (
        next(cycle_iter)
        == """\
.....#....
....#...O#
...OO##...
.OO#......
.....OOO#.
.O#...O#.#
....O#....
......OOOO
#...O###..
#..OO#...."""
    )
    assert (
        next(cycle_iter)
        == """\
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#..OO###..
#.OOO#...O"""
    )
    assert (
        next(cycle_iter)
        == """\
.....#....
....#...O#
.....##...
..O#......
.....OOO#.
.O#...O#.#
....O#...O
.......OOO
#...O###.O
#.OOO#...O"""
    )
    while True:
        try:
            next(cycle_iter)
        except StopIteration as exc:
            titled_platform_after_many_cycles = exc.value
            break
    assert process.calculate_load(titled_platform_after_many_cycles) == 64
