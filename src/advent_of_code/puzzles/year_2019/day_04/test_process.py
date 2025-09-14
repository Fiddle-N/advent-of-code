from advent_of_code.puzzles.year_2019.day_04 import process


def test_example_1():
    assert process.meets_criteria_1(111111)


def test_example_2():
    assert not process.meets_criteria_1(223450)


def test_example_3():
    assert not process.meets_criteria_1(123789)


def test_example_4():
    assert process.meets_criteria_2(112233)


def test_example_5():
    assert not process.meets_criteria_2(123444)


def test_example_6():
    assert process.meets_criteria_2(111122)
