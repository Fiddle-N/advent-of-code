from advent_of_code.puzzles.year_2015.day_16 import process


def test_calculate_best_score() -> None:
    sues = [
        {"cats": 7, "samoyeds": 2},
        {"cats": 8, "samoyeds": 2},
        {"pomeranians": 2, "cats": 7},
    ]
    assert (
        process.find_sue(
            sues, mfcsam_result=process.generate_mfcsam_comp_fns(mode="part_2")
        )
        == 2
    )
