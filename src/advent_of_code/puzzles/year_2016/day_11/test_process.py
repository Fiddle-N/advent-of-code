from advent_of_code.puzzles.year_2016.day_11 import process


def test_a():
    comps = process.parse_components("""\
The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant.""")
    assert process.simulate(comps) == 11
