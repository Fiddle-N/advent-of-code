from advent_of_code.puzzles.year_2025.day_01 import process


def test_execute_instructions():
    rotations = process.parse("""\
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82""")
    assert process.execute_instructions(rotations, mode="original") == 3


def test_execute_instructions_click_mode():
    rotations = process.parse("""\
L68
L30
R48
L5
R60
L55
L1
L99
R14
L82""")
    assert process.execute_instructions(rotations, mode="click") == 6


def test_execute_instructions_click_mode_multiple_rotations():
    rotations = process.parse("""\
R1000""")
    assert process.execute_instructions(rotations, mode="click") == 10


def test_execute_instructions_click_mode_counting_backwards_exactly_zero_():
    rotations = process.parse("""\
L50
L100""")
    assert process.execute_instructions(rotations, mode="click") == 2


def test_execute_instructions_click_mode_counting_backwards_exactly_zero_without_double_counting():
    rotations = process.parse("""\
L50
L100
L1
L0""")
    assert process.execute_instructions(rotations, mode="click") == 2


def test_execute_instructions_click_mode_counting_forwards_exactly_zero():
    rotations = process.parse("""\
R50
R100""")
    assert process.execute_instructions(rotations, mode="click") == 2


def test_execute_instructions_click_mode_counting_forwards_exactly_zero_without_double_counting():
    rotations = process.parse("""\
R50
R100
R1
R0""")
    assert process.execute_instructions(rotations, mode="click") == 2


def test_execute_instructions_click_mode_counting_forwards_exactly_zero_then_counting_back():
    rotations = process.parse("""\
R50
L1""")
    assert process.execute_instructions(rotations, mode="click") == 1


def test_execute_instructions_click_mode_counting_backwards_exactly_zero_then_counting_forwards():
    rotations = process.parse("""\
L50
R1""")
    assert process.execute_instructions(rotations, mode="click") == 1
