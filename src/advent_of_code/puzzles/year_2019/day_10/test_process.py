from advent_of_code.puzzles.year_2019.day_10 import process


def test_example_1():
    text = """\
......#.#.
#..#.#....
..#######.
.#.#.###..
.#..#.....
..#....#.#
#..#....#.
.##.#..###
##...#..#.
.#....####
"""
    region = process.grid(text)
    asteroids = process.get_asteroids(region)
    best_location = process.get_best_location(asteroids)
    location, detected_asteroids = best_location
    assert (location.x, location.y) == (5, 8)
    assert detected_asteroids == 33


def test_example_2():
    text = """\
#.#...#.#.
.###....#.
.#....#...
##.#.#.#.#
....#.#.#.
.##..###.#
..#...##..
..##....##
......#...
.####.###.
"""
    region = process.grid(text)
    asteroids = process.get_asteroids(region)
    best_location = process.get_best_location(asteroids)
    location, detected_asteroids = best_location
    assert (location.x, location.y) == (1, 2)
    assert detected_asteroids == 35


def test_example_3():
    text = """\
.#..#..###
####.###.#
....###.#.
..###.##.#
##.##.#.#.
....###..#
..#.#..#.#
#..#.#.###
.##...##.#
.....#.#..
"""
    region = process.grid(text)
    asteroids = process.get_asteroids(region)
    best_location = process.get_best_location(asteroids)
    location, detected_asteroids = best_location
    assert (location.x, location.y) == (6, 3)
    assert detected_asteroids == 41


def test_example_4():
    text = """\
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
"""
    region = process.grid(text)
    asteroids = process.get_asteroids(region)
    best_location = process.get_best_location(asteroids)
    location, detected_asteroids = best_location
    assert (location.x, location.y) == (11, 13)
    assert detected_asteroids == 210


def test_example_5():
    text = """\
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
"""
    region = process.grid(text)
    asteroids = process.get_asteroids(region)
    best_location = process.get_best_location(asteroids)
    location, detected_asteroids = best_location
    assert (location.x, location.y) == (11, 13)
    assert detected_asteroids == 210


def test_incomplete_example():
    text = """\
.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##
"""
    region = process.grid(text)
    asteroids = process.get_asteroids(region)
    point = process.Coords(11, 13)
    angle_distances = process.clockwise(point, asteroids)
    sorted_true_angles = process.calculate_true_angle(angle_distances)
    correct_asteroid = process.two_hundred_asteroid(sorted_true_angles)
    assert (correct_asteroid.x, correct_asteroid.y) == (8, 2)
