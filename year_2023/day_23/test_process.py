from year_2023.day_23 import process


def test_input():
    input_ = """\
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#"""
    hiking_trails = process.HikingTrails(input_)
    graph = process.generate_graph(hiking_trails)
    paths = process.resolve_all_paths(
        graph,
        start=hiking_trails.start,
        end=hiking_trails.end
    )
    assert sorted(paths.values()) == [
        74, 82, 82, 86, 90, 94
    ]
    largest_path_info = process.find_largest_path(paths)
    largest_path, largest_path_dist = largest_path_info
    assert largest_path == (
        process.Coords(1, 0),
        process.Coords(3, 5),
        process.Coords(11, 3),
        process.Coords(13, 13),
        process.Coords(21, 11),
        process.Coords(19, 19),
        process.Coords(21, 22),
    )
    assert largest_path_dist == 94
