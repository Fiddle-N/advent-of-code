import math

from year_2023.day_06 import process


def test_distances_of_races():
    race_input = """\
Time:      7  15   30
Distance:  9  40  200"""

    race = process.Races(race_input)
    distances = race.distances()
    assert distances == [
        [0, 6, 10, 12, 12, 10, 6, 0],
        [0, 14, 26, 36, 44, 50, 54, 56, 56, 54, 50, 44, 36, 26, 14, 0],
        [0, 29, 56, 81, 104, 125, 144, 161, 176, 189, 200, 209, 216, 221, 224, 225,
         224, 221, 216, 209, 200, 189, 176, 161, 144, 125, 104, 81, 56, 29, 0],
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
