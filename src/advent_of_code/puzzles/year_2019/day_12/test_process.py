from advent_of_code.puzzles.year_2019.day_12 import process


def test_example_1_problem_1():
    text = """\
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>"""
    moon_coords = process.process_text(text)
    moons = process.Moons(moon_coords)
    moons.simulate(10)
    assert moons.total_energy == 179


def test_example_2_problem_1():
    text = """\
<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>"""
    moon_coords = process.process_text(text)
    moons = process.Moons(moon_coords)
    moons.simulate(100)
    assert moons.total_energy == 1940


def test_example_1_problem_2():
    text = """\
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>"""
    moon_coords = process.process_text(text)
    moons = process.Moons(moon_coords)
    first_repeat = moons.first_repeat()
    assert first_repeat == 2772


def test_example_2_problem_2():
    text = """\
<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>"""
    moon_coords = process.process_text(text)
    moons = process.Moons(moon_coords)
    first_repeat = moons.first_repeat()
    assert first_repeat == 4686774924
