from advent_of_code.puzzles.year_2016.day_01 import process


def test_run_instrs_to_end_1():
    instrs = process.parse_instrs("R2, L3")
    assert process.run_instrs(instrs, dest="end") == 5


def test_run_instrs_to_end_2():
    instrs = process.parse_instrs("R2, R2, R2")
    assert process.run_instrs(instrs, dest="end") == 2


def test_run_instrs_to_end_3():
    instrs = process.parse_instrs("R5, L5, R5, R3")
    assert process.run_instrs(instrs, dest="end") == 12


def test_run_instrs_to_ebhq():
    instrs = process.parse_instrs("R8, R4, R4, R8")
    assert process.run_instrs(instrs, dest="ebhq") == 4
