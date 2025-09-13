import pytest

from advent_of_code.puzzles.year_2023.day_08 import process


def test_navigation_no_cycle():
    nav_input = """\
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""
    nav = process.Navigation(nav_input)

    nav_iter = process.navigate(nav)
    assert next(nav_iter) == "CCC"
    assert next(nav_iter) == "ZZZ"

    try:
        next(nav_iter)
    except StopIteration as exc:
        steps = exc.value
    else:
        pytest.fail()

    assert steps == 2


def test_navigation_cycle():
    nav_input = """\
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""
    nav = process.Navigation(nav_input)

    nav_iter = process.navigate(nav)
    exp_elements = ["BBB", "AAA", "BBB", "AAA", "BBB", "ZZZ"]
    for ele in exp_elements:
        assert next(nav_iter) == ele

    try:
        next(nav_iter)
    except StopIteration as exc:
        steps = exc.value
    else:
        pytest.fail()

    assert steps == 6


def test_navigate_simultaneously():
    nav_input = """\
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""
    nav = process.Navigation(nav_input)

    assert process.navigate_simultaneously(nav) == 6


def test_navigate_simultaneously_fails_if_more_than_one_end_element_visited():
    nav_input = """\
LR

11A = (11B, 11B)
11B = (XXX, 11Z)
11Z = (22B, XXX)
22B = (XXX, 22Z)
22Z = (11A, 11A)
XXX = (XXX, XXX)"""
    nav = process.Navigation(nav_input)

    with pytest.raises(ValueError, match="More than one end element visited"):
        process.navigate_simultaneously(nav)


def test_navigate_simultaneously_fails_if_path_to_one_end_element_does_not_follow_loop_with_no_offset():
    nav_input = """\
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11C, XXX)
11C = (XXX, 11D)
11D = (11E, XXX)
11E = (XXX, 11A)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""
    nav = process.Navigation(nav_input)

    with pytest.raises(
        ValueError, match="Path to end element does not follow a loop with zero offset"
    ):
        process.navigate_simultaneously(nav)
