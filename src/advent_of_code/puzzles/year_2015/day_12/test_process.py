import pytest

from advent_of_code.puzzles.year_2015.day_12 import process


@pytest.mark.parametrize(
    "input_json, exp_sum",
    [
        ("[1,2,3]", 6),
        ('{"a":2,"b":4}', 6),
        ("[[[3]]]", 3),
        ('{"a":{"b":4},"c":-1}', 3),
        ('{"a":[-1,1]}', 0),
        ('[-1,{"a":1}]', 0),
        ("[]", 0),
        ("{}", 0),
    ],
)
def test_sum_json_numbers(input_json: str, exp_sum: int) -> None:
    jsn = process.JSONSumNumbers()
    assert jsn.sum_numbers(input_json) == exp_sum


@pytest.mark.parametrize(
    "input_json, exp_sum",
    [
        ("[1,2,3]", 6),
        ('[1,{"c":"red","b":2},3]', 4),
        ('{"d":"red","e":[1,2,3,4],"f":5}', 0),
        ('[1,"red",5]', 6),
    ],
)
def test_sum_json_numbers_ignore_red_in_objs(input_json: str, exp_sum: int) -> None:
    jsn = process.JSONSumNumbers()
    assert jsn.sum_numbers(input_json, ignore_red=True) == exp_sum
