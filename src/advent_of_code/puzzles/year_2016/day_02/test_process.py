from advent_of_code.puzzles.year_2016.day_02 import process


def test_calculate_code_imaginary_keypad():
    instrs = process.parse_instrs("""\
ULL
RRDDD
LURDL
UUUUD""")
    assert process.calculate_code(instrs, keypad_type="imaginary") == "1985"


def test_calculate_code_real_keypad():
    instrs = process.parse_instrs("""\
ULL
RRDDD
LURDL
UUUUD""")
    assert process.calculate_code(instrs, keypad_type="real") == "5DB3"
