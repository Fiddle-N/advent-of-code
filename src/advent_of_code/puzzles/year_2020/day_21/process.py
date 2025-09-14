import collections
import dataclasses
import itertools
import re
import timeit


@dataclasses.dataclass
class Food:
    ingredients: set
    allergens: set


class AllergenAssessment:

    def __init__(self, foods):
        self.foods = foods
        ingredients = itertools.chain.from_iterable(food.ingredients for food in self.foods)
        self.ingredients = collections.Counter(ingredients)
        self.allergens = set.union(*[food.allergens for food in self.foods])
        self.allergenic_ingredients = self._calculate_allergenic_ingredients()

    @classmethod
    def from_string(cls, food_str):
        foods = []
        for line in food_str.splitlines():
            line_re = re.match(r'(.*) \(contains (.*)\)', line)
            raw_ingredients = line_re.group(1)
            raw_allergens = line_re.group(2)
            ingredients = {*raw_ingredients.split()}
            allergens = {*raw_allergens.split(', ')}
            foods.append(Food(ingredients, allergens))
        return cls(foods)

    @classmethod
    def from_file(cls):
        with open('input.txt') as f:
            return cls.from_string(f.read().strip())

    def _extract_allergenic_ingredients(self):
        possible_allergenic_ingredients = {}
        for allergen in self.allergens:
            foods_containing_allergen = [food for food in self.foods if allergen in food.allergens]
            possible_ingredients_for_allergen = set.intersection(
                *[food.ingredients for food in foods_containing_allergen])
            if possible_ingredients_for_allergen:
                possible_allergenic_ingredients[allergen] = possible_ingredients_for_allergen
        return possible_allergenic_ingredients

    @staticmethod
    def _resolve_allergenic_ingredients(possible_allergenic_ingredients):
        while not all((len(ingredients) == 1) for ingredients in possible_allergenic_ingredients.values()):
            unresolved_allergenic_ingredients = possible_allergenic_ingredients
            resolved_ingredients = set.union(
                *[ingredients for ingredients in unresolved_allergenic_ingredients.values() if len(ingredients) == 1]
            )
            possible_allergenic_ingredients = {}
            for allergen, ingredients in unresolved_allergenic_ingredients.items():
                if len(ingredients) == 1:
                    possible_allergenic_ingredients[allergen] = ingredients
                else:
                    possible_allergenic_ingredients[allergen] = (ingredients - resolved_ingredients)

        allergenic_ingredients = {}
        for allergen, ingredients in possible_allergenic_ingredients.items():
            ingredients, = ingredients
            allergenic_ingredients[allergen] = ingredients
        return allergenic_ingredients

    def _calculate_allergenic_ingredients(self):
        possible_allergenic_ingredients = self._extract_allergenic_ingredients()
        allergenic_ingredients = self._resolve_allergenic_ingredients(possible_allergenic_ingredients)
        return allergenic_ingredients

    @property
    def non_allergenic_ingredients(self):
        allergenic_ingredients = set(self.allergenic_ingredients.values())
        return set(self.ingredients) - allergenic_ingredients

    def non_allergenic_ingredient_occurrence(self):
        non_allergenic_ingredients = self.non_allergenic_ingredients
        return sum(count for ingredient, count in self.ingredients.items() if ingredient in non_allergenic_ingredients)

    @property
    def canonical_dangerous_ingredients(self):
        return ','.join(
            ingredients
            for _, ingredients in sorted(self.allergenic_ingredients.items(), key=lambda x: x[0])
        )


def main():
    allergen_assessment = AllergenAssessment.from_file()
    print(f'Non allergenic ingredient occurrence: {allergen_assessment.non_allergenic_ingredient_occurrence()}')
    print(f'Canonical dangerous ingredients: {allergen_assessment.canonical_dangerous_ingredients}')


if __name__ == '__main__':
    print(f'Completed in {timeit.timeit(main, number=1)} seconds')