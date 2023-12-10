from year_2023.day_10 import process


def test_loop():
    field_input = """\
-L|F7
7S-7|
L|7||
-L-J|
L|-JF"""
    field = process.Field(field_input)
    exp_loop = [
        process.Coords(1, 1),
        process.Coords(1, 2),
        process.Coords(1, 3),
        process.Coords(2, 3),
        process.Coords(3, 3),
        process.Coords(3, 2),
        process.Coords(3, 1),
        process.Coords(2, 1),
    ]
    exp_reverse_loop = exp_loop[:1] + list(reversed(exp_loop[1:]))
    exp_loops = (exp_loop, exp_reverse_loop)
    assert field.loop in exp_loops
    assert process.furthest_steps_from_start(field.loop) == 4


def test_loop_2():
    field_input = """\
..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""
    field = process.Field(field_input)
    exp_loop = [
        process.Coords(0, 2),
        process.Coords(1, 2),
        process.Coords(1, 1),
        process.Coords(2, 1),
        process.Coords(2, 0),
        process.Coords(3, 0),
        process.Coords(3, 1),
        process.Coords(3, 2),
        process.Coords(4, 2),
        process.Coords(4, 3),
        process.Coords(3, 3),
        process.Coords(2, 3),
        process.Coords(1, 3),
        process.Coords(1, 4),
        process.Coords(0, 4),
        process.Coords(0, 3),
    ]
    exp_reverse_loop = exp_loop[:1] + list(reversed(exp_loop[1:]))
    exp_loops = (exp_loop, exp_reverse_loop)
    assert field.loop in exp_loops
    assert process.furthest_steps_from_start(field.loop) == 8


def test_enclosed_area():
    field_input = """\
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
..........."""
    field = process.Field(field_input)
    enclosed_area = process.area_enclosed_within_the_loop(field)
    assert enclosed_area == {
        process.Coords(2, 6),
        process.Coords(3, 6),
        process.Coords(7, 6),
        process.Coords(8, 6)
    }
    assert len(enclosed_area) == 4


def test_enclosed_area_2():
    field_input = """\
..........
.S------7.
.|F----7|.
.||....||.
.||....||.
.|L-7F-J|.
.|..||..|.
.L--JL--J.
.........."""
    field = process.Field(field_input)
    enclosed_area = process.area_enclosed_within_the_loop(field)
    assert enclosed_area == {
        process.Coords(2, 6),
        process.Coords(3, 6),
        process.Coords(6, 6),
        process.Coords(7, 6),
    }
    assert len(enclosed_area) == 4


def test_enclosed_area_3():
    field_input = """\
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ..."""
    field = process.Field(field_input)
    enclosed_area = process.area_enclosed_within_the_loop(field)
    assert enclosed_area == {
        process.Coords(14, 3),
        process.Coords(7, 4),
        process.Coords(8, 4),
        process.Coords(9, 4),
        process.Coords(7, 5),
        process.Coords(8, 5),
        process.Coords(6, 6),
        process.Coords(14, 6),
    }
    assert len(enclosed_area) == 8


def test_enclosed_area_4():
    field_input = """\
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L"""
    field = process.Field(field_input)
    enclosed_area = process.area_enclosed_within_the_loop(field)
    assert enclosed_area == {
        process.Coords(14, 3),
        process.Coords(10, 4),
        process.Coords(11, 4),
        process.Coords(12, 4),
        process.Coords(13, 4),
        process.Coords(11, 5),
        process.Coords(12, 5),
        process.Coords(13, 5),
        process.Coords(13, 6),
        process.Coords(14, 6),
    }
    assert len(enclosed_area) == 10
