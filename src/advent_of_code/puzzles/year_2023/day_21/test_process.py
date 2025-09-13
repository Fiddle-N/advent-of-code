import itertools

from advent_of_code.puzzles.year_2023.day_21 import process


def test_garden_example_with_one_garden_using_iteration():
    garden_input = """\
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""
    garden = process.Garden(garden_input)
    elf_step_calculator = process.ElfStepCalculator(garden)
    elf_step_iter = iter(elf_step_calculator)

    result = next(elf_step_iter)
    assert result.plots_reached == 2

    result = next(elf_step_iter)
    assert result.plots_reached == 4

    result = next(elf_step_iter)
    assert result.plots_reached == 6

    for _ in range(3):
        result = next(elf_step_iter)
    assert result.plots_reached == 16


def test_garden_example_with_infinite_gardens_using_iteration():
    garden_input = """\
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""
    garden = process.Garden(garden_input)

    step_results = {
        6: 16,
        10: 50,
        50: 1594,
        100: 6536,
        500: 167004,
    }
    max_steps = 500

    elf_step_calculator = process.ElfStepCalculator(garden, is_infinite=True)
    elf_step_iter = iter(elf_step_calculator)

    for step_no in itertools.count(start=1):
        result = next(elf_step_iter)
        if step_no in step_results:
            assert result.plots_reached == step_results[step_no]
        if step_no == max_steps:
            break
