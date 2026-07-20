from advent_of_code.puzzles.year_2016.day_15 import process


def test_calculate_button_press():
    discs = process.parse_discs("""\
Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1.""")
    assert process.calculate_button_press(discs) == 5
