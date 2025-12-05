from advent_of_code import common


def test_merge_intervals_equal() -> None:
    input_ = [(2, 6), (1, 3), (8, 10), (10, 12), (10, 13)]
    assert common.merge_intervals(input_) == [(1, 6), (8, 13)]
