from advent_of_code.puzzles.year_2019.day_03 import process


def test_example_1():
    cw = process.CrossedWires(
        path1=["R75", "D30", "R83", "U83", "L12", "D49", "R71", "U7", "L72"],
        path2=["U62", "R66", "U55", "R34", "D71", "R55", "D58", "R83"],
    )
    cw.calculate_coords_and_steps()
    closest_intersection_distance = cw.find_closest_intersection()
    assert closest_intersection_distance == 159
    fewest_combined_steps = cw.find_fewest_combined_steps()
    assert fewest_combined_steps == 610


def test_example_2():
    cw = process.CrossedWires(
        path1=[
            "R98",
            "U47",
            "R26",
            "D63",
            "R33",
            "U87",
            "L62",
            "D20",
            "R33",
            "U53",
            "R51",
        ],
        path2=["U98", "R91", "D20", "R16", "D67", "R40", "U7", "R15", "U6", "R7"],
    )
    cw.calculate_coords_and_steps()
    closest_intersection_distance = cw.find_closest_intersection()
    assert closest_intersection_distance == 135
    fewest_combined_steps = cw.find_fewest_combined_steps()
    assert fewest_combined_steps == 410
