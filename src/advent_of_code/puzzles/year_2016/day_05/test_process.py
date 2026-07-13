from advent_of_code.puzzles.year_2016.day_05 import process


def test_generate_pw_door_1():
    assert process.generate_pw_door_1(door_id="abc") == "18f47a30"


def test_generate_pw_door_2():
    assert process.generate_pw_door_2(door_id="abc") == "05ace8e3"
