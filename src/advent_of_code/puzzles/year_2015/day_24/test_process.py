from advent_of_code.puzzles.year_2015.day_24 import process


def test_group_packages_3_groups():
    presents = [1, 2, 3, 4, 5, 7, 8, 9, 10, 11]
    optimal_group = process.group_packages(presents, no_of_groups=3)
    assert sorted(optimal_group.presents) == [9, 11]
    assert optimal_group.qe == 99


def test_group_packages_4_groups():
    presents = [1, 2, 3, 4, 5, 7, 8, 9, 10, 11]
    optimal_group = process.group_packages(presents, no_of_groups=4)
    assert sorted(optimal_group.presents) == [4, 11]
    assert optimal_group.qe == 44
