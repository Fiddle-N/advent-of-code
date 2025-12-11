from advent_of_code.puzzles.year_2025.day_10 import process


def test_parse():
    input_ = """\
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""
    machines = process.parse(input_)
    assert machines == [
        process.Machine(lights=6, buttons=[1, 5, 2, 3, 10, 12]),
        process.Machine(lights=2, buttons=[23, 6, 17, 28, 15]),
        process.Machine(lights=29, buttons=[62, 38, 59, 24]),
    ]


def test_bfs_0():
    input_ = """\
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}"""
    (machine,) = process.parse(input_)
    assert process.bfs(machine) == 2


def test_bfs_1():
    input_ = """\
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}"""
    (machine,) = process.parse(input_)
    assert process.bfs(machine) == 3


def test_bfs_2():
    input_ = """\
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}"""
    (machine,) = process.parse(input_)
    assert process.bfs(machine) == 2
