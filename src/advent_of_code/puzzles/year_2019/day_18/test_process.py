# all tests skipped far too slow

#
# def test_maze_is_perfect():
#     input_maze = """\
# ########################
# #f.D.E.e.C.b.A.@.a.B.c.#
# ######################.#
# #d.....................#
# ########################"""
#     maze_solver = process.Maze(input_maze)
#     assert maze_solver.is_perfect()
#
#
# def test_maze_is_not_perfect():
#     input_maze = """\
# ########################
# #f.D.E.e.C.b.A.@.a.B.c.#
# #.####################.#
# #d.....................#
# ########################"""
#     maze_solver = process.Maze(input_maze)
#     assert not maze_solver.is_perfect()
#
#
# def test_distance_between_e_and_f_is_6():
#     input_maze = """\
# ########################
# #f.D.E.e.C.b.A.@.a.B.c.#
# ######################.#
# #d.....................#
# ########################"""
#     maze_solver = process.Maze(input_maze)
#     assert maze_solver.key_pair('e', 'f').doors == ('D', 'E')
#
#
# def test_generate_all_key_pair_details():
#     input_maze = """\
# ########################
# #f.D.E.e.C.b.A.@.a.B.c.#
# ######################.#
# #d.....................#
# ########################"""
#     maze_solver = process.Maze(input_maze)
#     assert maze_solver.generate_all_key_pairs() == {
#         ('@', 'a'): process.KeyPair(distance=2, keys=(), doors=()),
#         ('@', 'b'): process.KeyPair(distance=4, keys=(), doors=('A',)),
#         ('@', 'c'): process.KeyPair(distance=6, keys=('a',), doors=('B',)),
#         ('@', 'd'): process.KeyPair(distance=30, keys=('a', 'c'), doors=('B',)),
#         ('@', 'e'): process.KeyPair(distance=8, keys=('b',), doors=('A', 'C')),
#         ('@', 'f'): process.KeyPair(distance=14, keys=('b', 'e'), doors=('A', 'C', 'D', 'E')),
#         ('a', 'b'): process.KeyPair(distance=6, keys=(), doors=('A',)),
#         ('a', 'c'): process.KeyPair(distance=4, keys=(), doors=('B',)),
#         ('a', 'd'): process.KeyPair(distance=28, keys=('c',), doors=('B',)),
#         ('a', 'e'): process.KeyPair(distance=10, keys=('b',), doors=('A', 'C')),
#         ('a', 'f'): process.KeyPair(distance=16, keys=('b', 'e'), doors=('A', 'C', 'D', 'E')),
#         ('b', 'c'): process.KeyPair(distance=10, keys=('a',), doors=('A', 'B')),
#         ('b', 'd'): process.KeyPair(distance=34, keys=('a', 'c'), doors=('A', 'B')),
#         ('b', 'e'): process.KeyPair(distance=4, keys=(), doors=('C',)),
#         ('b', 'f'): process.KeyPair(distance=10, keys=('e',), doors=('C', 'D', 'E')),
#         ('c', 'd'): process.KeyPair(distance=24, keys=(), doors=()),
#         ('c', 'e'): process.KeyPair(distance=14, keys=('a', 'b'), doors=('A', 'B', 'C')),
#         ('c', 'f'): process.KeyPair(distance=20, keys=('a', 'b', 'e'), doors=('A', 'B', 'C', 'D', 'E')),
#         ('d', 'e'): process.KeyPair(distance=38, keys=('c', 'a', 'b'), doors=('A', 'B', 'C')),
#         ('d', 'f'): process.KeyPair(distance=44, keys=('c', 'a', 'b', 'e'), doors=('A', 'B', 'C', 'D', 'E')),
#         ('e', 'f'): process.KeyPair(distance=6, keys=(), doors=('D', 'E')),
#     }
#
#
# def test_generate_all_key_pair_details_without_intermediate_keys():
#     input_maze = """\
# ########################
# #f.D.E.e.C.b.A.@.a.B.c.#
# ######################.#
# #d.....................#
# ########################"""
#     maze_solver = process.Maze(input_maze)
#     assert maze_solver.generate_all_key_pairs(remove_intermediate_keys_fast=True) == {
#         ('@', 'a'): process.KeyPair(distance=2, keys=(), doors=()),
#         ('@', 'b'): process.KeyPair(distance=4, keys=(), doors=('A',)),
#         ('a', 'b'): process.KeyPair(distance=6, keys=(), doors=('A',)),
#         ('a', 'c'): process.KeyPair(distance=4, keys=(), doors=('B',)),
#         ('b', 'e'): process.KeyPair(distance=4, keys=(), doors=('C',)),
#         ('c', 'd'): process.KeyPair(distance=24, keys=(), doors=()),
#         ('e', 'f'): process.KeyPair(distance=6, keys=(), doors=('D', 'E')),
#     }
#
#
# def test_distance_input_maze_1():
#     input_maze = """\
# ########################
# #f.D.E.e.C.b.A.@.a.B.c.#
# ######################.#
# #d.....................#
# ########################"""
#     maze_solver = process.Maze(input_maze)
#     assert maze_solver.distance() == 86
#
#     # @ to a (17, 1) = 2
#     # @ to b (11, 1) = 8
#     # @ to c (21, 1) = 18
#     # @ to d (1, 3) = 42
#     # @ to e (7, 1) = 80
#     # @ to f (1, 1) = 86
#
#
# def test_distance_input_maze_2():
#     input_maze = """\
# ########################
# #...............b.C.D.f#
# #.######################
# #.....@.a.B.c.d.A.e.F.g#
# ########################"""
#     maze_solver = process.Maze(input_maze)
#     assert maze_solver.distance() == 132
#
#
# def test_distance_input_maze_3():
#     input_maze = """\
# #################
# #i.G..c...e..H.p#
# ########.########
# #j.A..b...f..D.o#
# ########@########
# #k.E..a...g..B.n#
# ########.########
# #l.F..d...h..C.m#
# #################"""
#     maze_solver = process.Maze(input_maze)
#     assert maze_solver.distance() == 136
#
#
#
# def test_distance_input_maze_4():
#     input_maze = """\
# ########################
# #@..............ac.GI.b#
# ###d#e#f################
# ###A#B#C################
# ###g#h#i################
# ########################"""
#     maze_solver = process.Maze(input_maze)
#     assert maze_solver.distance() == 81
#
#
# ####
#
# def test_new_method_0():
#     input_maze = """\
# #########
# #....@.a#
# #########"""
#     maze_solver = process.Maze(input_maze)
#     assert maze_solver.distance_2() == 2
#
#
# def test_new_method_1():
#     input_maze = """\
# #########
# #b.A.@.a#
# #########"""
#     maze_solver = process.Maze(input_maze)
#     assert maze_solver.distance_2() == 8
#
#
# def test_new_method_2():
#     input_maze = """\
# ########################
# #f.D.E.e.C.b.A.@.a.B.c.#
# ######################.#
# #d.....................#
# ########################"""
#     maze_solver = process.Maze(input_maze)
#     assert maze_solver.distance_2() == 86
#
#
# def test_new_method_3():
#     input_maze = """\
# ########################
# #...............b.C.D.f#
# #.######################
# #.....@.a.B.c.d.A.e.F.g#
# ########################"""
#     maze_solver = process.Maze(input_maze)
#     assert maze_solver.distance_2() == 132
#
#
# def test_new_method_4():
#     input_maze = """\
# #################
# #i.G..c...e..H.p#
# ########.########
# #j.A..b...f..D.o#
# ########@########
# #k.E..a...g..B.n#
# ########.########
# #l.F..d...h..C.m#
# #################"""
#     maze_solver = process.Maze(input_maze)
#     assert maze_solver.distance_2() == 136
#
#
# ###
#
# def test_new_new_method_0():
#     input_maze = """\
# #########
# #....@.a#
# #########"""
#     maze_solver = process.Maze(input_maze)
#     assert maze_solver.distance_3() == 2
#
#
# def test_new_new_method_1():
#     input_maze = """\
# #########
# #b.A.@.a#
# #########"""
#     maze_solver = process.Maze(input_maze)
#     assert maze_solver.distance_3() == 8
#
#
# def test_new_new_method_3():
#     input_maze = """\
# ########################
# #f.D.E.e.C.b.A.@.a.B.c.#
# ######################.#
# #d.....................#
# ########################"""
#     maze_solver = process.Maze(input_maze)
#     assert maze_solver.distance_3() == 86
#
#
# def test_new_new_method_4():
#     input_maze = """\
# #################
# #i.G..c...e..H.p#
# ########.########
# #j.A..b...f..D.o#
# ########@########
# #k.E..a...g..B.n#
# ########.########
# #l.F..d...h..C.m#
# #################"""
#     maze_solver = process.Maze(input_maze)
#     assert maze_solver.distance_3() == 136
