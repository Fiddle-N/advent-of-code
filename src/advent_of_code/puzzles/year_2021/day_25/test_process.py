from advent_of_code.puzzles.year_2021.day_25 import process


def test_process():
    grid = """\
v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>"""
    map_ = process.Map.from_text(grid)
    assert process.simulate_movement(map_) == 58
