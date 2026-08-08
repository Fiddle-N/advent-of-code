from advent_of_code.puzzles.year_2017.day_15 import process


def test_judge_part_1() -> None:
    assert process.judge_part_1(a_start=65, b_start=8921) == 588


def test_judge_part_2() -> None:
    assert process.judge_part_2(a_start=65, b_start=8921) == 309
