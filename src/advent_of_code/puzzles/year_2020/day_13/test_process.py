import math

from advent_of_code.puzzles.year_2020.day_13 import process


def test_earliest_bus():
    bus_input = """\
939
7,13,x,x,59,x,31,19"""
    shuttle_search = process.ShuttleSearch(bus_input)
    bus = shuttle_search.earliest_bus()
    assert bus == (59, 5)
    assert math.prod(bus) == 295


def test_chinese_remainder():
    bus_input = """\
939
7,13,x,x,59,x,31,19"""
    shuttle_search = process.ShuttleSearch(bus_input)
    assert shuttle_search.chinese_remainder() == 1068781


def test_chinese_remainder_2():
    bus_input = """\
0
17,x,13,19"""
    shuttle_search = process.ShuttleSearch(bus_input)
    assert shuttle_search.chinese_remainder() == 3417


def test_chinese_remainder_3():
    bus_input = """\
0
67,7,59,61"""
    shuttle_search = process.ShuttleSearch(bus_input)
    assert shuttle_search.chinese_remainder() == 754018


def test_chinese_remainder_4():
    bus_input = """\
0
67,x,7,59,61"""
    shuttle_search = process.ShuttleSearch(bus_input)
    assert shuttle_search.chinese_remainder() == 779210


def test_chinese_remainder_5():
    bus_input = """\
0
67,7,x,59,61"""
    shuttle_search = process.ShuttleSearch(bus_input)
    assert shuttle_search.chinese_remainder() == 1261476


def test_chinese_remainder_6():
    bus_input = """\
0
1789,37,47,1889"""
    shuttle_search = process.ShuttleSearch(bus_input)
    assert shuttle_search.chinese_remainder() == 1202161486
