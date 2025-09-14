import pytest

from advent_of_code.puzzles.year_2020.day_15 import process


def test_example_0_3_6_with_stop_val_2020():
    assert process.memory_game("0,3,6", stop_val=2020) == 436


@pytest.mark.skip("Far too slow")
def test_example_0_3_6_with_stop_val_30_mil():
    assert process.memory_game("0,3,6", stop_val=30_000_000) == 175594


def test_example_1_3_2_with_stop_val_2020():
    assert process.memory_game("1,3,2", stop_val=2020) == 1


def test_example_2_1_3_with_stop_val_2020():
    assert process.memory_game("2,1,3", stop_val=2020) == 10


def test_example_1_2_3_with_stop_val_2020():
    assert process.memory_game("1,2,3", stop_val=2020) == 27


def test_example_2_3_1_with_stop_val_2020():
    assert process.memory_game("2,3,1", stop_val=2020) == 78


def test_example_3_2_1_with_stop_val_2020():
    assert process.memory_game("3,2,1", stop_val=2020) == 438


def test_example_3_1_2_with_stop_val_2020():
    assert process.memory_game("3,1,2", stop_val=2020) == 1836
