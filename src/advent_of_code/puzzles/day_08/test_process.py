from advent_of_code.puzzles.day_08 import process


def test():
    input_str = """\
nop +0
acc +1
jmp +4
acc +3
jmp -3
acc -99
acc +1
jmp -4
acc +6"""
    handheld_halting = process.HandheldHalting(input_str)
    assert handheld_halting.process() == 5
    assert handheld_halting.process_with_changes() == 8