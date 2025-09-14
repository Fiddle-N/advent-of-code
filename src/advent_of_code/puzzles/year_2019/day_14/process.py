import collections
import math
import timeit
import dataclasses
import copy
import itertools
import fractions

import numpy


@dataclasses.dataclass
class Product:
    name: str
    qty: int
    reagents: dict


@dataclasses.dataclass
class Package:
    name: str
    qty: int


# Product = collections.namedtuple('Product', 'name qty reagents')
# Package = collections.namedtuple('Package', 'name qty')


def read_file():
    with open("input.txt") as f:
        return f.read().rstrip()


def _split_package_text(text):
    return text.split(" ")


def process_text(text):
    reactions = {}
    for reaction in text.split("\n"):
        reagent_str, product = reaction.split(" => ")
        raw_reagents = reagent_str.split(", ")
        product_qty, product_name = product.split(" ")
        # reagents = []
        reagents = collections.defaultdict(int)
        for reagent in raw_reagents:
            reagent_qty, reagent_name = reagent.split(" ")
            reagents[reagent_name] = int(reagent_qty)
            # reagents.append(Package(reagent_name, int(reagent_qty)))
        reactions[product_name] = Product(
            name=product_name,
            qty=int(product_qty),
            reagents=reagents,
        )
    return reactions


def _satisfied(requirements):
    for chemical, required in requirements.items():
        if required > 0 and chemical != "ORE":
            return False
    return True


def _get_next_requirement(requirements):
    for chemical, required in requirements.items():
        if required > 0 and chemical != "ORE":
            return Package(chemical, required)


def calculate_one_fuel(reactions, state=None):
    if state is None:
        state = collections.defaultdict(int)
    state["FUEL"] = 1
    while not _satisfied(state):
        requirement = _get_next_requirement(state)
        reaction = reactions[requirement.name]
        multiplier = math.ceil(requirement.qty / reaction.qty)
        produced = reaction.qty * multiplier
        state[reaction.name] -= produced
        for reagent, qty in reaction.reagents.items():
            required = qty * multiplier
            state[reagent] += required
    return state


def calculate_full_exchange_slow_af(reactions, state=None):
    fuel = 0
    while True:
        state = calculate_one_fuel(reactions, state)
        state_without_ore = {chem: val for chem, val in state.items() if chem != "ORE"}
        fuel += 1
        if not any(state_without_ore.values()):
            break
    return fuel, state["ORE"]


# def calculate_exchange_failed(reactions):
#     for chemical, reaction in reactions.copy().items():
#         if reaction.reagents[0].name == 'ORE':
#             continue
#         for reagent in reaction.reagents.copy():
#             lcm = numpy.lcm(reaction.qty, reagent.qty)
#             reaction_qty_multiple = int(lcm / reaction.qty)
#             reagent_qty_multiple = int(lcm / reagent.qty)
#
#             reaction.qty *= reaction_qty_multiple
#             for reagent in reaction.reagents:
#                 reagent.qty *= reaction_qty_multiple
#
#             products = [reactions[reagent.name] for reagent in reaction.reagents.copy()]
#             for product in products:
#                 product.qty *= reagent_qty_multiple
#                 for reagent in product.reagents:
#                     reagent.qty *= reagent_qty_multiple
#     print(0)


# def _are_reagents_still_remaining(product, remaining_chemicals):
#     for reagent in product.reagents:
#         if reagent in remaining_chemicals:
#             return True
#     return False


# def _retrieve_matching_products(reactions, name):
#
#     :
#         :
#             matching_products.append()


def calculate_lcms(product, reagents):
    lcms = [numpy.lcm(qty, product, dtype="int64") for qty in reagents]
    iterators = [
        list(
            itertools.takewhile(
                lambda x: x <= lcm, itertools.accumulate(itertools.repeat(reagent))
            )
        )
        for reagent, lcm in zip(reagents, lcms)
    ]
    combinations = [
        (combination, sum(combination)) for combination in itertools.product(*iterators)
    ]
    sorted_combinations = sorted(combinations, key=lambda x: x[1])
    result = None
    for combination, sum_val in sorted_combinations:
        if not (sum_val % product):
            result = combination
            break
    return result


def calculate_exchange(reactions):
    chemicals = list(reactions.keys())
    remaining_chemicals = set(chemicals)
    remaining_chemicals.add("ORE")
    while remaining_chemicals != {"ORE"}:
        next_chemical = chemicals.pop(0)
        next_product = reactions[next_chemical]
        if next_product is None:
            continue
        # if _are_reagents_still_remaining(next_product, remaining_chemicals):
        if not (len(next_product.reagents) == 1 and "ORE" in next_product.reagents):
            chemicals.append(next_chemical)
            continue
        matching_products = [
            product
            for chemical, product in reactions.items()
            if next_chemical in reactions[chemical].reagents
        ]
        matching_product_qty = [
            product.reagents[next_chemical] for product in matching_products
        ]
        # lcm_inputs = matching_product_qty.copy()
        # lcms = [
        #     numpy.lcm(qty, next_product.qty, dtype='int64')
        #     for qty in matching_product_qty
        # ]
        lcms = calculate_lcms(next_product.qty, matching_product_qty)
        # lcm_inputs.append(next_product.qty)
        # lcm = numpy.lcm.reduce(lcm_inputs)
        # ore_multiplier = int(lcm / next_product.qty)
        # ore_value = ore_multiplier * next_product.reagents['ORE']
        matching_product_multipliers = [
            int(lcm / qty) for qty, lcm in zip(matching_product_qty, lcms)
        ]
        for product, multiplier, lcm in zip(
            matching_products, matching_product_multipliers, lcms
        ):
            for reagent in product.reagents:
                product.reagents[reagent] *= multiplier

            product.qty *= multiplier
            product.reagents.pop(next_chemical)
            ore_multiplier = fractions.Fraction(lcm, next_product.qty)
            ore_value = ore_multiplier * next_product.reagents["ORE"]
            product.reagents["ORE"] += ore_value
        if next_chemical != "FUEL":
            reactions.pop(next_chemical)
        remaining_chemicals.remove(next_product.name)
    return reactions["FUEL"].qty, reactions["FUEL"].reagents["ORE"]


def fuel_for_ore(reactions, ore_store):
    state = collections.defaultdict(int)
    state["ORE"] = -ore_store
    fuel_store = 0
    while True:
        calculate_one_fuel(reactions, state)
        possible_ore_store = -state["ORE"]
        if possible_ore_store < 0:
            break
        else:
            fuel_store += 1
    return fuel_store


def max_fuel(reactions):
    temp_reactions = copy.deepcopy(reactions)
    full_exchange_fuel, full_exchange_ore = calculate_exchange(temp_reactions)
    fuel = (full_exchange_fuel / full_exchange_ore) * 1_000_000_000_000
    fuel = int(fuel)
    return fuel


def main():
    reaction_text = read_file()
    reactions = process_text(reaction_text)
    state = calculate_one_fuel(reactions)
    print("Ore required for exactly one fuel:", state["ORE"])
    fuel = max_fuel(reactions)
    print(fuel)


if __name__ == "__main__":
    print(timeit.timeit(main, number=1))
