"""
2015 Day 15

Part 1
Ingredients have a certain capacity, durability, flavour and texture. Work out the total score possible from 100
teaspoons of the various ingredients. Work out the total properties for each teaspoon combo and multiply - if a property
total would be negative, that is instead set to zero.

Part 2
Part 1, but only consider where teaspoons equal exactly 500 calories.
"""

import re
from collections.abc import Iterator
from dataclasses import dataclass
import math

from advent_of_code.common import read_file, timed_run

TEASPOON_NO = 100
TARGET_CALORIES = 500
INGREDIENT_PATTERN = r"(?P<name>\w+): capacity (?P<capacity>-?\d+), durability (?P<durability>-?\d+), flavor (?P<flavor>-?\d+), texture (?P<texture>-?\d+), calories (?P<calories>-?\d+)"


@dataclass(frozen=True)
class Ingredient:
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int


def parse_ingredients(ingredient_text: str) -> dict[str, Ingredient]:
    ingredients: dict[str, Ingredient] = {}
    for line in ingredient_text.splitlines():
        if (match := re.fullmatch(INGREDIENT_PATTERN, line)) is not None:
            name = match.group("name")
            capacity = int(match.group("capacity"))
            durability = int(match.group("durability"))
            flavor = int(match.group("flavor"))
            texture = int(match.group("texture"))
            calories = int(match.group("calories"))
            ingredients[name] = Ingredient(
                capacity, durability, flavor, texture, calories
            )
    return ingredients


def generate_target_tuples(target: int, n: int) -> Iterator[tuple[int, ...]]:
    if n == 1:
        yield (target,)
        return
    for i in range(target + 1):
        for tail in generate_target_tuples(target - i, n - 1):
            yield (i,) + tail


def calculate_best_score(
    ingredients: dict[str, Ingredient], target_calories: int | None = None
) -> int:
    best_score = 0
    for teaspoons in generate_target_tuples(TEASPOON_NO, len(ingredients)):
        if sum(teaspoons) != TEASPOON_NO:
            continue
        if target_calories is not None:
            calories = sum(
                teaspoon * ingredient.calories
                for teaspoon, ingredient in zip(teaspoons, ingredients.values())
            )
            if calories != target_calories:
                continue
        property_scores = []
        for ingredient_property in ("capacity", "durability", "flavor", "texture"):
            property_score = sum(
                teaspoon * getattr(ingredient, ingredient_property)
                for teaspoon, ingredient in zip(teaspoons, ingredients.values())
            )
            if property_score < 0:
                property_score = 0
            property_scores.append(property_score)
        score = math.prod(property_scores)
        if score > best_score:
            best_score = score
    return best_score


def run():
    ingredient_text = read_file()
    ingredient_stats = parse_ingredients(ingredient_text)
    print(calculate_best_score(ingredient_stats))
    print(calculate_best_score(ingredient_stats, target_calories=TARGET_CALORIES))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
