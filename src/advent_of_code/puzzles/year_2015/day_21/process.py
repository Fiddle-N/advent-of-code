"""
2015 Day 21

https://adventofcode.com/2015/day/21

Part 1
Winning with the lowest cost.

Part 2
Losing with the highest cost.
"""

import operator
from itertools import product
from dataclasses import dataclass
from typing import Self, Literal
from math import ceil

from advent_of_code.common import read_file, timed_run

PLAYER_HP = 100


@dataclass(frozen=True)
class EquipmentStats:
    cost: int
    damage: int
    armour: int

    def __add__(self: Self, other: Self):
        return type(self)(
            cost=self.cost + other.cost,
            damage=self.damage + other.damage,
            armour=self.armour + other.armour,
        )


@dataclass(frozen=True)
class Item:
    name: str
    stats: EquipmentStats


WEAPONS = [
    Item(name="Dagger", stats=EquipmentStats(cost=8, damage=4, armour=0)),
    Item(name="Shortsword", stats=EquipmentStats(cost=10, damage=5, armour=0)),
    Item(name="Warhammer", stats=EquipmentStats(cost=25, damage=6, armour=0)),
    Item(name="Longsword", stats=EquipmentStats(cost=40, damage=7, armour=0)),
    Item(name="Greataxe", stats=EquipmentStats(cost=74, damage=8, armour=0)),
]

ARMOUR = [
    Item(
        name="", stats=EquipmentStats(cost=0, damage=0, armour=0)
    ),  # represents no armour
    Item(name="Leather", stats=EquipmentStats(cost=13, damage=0, armour=1)),
    Item(name="Chainmail", stats=EquipmentStats(cost=31, damage=0, armour=2)),
    Item(name="Splintmail", stats=EquipmentStats(cost=53, damage=0, armour=3)),
    Item(name="Bandedmail", stats=EquipmentStats(cost=75, damage=0, armour=4)),
    Item(name="Platemail", stats=EquipmentStats(cost=102, damage=0, armour=5)),
]

RINGS = [
    Item(
        name="", stats=EquipmentStats(cost=0, damage=0, armour=0)
    ),  # represents no ring
    Item(name="Damage +1", stats=EquipmentStats(cost=25, damage=1, armour=0)),
    Item(name="Damage +2", stats=EquipmentStats(cost=50, damage=2, armour=0)),
    Item(name="Damage +3", stats=EquipmentStats(cost=100, damage=3, armour=0)),
    Item(name="Defense +1", stats=EquipmentStats(cost=20, damage=0, armour=1)),
    Item(name="Defense +2", stats=EquipmentStats(cost=40, damage=0, armour=2)),
    Item(name="Defense +3", stats=EquipmentStats(cost=80, damage=0, armour=3)),
]


@dataclass(frozen=True)
class CharacterStats:
    hp: int
    damage: int
    armour: int


def calculate_equipment_stats() -> list[EquipmentStats]:
    uniq_equipment_stats = set()
    # choice of one weapon, one armour and two rings
    # armour choices already include no armour and ring choices already include no ring
    for weapon, armour, ring_1, ring_2 in product(
        WEAPONS,
        ARMOUR,
        RINGS,
        RINGS,
    ):
        if ring_1.name and ring_1.name == ring_2.name:
            # disallow using the exact same ring - only one of each item exists
            continue
        combined_stats = weapon.stats + armour.stats + ring_1.stats + ring_2.stats
        uniq_equipment_stats.add(combined_stats)
    return list(uniq_equipment_stats)


def parse_boss_stats(raw_boss_stats: str) -> CharacterStats:
    boss_stats = [int(line.split(": ")[1]) for line in raw_boss_stats.splitlines()]
    return CharacterStats(hp=boss_stats[0], damage=boss_stats[1], armour=boss_stats[2])


def battle(
    boss_stats: CharacterStats,
    player_equipment_stats: list[EquipmentStats],
    mode: Literal["best_win", "worst_loss"],
) -> int | None:
    # sort by lowest to highest cost if calculating best win, and highest to lowest if worst loss
    player_equipment_stats = sorted(
        player_equipment_stats,
        key=lambda stats: stats.cost,
        reverse=(mode == "worst_loss"),
    )

    # to calculate player vs boss battle
    # calculate how many rounds each needs to defeat the other and compare values against each other
    # since player goes first, if they need the same number of rounds or less compared to the boss, they win
    # for loss condition, we use the exact opposite comparison, strictly if they need more rounds than the boss
    player_boss_damage_comp_fn = operator.le if mode == "best_win" else operator.gt

    for equipment_stats in player_equipment_stats:
        player_stats = CharacterStats(
            hp=PLAYER_HP,
            damage=equipment_stats.damage,
            armour=equipment_stats.armour,
        )

        # character must deal at least one damage
        player_dmg = max(player_stats.damage - boss_stats.armour, 1)
        boss_dmg = max(boss_stats.damage - player_stats.armour, 1)
        player_win_rounds = ceil(boss_stats.hp / player_dmg)
        boss_win_rounds = ceil(player_stats.hp / boss_dmg)
        if player_boss_damage_comp_fn(player_win_rounds, boss_win_rounds):
            return equipment_stats.cost


def run():
    raw_boss_stats = read_file()
    boss_stats = parse_boss_stats(raw_boss_stats)
    equipment_stats = calculate_equipment_stats()
    print(battle(boss_stats, equipment_stats, mode="best_win"))
    print(battle(boss_stats, equipment_stats, mode="worst_loss"))


def main() -> None:
    timed_run(run)


if __name__ == "__main__":
    main()
