import math

from year_2023.day_06 import process


def test_winning_ranges_of_races():
    race_input = """\
Time:      7  15   30
Distance:  9  40  200"""

    race = process.Races(race_input)
    winning_ranges = race.winning_ranges()
    assert winning_ranges == [
        process.WinningRange(2, 5),
        process.WinningRange(4, 11),
        process.WinningRange(11, 19),
    ]
    num_of_winning_distances = process.num_of_winning_distances(race)
    assert num_of_winning_distances == [4, 8, 9]
    assert math.prod(num_of_winning_distances) == 288


def test_distances_of_long_race():
    race_input = """\
Time:      7  15   30
Distance:  9  40  200"""

    race = process.Races(race_input, long_race=True)
    assert math.prod(process.num_of_winning_distances(race)) == 71503
