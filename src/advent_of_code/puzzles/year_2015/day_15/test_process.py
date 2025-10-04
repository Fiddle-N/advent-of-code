from advent_of_code.puzzles.year_2015.day_15 import process


def test_calculate_best_score() -> None:
    ingredient_text = """\
Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3"""
    ingredients = process.parse_ingredients(ingredient_text)
    assert process.calculate_best_score(ingredients) == 62842880


def test_calculate_best_score_target_calories() -> None:
    ingredient_text = """\
Butterscotch: capacity -1, durability -2, flavor 6, texture 3, calories 8
Cinnamon: capacity 2, durability 3, flavor -2, texture -1, calories 3"""
    ingredients = process.parse_ingredients(ingredient_text)
    assert process.calculate_best_score(ingredients, target_calories=500) == 57600000
