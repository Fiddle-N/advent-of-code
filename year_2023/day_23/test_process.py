from year_2023.day_23 import process


def test_hiking_trail():
    hiking_trail_input = """\
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
    hiking_trails = process.HikingTrails(hiking_trail_input)

    di_graph = process.generate_graph(hiking_trails)
    di_paths = process.resolve_all_paths(
        di_graph,
        start=hiking_trails.start,
        end=hiking_trails.end
    )
    assert sorted(di_paths) == [
        74, 82, 82, 86, 90, 94
    ]
    largest_path_dist = process.find_largest_path(di_paths)
    assert largest_path_dist == 94

    undi_graph = process.di_to_undi_graph(
        di_graph,
        start=hiking_trails.start,
        end=hiking_trails.end
    )
    undi_paths = process.resolve_all_paths(
        undi_graph,
        start=hiking_trails.start,
        end=hiking_trails.end
    )
    largest_undi_path_dist = process.find_largest_path(undi_paths)
    assert largest_undi_path_dist == 154
