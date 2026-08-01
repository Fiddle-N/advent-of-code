from advent_of_code.puzzles.year_2017.day_05 import process


def test_run_part_1() -> None:
    instrs = [0, 3, 0, 1, -3]
    final_instrs, steps = process.execute_instrs(instrs, mode="part_1")
    assert final_instrs == [2, 5, 0, 1, -2]
    assert steps == 5


def test_run_part_2() -> None:
    instrs = [0, 3, 0, 1, -3]
    final_instrs, steps = process.execute_instrs(instrs, mode="part_2")
    assert final_instrs == [2, 3, 2, 3, -1]
    assert steps == 10
