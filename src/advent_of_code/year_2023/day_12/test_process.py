import pytest

from advent_of_code.year_2023.day_12 import process


@pytest.mark.parametrize(
    "condition_record, damaged_springs, arrangements",
    [
        ("#", (1,), 1),
        (".", (1,), 0),
        ("?", (1,), 1),
        ("#.", (1,), 1),
        (".#", (1,), 1),
        ("##", (1,), 0),
        ("..", (1,), 0),
    ],
)
def test_condition_simple_base_cases(condition_record, damaged_springs, arrangements):
    assert process.arrangements(condition_record, damaged_springs) == arrangements


def test_condition_records():
    field_input = """\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""
    field = process.Field(field_input)
    arrangements = field.arrangements()
    assert arrangements == [1, 4, 1, 1, 4, 10]
    assert sum(arrangements) == 21


def test_condition_records_unfolded():
    field_input = """\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""
    field = process.Field(field_input, unfolded=True)
    arrangements = field.arrangements()
    assert arrangements == [1, 16384, 1, 16, 2500, 506250]
    assert sum(arrangements) == 525152
