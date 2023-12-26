from year_2023.day_10 import process


def test_simple_loop_length():
    field_input = """\
-L|F7
7S-7|
L|7||
-L-J|
L|-JF"""
    field = process.Field(field_input)
    exp_forward_loop_verts = [
        process.Coords(1, 1),
        process.Coords(1, 3),
        process.Coords(3, 3),
        process.Coords(3, 1),
    ]
    exp_reverse_loop_verts = exp_forward_loop_verts[:1] + list(reversed(exp_forward_loop_verts[1:]))
    exp_loops_verts = (exp_forward_loop_verts, exp_reverse_loop_verts)
    assert field.loop_verts in exp_loops_verts
    assert field.loop_length == 8
    assert field.loop_length // 2 == 4


def test_slightly_complex_loop_length():
    field_input = """\
..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""
    field = process.Field(field_input)
    exp_forward_loop_verts = [
        process.Coords(0, 2),
        process.Coords(1, 2),
        process.Coords(1, 1),
        process.Coords(2, 1),
        process.Coords(2, 0),
        process.Coords(3, 0),
        process.Coords(3, 2),
        process.Coords(4, 2),
        process.Coords(4, 3),
        process.Coords(1, 3),
        process.Coords(1, 4),
        process.Coords(0, 4),
    ]
    exp_reverse_loop_verts = exp_forward_loop_verts[:1] + list(reversed(exp_forward_loop_verts[1:]))
    exp_loops_verts = (exp_forward_loop_verts, exp_reverse_loop_verts)
    assert field.loop_verts in exp_loops_verts
    assert field.loop_length == 16
    assert field.loop_length // 2 == 8


def test_simple_loop_enclosed_num_of_tiles():
    field_input = """\
-L|F7
7S-7|
L|7||
-L-J|
L|-JF"""
    field = process.Field(field_input)
    assert process.enclosed_num_of_tiles(field) == 1


def test_slightly_complex_loop_enclosed_num_of_tiles():
    field_input = """\
..F7.
.FJ|.
SJ.L7
|F--J
LJ..."""
    field = process.Field(field_input)
    assert process.enclosed_num_of_tiles(field) == 1


def test_medium_length_loop_enclosed_tiles():
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
    assert process.enclosed_num_of_tiles(field) == 4


def test_medium_length_loop_with_no_full_tile_path_to_outside_for_all_outside_tiles_enclosed_num_of_tiles():
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
    assert process.enclosed_num_of_tiles(field) == 4


def test_large_loop_enclosed_tiles():
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
    assert process.enclosed_num_of_tiles(field) == 8


def test_large_loop_2_with_surrounding_junk_pipe_enclosed_tiles():
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
    assert process.enclosed_num_of_tiles(field) == 10
