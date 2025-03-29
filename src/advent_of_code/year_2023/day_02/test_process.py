from advent_of_code.year_2023.day_02 import process


def test_process():
    games_record_input = """\
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""
    games_record = process.generate_games_record(games_record_input)

    min_no_of_cubes_needed = process.calculate_min_no_of_cubes_needed(games_record)
    assert min_no_of_cubes_needed == {
        1: process.CubeSelection(red=4, green=2, blue=6),
        2: process.CubeSelection(red=1, green=3, blue=4),
        3: process.CubeSelection(red=20, green=13, blue=6),
        4: process.CubeSelection(red=14, green=3, blue=15),
        5: process.CubeSelection(red=6, green=3, blue=2),
    }

    games_possible_with_result = process.games_possible_with(
        min_no_of_cubes_needed, process.ELF_QUESTION_CUBE_SELECTION
    )
    assert games_possible_with_result == [1, 2, 5]
    assert sum(games_possible_with_result) == 8

    power_levels = process.generate_power_levels(min_no_of_cubes_needed.values())
    assert power_levels == [48, 12, 1560, 630, 36]
    assert sum(power_levels) == 2286
