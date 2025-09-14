from advent_of_code.puzzles.year_2020.day_12 import process


def test_with_theoretical_actions():
    instructions_input = """\
F10
N3
F7
R90
F11"""
    ship = process.Ship(instructions_input)
    exp_pos = process.Coords(17, -8)
    assert process.process_with_theoretical_actions(ship) == exp_pos
    assert exp_pos.manhattan_dist() == 25


def test_with_actual_actions():
    instructions_input = """\
F10
N3
F7
R90
F11"""
    ship = process.Ship(instructions_input)
    exp_pos = process.Coords(214, -72)
    assert process.process_with_actual_actions(ship) == exp_pos
    assert exp_pos.manhattan_dist() == 286
