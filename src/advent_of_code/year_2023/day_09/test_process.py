import pytest

from advent_of_code.year_2023.day_09 import process


def test_history_1():
    history_input = "0 3 6 9 12 15"
    history = process.history_from_str(history_input)
    full_history = process.get_full_history(history)
    assert full_history == [[0, 3, 6, 9, 12, 15], [3, 3, 3, 3, 3], [0, 0, 0, 0]]
    next_history = process.extrapolate_full_history(full_history)
    assert next_history == [
        [-3, 0, 3, 6, 9, 12, 15, 18],
        [3, 3, 3, 3, 3, 3, 3],
        [0, 0, 0, 0, 0, 0],
    ]
    assert process.next_extrapolated_val(next_history) == 18
    assert process.prev_extrapolated_val(next_history) == -3


def test_history_2():
    history_input = "1 3 6 10 15 21"
    history = process.history_from_str(history_input)
    full_history = process.get_full_history(history)
    assert full_history == [
        [1, 3, 6, 10, 15, 21],
        [2, 3, 4, 5, 6],
        [1, 1, 1, 1],
        [0, 0, 0],
    ]
    next_history = process.extrapolate_full_history(full_history)
    assert next_history == [
        [0, 1, 3, 6, 10, 15, 21, 28],
        [1, 2, 3, 4, 5, 6, 7],
        [1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0],
    ]
    assert process.next_extrapolated_val(next_history) == 28
    assert process.prev_extrapolated_val(next_history) == 0


def test_history_3():
    history_input = "10 13 16 21 30 45"
    history = process.history_from_str(history_input)
    full_history = process.get_full_history(history)
    assert full_history == [
        [10, 13, 16, 21, 30, 45],
        [3, 3, 5, 9, 15],
        [0, 2, 4, 6],
        [2, 2, 2],
        [0, 0],
    ]
    next_history = process.extrapolate_full_history(full_history)
    assert next_history == [
        [5, 10, 13, 16, 21, 30, 45, 68],
        [5, 3, 3, 5, 9, 15, 23],
        [-2, 0, 2, 4, 6, 8],
        [2, 2, 2, 2, 2],
        [0, 0, 0, 0],
    ]
    assert process.next_extrapolated_val(next_history) == 68
    assert process.prev_extrapolated_val(next_history) == 5


def test_sum_extrapolate_report():
    report_input = """\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""
    extrapolated_report = process.get_extrapolated_report(report_input)

    sum_next_extrapolation = process.sum_next_extrapolated_vals(extrapolated_report)
    assert sum_next_extrapolation == 114

    sum_prev_extrapolation = process.sum_prev_extrapolated_vals(extrapolated_report)
    assert sum_prev_extrapolation == 2


def test_cannot_predict_history_for_irregular_history():
    history = [0, 2, 3674]
    with pytest.raises(
        ValueError,
        match="Could not predict history - sequence does not reduce to regular sum",
    ):
        process.get_full_history(history)
