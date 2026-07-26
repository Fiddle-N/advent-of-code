from advent_of_code.puzzles.year_2016.day_24 import process


def test_shortest_visit() -> None:
    maze = process.parse_maze("""\
###########
#0.1.....2#
#.#######.#
#4.......3#
###########""")
    shortest_pairs = process.calculate_shortest_pairs(maze)
    assert (
        process.calculate_shortest_route(maze, shortest_pairs, return_to_start=False)
        == 14
    )
