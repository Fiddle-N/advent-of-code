from advent_of_code.puzzles.year_2017.day_17 import process


def test_spinlock() -> None:
    assert (
        process.spinlock(
            forward_steps=3,
            cycles=process.SPINLOCK_INSERTIONS_1,
            search_no=process.SPINLOCK_TARGET_1,
        )
        == 638
    )
