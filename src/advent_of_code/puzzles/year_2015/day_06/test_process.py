import pytest

from advent_of_code.puzzles.year_2015.day_06 import process


@pytest.mark.parametrize(
    "step_input, output",
    [
        ("turn on 0,0 through 999,999", 1_000_000),
        ("toggle 0,0 through 999,0", 1_000),
        ("turn on 0,0 through 999,999\nturn off 499,499 through 500,500", 999_996),
    ],
)
def test_fixed_brightness(step_input, output) -> None:
    steps = process.parse_steps(step_input)
    assert (
        process.execute_brightness_steps(steps, process.execute_fixed_brightness)
        == output
    )


@pytest.mark.parametrize(
    "step_input, output",
    [
        ("turn on 0,0 through 0,0", 1),
        ("toggle 0,0 through 999,999", 2_000_000),
    ],
)
def test_variable_brightness(step_input, output) -> None:
    steps = process.parse_steps(step_input)
    assert (
        process.execute_brightness_steps(steps, process.execute_variable_brightness)
        == output
    )
