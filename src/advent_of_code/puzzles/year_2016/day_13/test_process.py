from advent_of_code.common import Coords
from advent_of_code.puzzles.year_2016.day_13 import process


def test_building_simulator():
    bn = process.BuildingNavigator(10)
    assert bn.simulate(
        start=process.START, target=Coords(7, 4), reachable_from_steps=0
    ) == (11, 1)
