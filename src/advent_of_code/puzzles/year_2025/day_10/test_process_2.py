from advent_of_code.puzzles.year_2025.day_10 import process_2


def test_parse():
    input_ = """\
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""
    machines = process_2.parse(input_)
    assert machines == [
        process_2.Machine(
            buttons=[
                [3],
                [1, 3],
                [2],
                [2, 3],
                [0, 2],
                [0, 1],
            ],
            joltages=[3, 5, 4, 7],
        ),
        process_2.Machine(
            buttons=[
                [0, 2, 3, 4],
                [2, 3],
                [0, 4],
                [0, 1, 2],
                [1, 2, 3, 4],
            ],
            joltages=[7, 5, 12, 7, 2],
        ),
        process_2.Machine(
            buttons=[
                [0, 1, 2, 3, 4],
                [0, 3, 4],
                [0, 1, 2, 4, 5],
                [1, 2],
            ],
            joltages=[10, 11, 11, 5, 10, 5],
        ),
    ]


"""
{3,5,4,7}

(3) -> 7
(1,3) -> 5
(2) -> 4
(2,3) -> 4
(0,2) -> 3
(0,1) -> 3

0 -> 6
1 -> 8
2 -> 11
3 -> 16

"""


def test_bfs_0():
    input_ = """\
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}"""
    (machine,) = process_2.parse(input_)
    df_searcher = process_2.JoltageDFSearcher(machine)
    assert df_searcher.dfs() == 10


def test_bfs_1():
    input_ = """\
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}"""
    (machine,) = process_2.parse(input_)
    df_searcher = process_2.JoltageDFSearcher(machine)
    assert df_searcher.dfs() == 12


def test_bfs_2():
    input_ = """\
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""
    (machine,) = process_2.parse(input_)
    df_searcher = process_2.JoltageDFSearcher(machine)
    assert df_searcher.dfs() == 11
