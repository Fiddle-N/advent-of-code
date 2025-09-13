from advent_of_code.puzzles.year_2023.day_17 import process


def test_crucible_minimal_heat_loss():
    city_input = """\
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""
    city = process.City(city_input)
    assert process.crucible_minimal_heat_loss(city) == 102


def test_ultra_crucible_minimal_heat_loss():
    city_input = """\
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533"""
    city = process.City(city_input)
    assert process.ultra_crucible_minimal_heat_loss(city) == 94


def test_ultra_crucible_minimal_heat_loss_with_non_optimal_city():
    city_input = """\
111111111111
999999999991
999999999991
999999999991
999999999991"""
    city = process.City(city_input)
    assert process.ultra_crucible_minimal_heat_loss(city) == 71


def test_minimal_heat_loss_start_position():
    # ensure that we can move 3 positions straight from the start position
    # and do not count the start positions itself as a straight move
    city_input = """\
29
19
19
11"""
    city = process.City(city_input)
    assert process.crucible_minimal_heat_loss(city) == 4


def test_minimal_heat_loss_minimal_input():
    city_input = """\
13242232
33423242
24222222"""
    city = process.City(city_input)
    assert process.crucible_minimal_heat_loss(city) == 22
