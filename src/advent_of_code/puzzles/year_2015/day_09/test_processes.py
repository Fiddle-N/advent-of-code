from advent_of_code.puzzles.year_2015.day_09 import process


def test_shortest_distance():
    distance_text = """\
London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141"""
    dr = process.DistanceResolver.from_distances(distance_text)
    assert dr.shortest_path_length() == 605


def test_longest_distance():
    distance_text = """\
London to Dublin = 464
London to Belfast = 518
Dublin to Belfast = 141"""
    dr = process.DistanceResolver.from_distances(distance_text)
    assert dr.longest_path_length() == 982
