from advent_of_code.puzzles.year_2015.day_18 import process


def test_light_animation():
    grid_text = """\
.#.#.#
...##.
#....#
..#...
#.#..#
####.."""
    cgl = process.ConwaysGameOfLife.parse_grid(grid_text)
    animation_simulator = cgl.simulate_animation()
    for _ in range(4):
        next_lights = next(animation_simulator)
    on_lights = process.calculate_on_lights(next_lights)
    assert on_lights == 4


def test_light_animation_stuck_corners():
    grid_text = """\
.#.#.#
...##.
#....#
..#...
#.#..#
####.."""
    cgl = process.ConwaysGameOfLife.parse_grid(grid_text)
    animation_simulator = cgl.simulate_animation(stuck_corners=True)
    for _ in range(5):
        next_lights = next(animation_simulator)
    on_lights = process.calculate_on_lights(next_lights)
    assert on_lights == 17
