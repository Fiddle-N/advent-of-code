# TBD

# from advent_of_code.puzzles.year_2019.day_18 import process2
#
#
# def test_maze_1():
#     input_maze = """\
# #######
# #a.#Cd#
# ##@#@##
# #######
# ##@#@##
# #cB#Ab#
# #######"""
#     maze_solver = process2.Maze(input_maze)
#     assert maze_solver.distance() == 8
#
#
# def test_maze_2():
#     input_maze = """\
# ###############
# #d.ABC.#.....a#
# ######@#@######
# ###############
# ######@#@######
# #b.....#.....c#
# ###############"""
#     maze_solver = process2.Maze(input_maze)
#     assert maze_solver.distance() == 24
#
#
# def test_maze_3():
#     input_maze = """\
# #############
# #DcBa.#.GhKl#
# #.###@#@#I###
# #e#d#####j#k#
# ###C#@#@###J#
# #fEbA.#.FgHi#
# #############"""
#     maze_solver = process2.Maze(input_maze)
#     assert maze_solver.distance() == 32
#
#
# def test_maze_4():
#     input_maze = """\
# #############
# #g#f.D#..h#l#
# #F###e#E###.#
# #dCba@#@BcIJ#
# #############
# #nK.L@#@G...#
# #M###N#H###.#
# #o#m..#i#jk.#
# #############"""
#     maze_solver = process2.Maze(input_maze)
#     assert maze_solver.distance() == 72
