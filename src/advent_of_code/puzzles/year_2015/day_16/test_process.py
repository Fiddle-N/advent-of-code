from advent_of_code.puzzles.year_2015.day_16 import process


def test_calculate_best_score() -> None:
    mfcsam_result = {
        "children": lambda val: val == 3,
        "cats": lambda val: val > 7,
        "samoyeds": lambda val: val == 2,
        "pomeranians": lambda val: val < 3,
    }
    sues = [
        {"cats": 7, "samoyeds": 2},
        {"cats": 8, "samoyeds": 2},
        {"pomeranians": 2, "cats": 7},
    ]
    assert process.find_sue(sues, mfcsam_result) == 2
